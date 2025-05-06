# Event Ticketing Platform

A Django REST API-based event ticketing platform that allows organizers to create and manage events while users can browse and purchase tickets.

## Features

- User Authentication (JWT-based)
- Role-based access (User/Organizer)
- Event Management
- Ticket Management
- Purchase System
- Analytics Dashboard
- Password Reset System
- Swagger Documentation

## Tech Stack

- Django 5.2
- Django REST Framework
- PostgreSQL
- JWT Authentication
- drf-spectacular (Swagger/OpenAPI)

## Prerequisites

- Python 3.8+
- PostgreSQL
- pip (Python package manager)

## Setup Instructions

1. Clone the repository:
```bash
git clone https://github.com/sint18/event-ticketing.git
cd event-ticketing/event_ticketing
```

2. Create and activate a virtual environment:
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/MacOS
python3 -m venv venv
source venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r ../requirements.txt
```

4. Configure PostgreSQL:
   - Create a database named `event_ticketing_db`
   - Update database settings in `event_ticketing/settings.py` if needed:
```python
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "event_ticketing_db",
        "USER": "postgres",
        "PASSWORD": "postgres",
        "HOST": "localhost",
        "PORT": "5432",
    }
}
```

5. Run migrations:
```bash
python manage.py migrate
```

6. Create a superuser:
```bash
python manage.py createsuperuser
```

## Running the Application

1. Start the development server:
```bash
python manage.py runserver
```

2. Access the following URLs:
   - Admin Panel: `http://localhost:8000/admin/`
   - API Documentation: `http://localhost:8000/api/schema/swagger-ui/`
   - API Root: `http://localhost:8000/api/`

## API Documentation

The API documentation is available through Swagger UI at `/api/schema/swagger-ui/`. The endpoints are organized into the following categories:

- Authentication
- Event Management (Organizer)
- Ticket Management (Organizer)
- Event Browsing & Ticket Purchase (User)
- Analytics

## Admin Panel

The Django admin panel provides an interface to manage:
- Users (with role management)
- Events
- Tickets
- Purchases

Access the admin panel at `/admin/` using your superuser credentials.

## Authentication

The platform uses JWT (JSON Web Tokens) for authentication:

1. Register a new user:
```bash
POST /api/register/
```

2. Obtain JWT token:
```bash
POST /api/token/
```

3. Refresh token:
```bash
POST /api/token/refresh/
```

## Development

### Code Style
The project uses `pylint` with Django plugins. A `.pylintrc` file is included in the repository.

### Email Configuration
For development, emails are printed to the console. Update `EMAIL_BACKEND` in settings.py for production:

```python
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
```

## Production Considerations

Before deploying to production:

1. Update `settings.py`:
   - Set `DEBUG = False`
   - Configure `ALLOWED_HOSTS`
   - Update `SECRET_KEY`
   - Configure proper email backend
   - Update `FRONTEND_URL`

2. Set up proper database credentials
3. Configure static files serving
4. Set up proper SSL/TLS certificates
5. Configure proper security middleware

## Author

* **Sint Lwin Htoo / sint18**
    * [My Portfolio - sinthtoo.com](https://www.sinthtoo.com/)
    * [https://github.com/sint18](https://github.com/sint18)
    * [https://www.linkedin.com/in/sintlwinhtoo/](https://www.linkedin.com/in/sintlwinhtoo/)
    * [sintlwinhtoo.slh@gmail.com](mailto:your.email@example.com)