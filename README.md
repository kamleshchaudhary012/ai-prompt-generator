# AI Prompt Generator - Django Edition

A modern web application for generating effective AI prompts with smart topic suggestions based on categories.

## Features

- Generate ready-to-use prompts for different AI platforms
- Keyword suggestions based on selected category
- Support for multiple categories:
  - ChatGPT
  - Midjourney (AI Art)
  - Blogging/SEO
  - Coding
  - Social Media
- Trending topics section showing popular searches
- Copy-to-clipboard functionality
- Mobile responsive design
- Clean, intuitive user interface
- Django backend with database for prompts and keyword suggestions
- Production-ready configuration for easy deployment

## Tech Stack

- Django (Backend)
- PostgreSQL (Production Database)
- SQLite (Development Database)
- HTML5
- Tailwind CSS
- JavaScript (Fetch API for AJAX)
- Font Awesome for icons
- Gunicorn (WSGI HTTP Server)
- Whitenoise (Static Files Serving)

## Getting Started (Development)

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/ai-prompt-generator.git
   ```

2. Navigate to the project directory:
   ```
   cd ai-prompt-generator
   ```

3. Create a virtual environment:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

4. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

5. Copy the example environment file:
   ```
   cp .env.example .env
   ```

6. Edit the `.env` file with your development settings:
   ```
   SECRET_KEY=your-dev-secret-key
   DEBUG=True
   ALLOWED_HOSTS=localhost,127.0.0.1
   ```

7. Run database migrations:
   ```
   python manage.py migrate
   ```

8. Load initial data:
   ```
   python manage.py load_initial_data
   ```

9. Run the development server:
   ```
   python manage.py runserver
   ```

10. Visit `http://127.0.0.1:8000/` in your web browser

## Deployment to Production

See [DEPLOYMENT.md](DEPLOYMENT.md) for detailed instructions on deploying to:

- Heroku
- DigitalOcean App Platform
- AWS or other VPS

## Project Structure

```
ai-prompt-generator/
├── prompt_generator/       # Main Django project
├── generator/              # Django app
│   ├── models.py           # Database models
│   ├── views.py            # API endpoints and views
│   ├── urls.py             # URL routing
│   └── management/         # Management commands
├── templates/              # HTML templates
│   └── home.html           # Main page template
├── static/                 # Static files
│   ├── css/                # CSS styles
│   └── js/                 # JavaScript files
└── manage.py               # Django management script
```

## Features in Detail

### Smart Keyword Suggestions

As you type in the topic field, the application will suggest popular keywords related to the selected category. This helps users discover relevant topics and improves the quality of generated prompts.

### Dynamic Category Selection

The application provides different prompt templates based on the selected category, ensuring that the generated prompts are tailored to the specific use case.

### Persistent Data Storage

All user interactions contribute to improving the suggestion system. When users generate prompts for a topic, the system records the topic's popularity, which enhances future keyword suggestions.

## License

MIT

## Contact

Your Name - your.email@example.com

Project Link: [https://github.com/yourusername/ai-prompt-generator](https://github.com/yourusername/ai-prompt-generator) 