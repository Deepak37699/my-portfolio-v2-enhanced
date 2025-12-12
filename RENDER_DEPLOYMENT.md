# Render Deployment Guide

## Deployment Configuration

- Created `render.yaml` with production settings
- Configured Python 3.9.13 runtime
- Set PORT environment variable to 8000
- Gunicorn as production server

## Deployment Steps

1. Push code to GitHub repository
2. Create new Web Service on Render dashboard
3. Connect GitHub repository
4. Render will automatically detect `render.yaml`
5. Confirm environment variables match `.env.production`
6. Deploy!

## Post-Deployment

- Verify application at provided Render URL
- Update DNS settings if using custom domain
- Monitor logs in Render dashboard
