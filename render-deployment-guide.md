# ResQConnect - Render Deployment Guide

This guide provides detailed instructions for deploying the ResQConnect emergency assistance platform on Render.

## Overview

ResQConnect is a Flask-based emergency assistance platform that provides real-time disaster alerts, emergency complaint registration, first aid information, and weather information. The application is designed to be easily deployable on Render with minimal configuration.

## Prerequisites

- A Render account (sign up at https://render.com)
- A MongoDB Atlas account or other accessible MongoDB hosting service
- A GitHub account with the repository forked

## Step-by-Step Deployment Guide

### 1. Prepare Your Repository

1. Fork the ResQConnect repository to your GitHub account
2. Ensure all dependencies are listed in `requirements.txt`
3. Verify that the `wsgi.py` file is properly configured for WSGI deployment
4. Confirm that environment variable configuration is working in `main.py`

### 2. Set Up MongoDB

1. Create an account at [MongoDB Atlas](https://www.mongodb.com/atlas) or use another MongoDB hosting service
2. Create a new cluster and database
3. Set up database access with a username and password
4. Configure network access to allow connections from anywhere (0.0.0.0/0) or specifically from Render's IP ranges
5. Get your connection string in the format: `mongodb+srv://<username>:<password>@<cluster-name>.mongodb.net/<database-name>`

### 3. Create Render Web Service

1. Log in to your Render dashboard
2. Click "New +" and select "Web Service"
3. Connect your GitHub account and select your forked repository
4. Choose the branch you want to deploy (typically `main` or `master`)

### 4. Configure Environment Variables

Before creating the service, you'll need to set the following environment variables:

- `MONGO_URI` (required): Your MongoDB connection string from step 2
- `SECRET_KEY` (required): A secure random string for Flask session management
- `PORT` (optional): Render automatically sets this, but you can override if needed

### 5. Configure Build Settings

- **Environment**: Python
- **Runtime**: Choose the latest Python version (3.11 or higher recommended)
- **Build Command**: `pip install -r requirements.txt`
- **Start Command**: `gunicorn --bind 0.0.0.0:$PORT wsgi:app`

### 6. Deploy

1. Review your settings
2. Click "Create Web Service"
3. Wait for the build and deployment to complete (this may take a few minutes)
4. Once complete, your application will be available at the URL provided by Render

## Configuration Details

### Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `MONGO_URI` | Yes | MongoDB connection string |
| `SECRET_KEY` | Yes | Flask secret key for session security |
| `PORT` | No | Port to run the application on (Render sets this automatically) |

### Render-Specific Configuration

The application is already configured for Render deployment:

- The `wsgi.py` file provides WSGI compatibility
- The `main.py` file reads the `PORT` environment variable
- Background scheduler in `main.py` is configured to work in Render environment
- Error handling is implemented for various deployment scenarios

## Post-Deployment Steps

1. Visit your deployed application URL
2. Test all functionality including:
   - Home page loading
   - Complaint submission
   - Weather and alerts display
   - Admin panel (with default credentials: Admin/1234)
3. Verify that MongoDB is connecting properly by checking complaint submissions
4. Set up custom domain if desired

## Troubleshooting

### Common Issues

**Application fails to start:**
- Check that `MONGO_URI` is properly set and accessible
- Verify MongoDB connection string format
- Ensure all required environment variables are set

**Background tasks not running:**
- The application uses APScheduler for background tasks
- These should run automatically in the Render environment
- Check application logs for any scheduler errors

**Database connection issues:**
- Verify MongoDB network access settings allow connections from Render
- Ensure the connection string is properly URL-encoded if it contains special characters
- Check that the database user has proper permissions

### Checking Logs

You can view application logs in the Render dashboard under your web service to troubleshoot issues.

## Scaling Recommendations

- For basic usage, the free tier should be sufficient
- For production use, consider upgrading to a starter or professional instance
- Monitor your application's resource usage and scale accordingly

## Security Considerations

- Change the default admin credentials after deployment
- Use a strong, unique `SECRET_KEY` environment variable
- Ensure your MongoDB database is properly secured
- Regularly update dependencies listed in `requirements.txt`

## Updating Your Deployment

When you push changes to your GitHub repository, Render will automatically rebuild and redeploy your application. You can disable auto-deploys in the Render dashboard if you prefer manual deployments.

## Support

If you encounter issues with deployment, check the Render dashboard logs first. For application-specific issues, refer to the main README or open an issue in the repository.