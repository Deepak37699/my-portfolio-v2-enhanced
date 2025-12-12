from fastapi import APIRouter, Depends, HTTPException, status, Form, Request, Response
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from datetime import timedelta
import logging

from app.models.user import UserLogin, Token, UserCreate
from app.services.data_manager import DataManager
from app.utils.security import (
    verify_password, 
    create_access_token, 
    verify_token, 
    get_password_hash,
    generate_default_admin_password,
    validate_password_strength,
    ACCESS_TOKEN_EXPIRE_MINUTES
)

logger = logging.getLogger(__name__)

router = APIRouter()
security = HTTPBearer(auto_error=False)
data_manager = DataManager()


def get_templates(request: Request) -> Jinja2Templates:
    """Get templates from app state."""
    return request.app.state.templates


async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """Get current authenticated user."""
    if not credentials:
        return None
    
    token_data = verify_token(credentials.credentials)
    if not token_data or not token_data.username:
        return None
    
    user = data_manager.get_user_by_username(token_data.username)
    if not user or not user.is_active:
        return None
    
    return user


async def require_auth(current_user = Depends(get_current_user)):
    """Require authentication - raises exception if not authenticated."""
    if not current_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return current_user


@router.get("/login", response_class=HTMLResponse)
async def login_page(request: Request, templates: Jinja2Templates = Depends(get_templates)):
    """Display login page."""
    try:
        return templates.TemplateResponse("admin/login.html", {
            "request": request,
            "page_title": "Admin Login",
            "error_message": request.query_params.get("error"),
            "success_message": request.query_params.get("success")
        })
    except Exception as e:
        logger.error(f"Error loading login page: {e}")
        raise HTTPException(status_code=500, detail="Error loading login page")


@router.post("/login", response_class=HTMLResponse)
async def login(
    request: Request,
    username: str = Form(...),
    password: str = Form(...),
    templates: Jinja2Templates = Depends(get_templates)
):
    """Handle login form submission."""
    try:
        # Print detailed debug information
        print(f"====== LOGIN ATTEMPT ======")
        print(f"Username: {username}")
        print(f"Password length: {len(password)}")
        logger.info(f"Login attempt for user: {username}")
          # Check if user exists
        user = data_manager.get_user_by_username(username)
        print(f"User found in database: {user is not None}")
        logger.debug(f"User found: {user is not None}")
        
        if not user:
            print(f"User '{username}' not found in database")
            logger.warning(f"Login failed: User '{username}' not found")
            return RedirectResponse(
                url="/auth/login?error=Invalid username or password",
                status_code=303
            )
            
        if not user.is_active:
            print(f"User '{username}' is not active")
            logger.warning(f"Login failed: User '{username}' is inactive")
            return RedirectResponse(
                url="/auth/login?error=Account is inactive",
                status_code=303
            )
        
        # Verify password
        is_password_valid = verify_password(password, user.hashed_password)
        logger.debug(f"Password verification result: {is_password_valid}")
        
        if not is_password_valid:
            logger.warning(f"Login failed: Invalid password for user '{username}'")
            return RedirectResponse(
                url="/auth/login?error=Invalid username or password",
                status_code=303
            )
        
        logger.info(f"Login successful for user: {username}")
        
        # Create access token
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"sub": user.username}, expires_delta=access_token_expires
        )
        
        # Redirect to admin dashboard
        response = RedirectResponse(url="/admin/dashboard", status_code=303)
        response.set_cookie(
            key="access_token",
            value=f"Bearer {access_token}",
            max_age=ACCESS_TOKEN_EXPIRE_MINUTES * 60,
            httponly=True,
            secure=False  # Set to True in production with HTTPS
        )
        
        logger.info(f"User {username} logged in successfully")
        return response
        
    except Exception as e:
        logger.error(f"Login error: {e}")
        return RedirectResponse(
            url="/auth/login?error=An error occurred during login",
            status_code=303
        )


@router.post("/logout")
async def logout():
    """Handle logout."""
    response = RedirectResponse(url="/auth/login?success=Logged out successfully", status_code=303)
    response.delete_cookie(key="access_token")
    return response
    
    
@router.get("/debug-auth", include_in_schema=False)
async def debug_auth():
    """Debug endpoint for authentication."""
    try:
        # Check if default admin exists
        users = data_manager.get_all_users()
        
        users_info = []
        for i, user in enumerate(users):
            user_dict = {
                "index": i,
                "username": user.username,
                "is_active": user.is_active,
                "hash_prefix": user.hashed_password[:10] + "..." if user.hashed_password else None,
                "created_date": str(user.created_date)
            }
            users_info.append(user_dict)
        
        # Check default password manually
        default_user = data_manager.get_user_by_username("admin")
        password_check = None
        if default_user:
            try:
                password_check = verify_password("admin123", default_user.hashed_password)
            except Exception as e:
                password_check = f"Error: {str(e)}"
        
        return {
            "auth_debug": True,
            "users_count": len(users),
            "users": users_info,
            "admin_exists": any(u.username == "admin" for u in users),
            "admin_password_check": password_check
        }
    except Exception as e:
        return {"error": str(e)}


@router.post("/api/login")
async def api_login(user_credentials: UserLogin):
    """API endpoint for login."""
    try:
        # Check if user exists
        user = data_manager.get_user_by_username(user_credentials.username)
        if not user or not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid username or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        # Verify password
        if not verify_password(user_credentials.password, user.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid username or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        # Create access token
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"sub": user.username}, expires_delta=access_token_expires
        )
        
        logger.info(f"User {user_credentials.username} logged in via API")
        return {"access_token": access_token, "token_type": "bearer"}
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"API login error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )


@router.post("/api/create-admin")
async def create_admin_user(user_data: UserCreate):
    """Create the first admin user. This should be disabled after setup."""
    try:
        # Check if any users exist
        existing_users = data_manager.get_all_users()
        if existing_users:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Admin user already exists"
            )
        
        # Validate password strength
        is_strong, message = validate_password_strength(user_data.password)
        if not is_strong:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=message
            )
        
        # Hash password and create user
        hashed_password = get_password_hash(user_data.password)
        new_user = data_manager.create_user(user_data, hashed_password)
        
        logger.info(f"Admin user created: {new_user.username}")
        return {"message": "Admin user created successfully", "username": new_user.username}
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error creating admin user: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error creating admin user"
        )


@router.get("/setup", response_class=HTMLResponse)
async def setup_page(request: Request, templates: Jinja2Templates = Depends(get_templates)):
    """Setup page for creating the first admin user."""
    try:
        # Check if any users exist
        try:
            existing_users = data_manager.get_all_users()
        except Exception as e:
            logger.error(f"Error checking existing users: {e}")
            existing_users = []
            
        if existing_users:
            return RedirectResponse(url="/auth/login", status_code=303)
        
        return templates.TemplateResponse("admin/setup.html", {
            "request": request,
            "page_title": "Admin Setup",
            "error_message": request.query_params.get("error"),
            "success_message": request.query_params.get("success")
        })
    except Exception as e:
        logger.error(f"Error loading setup page: {e}")
        return templates.TemplateResponse("error.html", {
            "request": request,
            "error_message": "Unable to load setup page"
        }, status_code=500)


@router.post("/setup")
async def setup_admin(
    request: Request,
    username: str = Form(...),
    password: str = Form(...),
    confirm_password: str = Form(...),
    templates: Jinja2Templates = Depends(get_templates)
):
    """Handle admin setup form submission."""
    try:
        # Check if any users exist
        try:
            existing_users = data_manager.get_all_users()
        except Exception as e:
            logger.error(f"Error checking existing users: {e}")
            existing_users = []
            
        if existing_users:
            return RedirectResponse(url="/auth/login", status_code=303)
        
        # Validate passwords match
        if password != confirm_password:
            return RedirectResponse(
                url="/auth/setup?error=Passwords do not match",
                status_code=303
            )
        
        # Validate password strength
        is_strong, message = validate_password_strength(password)
        if not is_strong:
            return RedirectResponse(
                url=f"/auth/setup?error={message}",
                status_code=303
            )
        
        # Create user with error handling
        try:
            user_data = UserCreate(username=username.strip(), password=password)
            hashed_password = get_password_hash(password)
            new_user = data_manager.create_user(user_data, hashed_password)
            logger.info(f"Admin user created: {new_user.username}")
        except Exception as e:
            logger.error(f"Error creating admin user: {e}")
            return templates.TemplateResponse("error.html", {
                "request": request,
                "error_message": "Failed to create admin user"
            }, status_code=500)
        
        return RedirectResponse(
            url="/auth/login?success=Admin user created successfully. Please log in.",
            status_code=303
        )
        
    except Exception as e:
        logger.error(f"Error in admin setup: {e}")
        return templates.TemplateResponse("error.html", {
            "request": request,
            "error_message": "An unexpected error occurred during setup"
        }, status_code=500)


@router.get("/me")
async def get_current_user_info(current_user = Depends(require_auth)):
    """Get current user information."""
    return {
        "username": current_user.username,
        "is_active": current_user.is_active,
        "created_date": current_user.created_date
    }
