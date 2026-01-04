# ResQConnect - Emergency Assistance Platform

## What is this project?

This project presents ResQConnect, a web-based emergency assistance platform aimed at providing timely and critical support during disasters and emergencies. Inspired by modern disaster alert systems and AI-based virtual assistants, ResQConnect combines multiple emergency services into a single, accessible interface. The platform enables users to receive real-time disaster alerts, access first aid information, register emergency complaints, and interact with an AI-powered chatbot for immediate guidance.

Developed using a Flask backend and MongoDB database, the system integrates Gemini AI APIs to enhance the chatbot's responsiveness and relevance. It is designed to assist users during a wide range of emergencies, including natural disasters, medical crises, and roadside incidents. By leveraging artificial intelligence and a user-centric design, ResQConnect ensures rapid response, accurate information delivery, and increased user engagement during critical situations.

## Home Page Screenshot

![ResQConnect Home Page](static/screenshot.png)

## Features

- Real-time disaster alerts
- Emergency complaint registration
- First aid information
- Weather information
- Admin dashboard for managing services
- Responsive UI with Tailwind CSS

## How to run it?

### Prerequisites
- Python 3.8+
- MongoDB

### Local Installation

1. Clone the repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Create a `config.json` file with the following structure:
   ```json
   {
     "params": {
       "mongo_uri": "mongodb://localhost:27017/emergencyDB"
     }
   }
   ```

4. Run the application:
   ```bash
   python main.py
   ```

### Environment Variables

You can also set the following environment variables instead of using config.json:

- `MONGO_URI` - MongoDB connection string
- `SECRET_KEY` - Flask secret key
- `PORT` - Port to run the application on (default: 5000)

### Running in Production

For production deployment, it's recommended to use a WSGI server like Gunicorn:

```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 main:app
```

### Deployment on Render

This project is ready for deployment on Render. Follow these steps:

#### Prerequisites
- A Render account (https://render.com)
- A MongoDB Atlas account or other MongoDB hosting service

#### Deployment Steps

1. Fork this repository to your GitHub account

2. Create a new Web Service on Render:
   - Connect your GitHub account
   - Select your forked repository
   - Choose the branch (usually `main` or `master`)

3. Configure the build:
   - Environment: `Python`
   - Python version: `3.11` (or latest)
   - Build command: `pip install -r requirements.txt`
   - Start command: `gunicorn --bind 0.0.0.0:$PORT wsgi:app`

4. Set environment variables in Render dashboard:
   - `MONGO_URI` - Your MongoDB connection string
   - `SECRET_KEY` - A secure secret key for Flask sessions

5. Click "Create Web Service" and wait for deployment to complete

#### Environment Variables for Render

- `MONGO_URI` (required): Your MongoDB connection string (e.g., `mongodb+srv://username:password@cluster.mongodb.net/emergencyDB`)
- `SECRET_KEY` (required): A random string for Flask session security
- `PORT` (optional): Render automatically sets this, but you can override if needed

#### Render Deployment Configuration

The project includes:
- `Dockerfile` for containerized deployment
- `requirements.txt` with all dependencies
- `wsgi.py` for WSGI server compatibility
- Proper configuration handling for environment variables

#### Important Notes for Render Deployment

1. Make sure your MongoDB connection string is accessible from the internet (if using MongoDB Atlas)
2. The application automatically uses the `PORT` environment variable provided by Render
3. Background tasks (like weather and alert fetching) will run in the deployed environment
4. For production use, ensure your MongoDB database is properly secured and has appropriate indexes