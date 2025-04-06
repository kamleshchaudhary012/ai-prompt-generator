# AI Prompt Generator - Deployment Guide

This guide provides instructions for deploying the AI Prompt Generator application to a production environment.

## Prerequisites

- Python 3.8 or higher
- PostgreSQL database
- A production server (Heroku, AWS, DigitalOcean, etc.)
- Git

## Local Preparation

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/ai-prompt-generator.git
   cd ai-prompt-generator
   ```

2. Create a virtual environment:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

4. Create a `.env` file based on `.env.example`:
   ```
   cp .env.example .env
   ```

5. Generate a secure secret key:
   ```python
   python -c "import secrets; print(secrets.token_urlsafe(50))"
   ```

6. Edit the `.env` file with your production settings:
   ```
   SECRET_KEY=your-generated-secret-key
   DEBUG=False
   ALLOWED_HOSTS=your-domain.com,www.your-domain.com
   DATABASE_URL=postgres://user:password@localhost/dbname
   ```

## Deployment to Heroku

1. Install the Heroku CLI and log in:
   ```
   heroku login
   ```

2. Create a new Heroku app:
   ```
   heroku create your-app-name
   ```

3. Add PostgreSQL addon:
   ```
   heroku addons:create heroku-postgresql:mini
   ```

4. Configure environment variables:
   ```
   heroku config:set SECRET_KEY=your-generated-secret-key
   heroku config:set DEBUG=False
   heroku config:set ALLOWED_HOSTS=your-app-name.herokuapp.com
   ```

5. Push to Heroku:
   ```
   git push heroku main
   ```

6. The release command in the Procfile will automatically run migrations and load initial data.

## Deployment to DigitalOcean App Platform

1. Create a new app on DigitalOcean App Platform.

2. Connect your GitHub repository.

3. Set the following environment variables:
   - `SECRET_KEY`
   - `DEBUG=False`
   - `ALLOWED_HOSTS` (comma-separated list of domains)

4. Add a PostgreSQL database component.

5. Set the build command to:
   ```
   pip install -r requirements.txt && python manage.py collectstatic --noinput
   ```

6. Set the run command to:
   ```
   gunicorn prompt_generator.wsgi
   ```

7. Deploy your app.

## Deployment to AWS or other VPS

1. Set up a Ubuntu server with Python and PostgreSQL.

2. Install Nginx as a reverse proxy:
   ```
   sudo apt-get update
   sudo apt-get install nginx
   ```

3. Configure Nginx to proxy to Gunicorn:
   ```
   server {
       listen 80;
       server_name your-domain.com;
       
       location /static/ {
           alias /path/to/your/app/staticfiles/;
       }
       
       location / {
           proxy_pass http://127.0.0.1:8000;
           proxy_set_header Host $host;
           proxy_set_header X-Real-IP $remote_addr;
       }
   }
   ```

4. Set up your application:
   ```
   git clone https://github.com/yourusername/ai-prompt-generator.git
   cd ai-prompt-generator
   python -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

5. Create and configure `.env` file.

6. Set up a systemd service to keep the application running:
   ```
   [Unit]
   Description=AI Prompt Generator
   After=network.target
   
   [Service]
   User=your-user
   Group=your-group
   WorkingDirectory=/path/to/your/app
   ExecStart=/path/to/your/app/venv/bin/gunicorn prompt_generator.wsgi:application --bind 127.0.0.1:8000
   Restart=always
   
   [Install]
   WantedBy=multi-user.target
   ```

7. Start the service:
   ```
   sudo systemctl enable ai-prompt-generator
   sudo systemctl start ai-prompt-generator
   ```

## Post-Deployment Tasks

1. Test the application thoroughly.

2. Set up monitoring (e.g., Sentry for error tracking).

3. Configure backups for your database.

4. Set up SSL certificates (e.g., using Let's Encrypt).

## Troubleshooting

- **Static files not showing**: Run `python manage.py collectstatic` and ensure your web server is configured to serve files from STATIC_ROOT.

- **Database connection issues**: Verify that the DATABASE_URL is correct and the database server is accessible.

- **500 errors**: Check the application logs for details.

- **Migration errors**: Try running `python manage.py migrate` manually.

For more help, please open an issue on the project's GitHub repository. 