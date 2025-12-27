from fastapi import APIRouter, Request, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.encoders import jsonable_encoder
from starlette.responses import JSONResponse
import logging

# Import model classes
from app.models.education import Education, EducationCreate, EducationUpdate
from app.models.experience import Experience, ExperienceCreate, ExperienceUpdate
from app.models.certification import Certification, CertificationCreate, CertificationUpdate
from app.models.contact import ContactMessageUpdate

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

@router.get("/projects", response_class=HTMLResponse, name="admin_projects")
async def admin_projects(request: Request):
    """Admin projects management page."""
    try:
        from app.services.data_manager import DataManager

        templates = request.app.state.templates
        data_manager = DataManager()

        try:
            projects = data_manager.get_all_projects()
        except Exception as e:
            logger.error(f"Error fetching projects: {e}")
            projects = []

        user = {"username": "admin"}

        context = {
            "request": request,
            "projects": projects,
            "user": user
        }

        return templates.TemplateResponse("admin/projects.html", context)

    except Exception as e:
        logger.error(f"Error rendering admin projects: {e}")
        return templates.TemplateResponse("error.html", {
            "request": request,
            "error_message": "Unable to load projects data"
        }, status_code=500)

@router.get("/skills", response_class=HTMLResponse, name="admin_skills")
async def admin_skills(request: Request):
    """Admin skills management page."""
    try:
        from app.services.data_manager import DataManager

        templates = request.app.state.templates
        data_manager = DataManager()

        try:
            skills = data_manager.get_all_skills()
        except Exception as e:
            logger.error(f"Error fetching skills: {e}")
            skills = []

        user = {"username": "admin"}

        context = {
            "request": request,
            "skills": skills,
            "user": user
        }

        return templates.TemplateResponse("admin/skills.html", context)

    except Exception as e:
        logger.error(f"Error rendering admin skills: {e}")
        return templates.TemplateResponse("error.html", {
            "request": request,
            "error_message": "Unable to load skills data"
        }, status_code=500)

@router.get("/messages", response_class=HTMLResponse, name="admin_messages")
async def admin_messages(request: Request):
    """Admin messages management page."""
    try:
        from app.services.data_manager import DataManager

        templates = request.app.state.templates
        data_manager = DataManager()

        try:
            messages = data_manager.get_all_messages()
            # Sort messages by date (newest first)
            messages = sorted(messages, key=lambda x: getattr(x, 'created_date', ''), reverse=True)
        except Exception as e:
            logger.error(f"Error fetching messages: {e}")
            messages = []

        user = {"username": "admin"}

        context = {
            "request": request,
            "messages": messages,
            "user": user
        }

        return templates.TemplateResponse("admin/messages.html", context)

    except Exception as e:
        logger.error(f"Error rendering admin messages: {e}")
        return templates.TemplateResponse("error.html", {
            "request": request,
            "error_message": "Unable to load messages data"
        }, status_code=500)

@router.get("/messages/{message_id}", response_class=HTMLResponse, name="admin_message_detail")
async def admin_message_detail(message_id: str, request: Request):
    """Admin message detail page."""
    try:
        from app.services.data_manager import DataManager

        templates = request.app.state.templates
        data_manager = DataManager()

        try:
            messages = data_manager.get_all_messages()
            message = next((m for m in messages if str(getattr(m, 'id', '')) == message_id), None)
            if not message:
                raise HTTPException(status_code=404, detail="Message not found")
        except Exception as e:
            logger.error(f"Error fetching message {message_id}: {e}")
            raise HTTPException(status_code=404, detail="Message not found")

        user = {"username": "admin"}

        context = {
            "request": request,
            "message": message,
            "user": user
        }

        return templates.TemplateResponse("admin/message_detail.html", context)

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error rendering admin message detail: {e}")
        return templates.TemplateResponse("error.html", {
            "request": request,
            "error_message": "Unable to load message data"
        }, status_code=500)

@router.get("/about", response_class=HTMLResponse, name="admin_about")
async def admin_about(request: Request):
    """Admin about management page."""
    try:
        from app.services.data_manager import DataManager

        templates = request.app.state.templates
        data_manager = DataManager()

        try:
            about_info = data_manager.get_about_info()
            education_records = data_manager.get_all_educations()
            experience_records = data_manager.get_all_experiences()
            certification_records = data_manager.get_all_certifications()
        except Exception as e:
            logger.error(f"Error fetching about data: {e}")
            about_info = {}
            education_records = []
            experience_records = []
            certification_records = []

        user = {"username": "admin"}

        context = {
            "request": request,
            "about": about_info,
            "education_records": education_records,
            "experience_records": experience_records,
            "certification_records": certification_records,
            "user": user
        }

        return templates.TemplateResponse("admin/about.html", context)

    except Exception as e:
        logger.error(f"Error rendering admin about: {e}")
        return templates.TemplateResponse("error.html", {
            "request": request,
            "error_message": "Unable to load about data"
        }, status_code=500)

# Education API routes
@router.get("/api/education")
async def get_education_list():
    """Get all education entries."""
    try:
        from app.services.data_manager import DataManager
        data_manager = DataManager()
        education = data_manager.get_all_educations()
        return JSONResponse(content=jsonable_encoder(education))
    except Exception as e:
        logger.error(f"Error fetching education: {e}")
        raise HTTPException(status_code=500, detail="Unable to fetch education data")

@router.post("/api/education")
async def create_education(education: EducationCreate):
    """Create a new education entry."""
    try:
        from app.services.data_manager import DataManager
        data_manager = DataManager()
        new_education = data_manager.create_education(education)
        return JSONResponse(content=jsonable_encoder(new_education))
    except Exception as e:
        logger.error(f"Error creating education: {e}")
        raise HTTPException(status_code=500, detail="Unable to create education")

@router.get("/api/education/{education_id}")
async def get_education(education_id: str):
    """Get a specific education entry."""
    try:
        from app.services.data_manager import DataManager
        data_manager = DataManager()
        education = data_manager.get_education_by_id(education_id)
        if not education:
            raise HTTPException(status_code=404, detail="Education not found")
        return JSONResponse(content=jsonable_encoder(education))
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching education {education_id}: {e}")
        raise HTTPException(status_code=500, detail="Unable to fetch education")

@router.put("/api/education/{education_id}")
async def update_education(education_id: str, education: EducationUpdate):
    """Update an education entry."""
    try:
        from app.services.data_manager import DataManager
        data_manager = DataManager()
        updated_education = data_manager.update_education(education_id, education)
        if not updated_education:
            raise HTTPException(status_code=404, detail="Education not found")
        return JSONResponse(content=jsonable_encoder(updated_education))
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error updating education {education_id}: {e}")
        raise HTTPException(status_code=500, detail="Unable to update education")

@router.delete("/api/education/{education_id}")
async def delete_education(education_id: str):
    """Delete an education entry."""
    try:
        from app.services.data_manager import DataManager
        data_manager = DataManager()
        success = data_manager.delete_education(education_id)
        if not success:
            raise HTTPException(status_code=404, detail="Education not found")
        return JSONResponse(content={"message": "Education deleted successfully"})
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deleting education {education_id}: {e}")
        raise HTTPException(status_code=500, detail="Unable to delete education")

# Experience API routes
@router.get("/api/experience")
async def get_experience_list():
    """Get all experience entries."""
    try:
        from app.services.data_manager import DataManager
        data_manager = DataManager()
        experience = data_manager.get_all_experiences()
        return JSONResponse(content=jsonable_encoder(experience))
    except Exception as e:
        logger.error(f"Error fetching experience: {e}")
        raise HTTPException(status_code=500, detail="Unable to fetch experience data")

@router.post("/api/experience")
async def create_experience(experience: ExperienceCreate):
    """Create a new experience entry."""
    try:
        from app.services.data_manager import DataManager
        data_manager = DataManager()
        new_experience = data_manager.create_experience(experience)
        return JSONResponse(content=jsonable_encoder(new_experience))
    except Exception as e:
        logger.error(f"Error creating experience: {e}")
        raise HTTPException(status_code=500, detail="Unable to create experience")

@router.get("/api/experience/{experience_id}")
async def get_experience(experience_id: str):
    """Get a specific experience entry."""
    try:
        from app.services.data_manager import DataManager
        data_manager = DataManager()
        experience = data_manager.get_experience_by_id(experience_id)
        if not experience:
            raise HTTPException(status_code=404, detail="Experience not found")
        return JSONResponse(content=jsonable_encoder(experience))
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching experience {experience_id}: {e}")
        raise HTTPException(status_code=500, detail="Unable to fetch experience")

@router.put("/api/experience/{experience_id}")
async def update_experience(experience_id: str, experience: ExperienceUpdate):
    """Update an experience entry."""
    try:
        from app.services.data_manager import DataManager
        data_manager = DataManager()
        updated_experience = data_manager.update_experience(experience_id, experience)
        if not updated_experience:
            raise HTTPException(status_code=404, detail="Experience not found")
        return JSONResponse(content=jsonable_encoder(updated_experience))
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error updating experience {experience_id}: {e}")
        raise HTTPException(status_code=500, detail="Unable to update experience")

@router.delete("/api/experience/{experience_id}")
async def delete_experience(experience_id: str):
    """Delete an experience entry."""
    try:
        from app.services.data_manager import DataManager
        data_manager = DataManager()
        success = data_manager.delete_experience(experience_id)
        if not success:
            raise HTTPException(status_code=404, detail="Experience not found")
        return JSONResponse(content={"message": "Experience deleted successfully"})
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deleting experience {experience_id}: {e}")
        raise HTTPException(status_code=500, detail="Unable to delete experience")

# Certification API routes
@router.get("/api/certifications")
async def get_certification_list():
    """Get all certification entries."""
    try:
        from app.services.data_manager import DataManager
        data_manager = DataManager()
        certifications = data_manager.get_all_certifications()
        return JSONResponse(content=jsonable_encoder(certifications))
    except Exception as e:
        logger.error(f"Error fetching certifications: {e}")
        raise HTTPException(status_code=500, detail="Unable to fetch certification data")

@router.post("/api/certifications")
async def create_certification(certification: CertificationCreate):
    """Create a new certification entry."""
    try:
        from app.services.data_manager import DataManager
        data_manager = DataManager()
        new_certification = data_manager.create_certification(certification)
        return JSONResponse(content=jsonable_encoder(new_certification))
    except Exception as e:
        logger.error(f"Error creating certification: {e}")
        raise HTTPException(status_code=500, detail="Unable to create certification")

@router.get("/api/certifications/{certification_id}")
async def get_certification(certification_id: str):
    """Get a specific certification entry."""
    try:
        from app.services.data_manager import DataManager
        data_manager = DataManager()
        certification = data_manager.get_certification_by_id(certification_id)
        if not certification:
            raise HTTPException(status_code=404, detail="Certification not found")
        return JSONResponse(content=jsonable_encoder(certification))
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching certification {certification_id}: {e}")
        raise HTTPException(status_code=500, detail="Unable to fetch certification")

@router.put("/api/certifications/{certification_id}")
async def update_certification(certification_id: str, certification: CertificationUpdate):
    """Update a certification entry."""
    try:
        from app.services.data_manager import DataManager
        data_manager = DataManager()
        updated_certification = data_manager.update_certification(certification_id, certification)
        if not updated_certification:
            raise HTTPException(status_code=404, detail="Certification not found")
        return JSONResponse(content=jsonable_encoder(updated_certification))
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error updating certification {certification_id}: {e}")
        raise HTTPException(status_code=500, detail="Unable to update certification")

@router.delete("/api/certifications/{certification_id}")
async def delete_certification(certification_id: str):
    """Delete a certification entry."""
    try:
        from app.services.data_manager import DataManager
        data_manager = DataManager()
        success = data_manager.delete_certification(certification_id)
        if not success:
            raise HTTPException(status_code=404, detail="Certification not found")
        return JSONResponse(content={"message": "Certification deleted successfully"})
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deleting certification {certification_id}: {e}")
        raise HTTPException(status_code=500, detail="Unable to delete certification")

# Message mark as read route
@router.post("/messages/{message_id}/mark-read")
async def mark_message_read(message_id: str):
    """Mark a message as read."""
    try:
        from app.services.data_manager import DataManager
        from app.models.contact import ContactMessageUpdate

        data_manager = DataManager()
        update_data = ContactMessageUpdate(is_read=True)
        updated_message = data_manager.update_message(message_id, update_data)
        if not updated_message:
            raise HTTPException(status_code=404, detail="Message not found")
        return JSONResponse(content={"message": "Message marked as read"})
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error marking message {message_id} as read: {e}")
        raise HTTPException(status_code=500, detail="Unable to mark message as read")
