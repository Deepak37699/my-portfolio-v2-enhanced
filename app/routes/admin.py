from fastapi import APIRouter, Request, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.encoders import jsonable_encoder
from starlette.responses import JSONResponse
import logging

# Initialize logger
logger = logging.getLogger(__name__)

router = APIRouter()

@router.get("/auth/login", response_class=HTMLResponse, name="admin_login")
async def admin_login(request: Request):
    """Admin login page."""
    templates = request.app.state.templates
    return templates.TemplateResponse("admin/login.html", {"request": request})

@router.get("/api/message-stats")
async def get_message_stats(request: Request):
    """API endpoint to get message statistics."""
    try:
        from app.services.data_manager import DataManager
        data_manager = DataManager()
        messages = data_manager.get_all_messages()
        
        total_messages = len(messages)
        unread_messages = len([m for m in messages if not getattr(m, 'is_read', False)])
        
        return JSONResponse(content=jsonable_encoder({
            "total_messages": total_messages,
            "unread_messages": unread_messages
        }))
    except Exception as e:
        logger.error(f"Error fetching message stats: {e}")
        raise HTTPException(status_code=500, detail="Unable to fetch message statistics")

@router.get("/dashboard", response_class=HTMLResponse, name="admin_dashboard")
async def admin_dashboard(request: Request):
    """Admin dashboard page."""
    try:
        from app.services.data_manager import DataManager
        
        templates = request.app.state.templates
        data_manager = DataManager()
        
        # Get dashboard data with error handling
        try:
            projects = data_manager.get_all_projects()
            skills = data_manager.get_all_skills()
            messages = data_manager.get_all_messages()
        except Exception as e:
            logger.error(f"Error fetching dashboard data: {e}")
            projects = []
            skills = []
            messages = []
        
        # Calculate stats with empty list fallbacks
        stats = {
            "total_projects": len(projects),
            "featured_projects": len([p for p in projects if getattr(p, 'featured', False)]),
            "total_skills": len(skills),
            "total_messages": len(messages),
            "unread_messages": len([m for m in messages if not getattr(m, 'is_read', False)])
        }
        
        # Get recent messages (last 5) with empty list fallback
        recent_messages = sorted(messages, key=lambda x: getattr(x, 'created_date', ''), reverse=True)[:5] if messages else []
        
        # Mock user data (you might want to get this from session/auth)
        user = {"username": "admin"}
        
        context = {
            "request": request,
            "stats": stats,
            "recent_messages": recent_messages,
            "user": user
        }
        
        return templates.TemplateResponse("admin/dashboard.html", context)
        
    except Exception as e:
        logger.error(f"Error rendering admin dashboard: {e}")
        return templates.TemplateResponse("error.html", {
            "request": request,
            "error_message": "Unable to load dashboard data"
        }, status_code=500)
