from fastapi import APIRouter, Request, Form, HTTPException, Depends
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from typing import Optional
import logging

from app.services.data_manager import DataManager
from app.models.contact import ContactMessageCreate

logger = logging.getLogger(__name__)

router = APIRouter()
data_manager = DataManager()


def get_templates(request: Request) -> Jinja2Templates:
    """Get templates from app state."""
    return request.app.state.templates


@router.get("/", response_class=HTMLResponse)
async def home(request: Request, templates: Jinja2Templates = Depends(get_templates)):
    """Home page displaying featured projects and key information."""
    try:
        # Get data with error handling
        try:
            all_projects = data_manager.get_all_projects()
            featured_projects = [p for p in all_projects if p.featured][:3]  # Show top 3 featured
        except Exception as e:
            logger.error(f"Error loading projects: {e}")
            featured_projects = []
            
        try:
            all_skills = data_manager.get_all_skills()
            top_skills = sorted(all_skills, key=lambda x: x.proficiency, reverse=True)[:6]
        except Exception as e:
            logger.error(f"Error loading skills: {e}")
            top_skills = []
            
        try:
            about_info = data_manager.get_about_info()
        except Exception as e:
            logger.error(f"Error loading about info: {e}")
            about_info = None
        
        return templates.TemplateResponse("index.html", {
            "request": request,
            "featured_projects": featured_projects,
            "top_skills": top_skills,
            "about": about_info,
            "page_title": "Home"
        })
    except Exception as e:
        logger.error(f"Error rendering home page: {e}")
        return templates.TemplateResponse("error.html", {
            "request": request,
            "error_message": "Unable to load home page content"
        }, status_code=500)


@router.get("/about", response_class=HTMLResponse)
async def about(request: Request, templates: Jinja2Templates = Depends(get_templates)):
    """About page with detailed information."""
    try:
        # Get about info with error handling
        try:
            about_info = data_manager.get_about_info()
        except Exception as e:
            logger.error(f"Error loading about info: {e}")
            about_info = None
            
        # Get skills with error handling
        try:
            all_skills = data_manager.get_all_skills()
        except Exception as e:
            logger.error(f"Error loading skills: {e}")
            all_skills = []
            
        # Group skills by category
        skills_by_category = {}
        for skill in all_skills:
            category = skill.category
            if category not in skills_by_category:
                skills_by_category[category] = []
            skills_by_category[category].append(skill)
        
        return templates.TemplateResponse("about.html", {
            "request": request,
            "about": about_info,
            "skills_by_category": skills_by_category,
            "page_title": "About"
        })
    except Exception as e:
        logger.error(f"Error rendering about page: {e}")
        return templates.TemplateResponse("error.html", {
            "request": request,
            "error_message": "Unable to load about page content"
        }, status_code=500)


@router.get("/projects", response_class=HTMLResponse)
async def projects(request: Request, templates: Jinja2Templates = Depends(get_templates)):
    """Projects page displaying all projects."""
    try:
        all_projects = data_manager.get_all_projects()
        
        # Sort projects by creation date (newest first)
        sorted_projects = sorted(all_projects, key=lambda x: x.created_date, reverse=True)
        
        return templates.TemplateResponse("projects.html", {
            "request": request,
            "projects": sorted_projects,
            "page_title": "Projects"
        })
    except Exception as e:
        logger.error(f"Error loading projects page: {e}")
        raise HTTPException(status_code=500, detail="Error loading projects page")


@router.get("/skills", response_class=HTMLResponse)
async def skills(request: Request, templates: Jinja2Templates = Depends(get_templates)):
    """Skills page displaying all skills organized by category."""
    try:
        all_skills = data_manager.get_all_skills()
        
        # Group skills by category and sort by proficiency
        skills_by_category = {}
        for skill in all_skills:
            category = skill.category
            if category not in skills_by_category:
                skills_by_category[category] = []
            skills_by_category[category].append(skill)
        
        # Sort skills within each category by proficiency
        for category in skills_by_category:
            skills_by_category[category].sort(key=lambda x: x.proficiency, reverse=True)
        
        return templates.TemplateResponse("skills.html", {
            "request": request,
            "skills": all_skills,  # Add the flat list that the template expects
            "skills_by_category": skills_by_category,
            "page_title": "Skills"
        })
    except Exception as e:
        logger.error(f"Error loading skills page: {e}")
        raise HTTPException(status_code=500, detail="Error loading skills page")


@router.get("/contact", response_class=HTMLResponse, name="contact")
async def contact_get(request: Request, templates: Jinja2Templates = Depends(get_templates)):
    """Contact page with contact form."""
    try:
        about_info = data_manager.get_about_info()
        
        return templates.TemplateResponse("contact.html", {
            "request": request,
            "about": about_info,
            "page_title": "Contact",
            "success_message": request.query_params.get("success"),
            "error_message": request.query_params.get("error")
        })
    except Exception as e:
        logger.error(f"Error loading contact page: {e}")
        raise HTTPException(status_code=500, detail="Error loading contact page")


@router.post("/contact", response_class=HTMLResponse)
async def contact_post(
    request: Request,
    name: str = Form(...),
    email: str = Form(...),
    subject: str = Form(...),
    message: str = Form(...),
    templates: Jinja2Templates = Depends(get_templates)
):
    """Handle contact form submission."""
    try:
        # Create contact message
        message_data = ContactMessageCreate(
            name=name.strip(),
            email=email.strip(),
            subject=subject.strip(),
            message=message.strip()
        )
        
        # Save message
        new_message = data_manager.create_message(message_data)
        
        logger.info(f"New contact message from {email}")
        
        # Redirect with success message
        return RedirectResponse(
            url="/contact?success=Thank you for your message! I'll get back to you soon.",
            status_code=303
        )
        
    except Exception as e:
        logger.error(f"Error submitting contact form: {e}")
        return RedirectResponse(
            url="/contact?error=Sorry, there was an error sending your message. Please try again.",
            status_code=303
        )


# API endpoints for frontend frameworks (if needed)
@router.get("/api/projects")
async def api_get_projects():
    """API endpoint to get all projects."""
    try:
        projects = data_manager.get_all_projects()
        return {"projects": [project.dict() for project in projects]}
    except Exception as e:
        logger.error(f"Error in API get projects: {e}")
        raise HTTPException(status_code=500, detail="Error fetching projects")


@router.get("/api/skills")
async def api_get_skills():
    """API endpoint to get all skills."""
    try:
        skills = data_manager.get_all_skills()
        return {"skills": [skill.dict() for skill in skills]}
    except Exception as e:
        logger.error(f"Error in API get skills: {e}")
        raise HTTPException(status_code=500, detail="Error fetching skills")


@router.get("/api/about")
async def api_get_about():
    """API endpoint to get about information."""
    try:
        about = data_manager.get_about_info()
        return {"about": about.dict() if about else None}
    except Exception as e:
        logger.error(f"Error in API get about: {e}")
        raise HTTPException(status_code=500, detail="Error fetching about info")


@router.post("/api/contact")
async def api_contact(message_data: ContactMessageCreate):
    """API endpoint for contact form submission."""
    try:
        new_message = data_manager.create_message(message_data)
        logger.info(f"New contact message from {message_data.email}")
        return {"message": "Message sent successfully", "id": new_message.id}
    except Exception as e:
        logger.error(f"Error in API contact: {e}")
        raise HTTPException(status_code=500, detail="Error sending message")
