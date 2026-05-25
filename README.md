# Photo Album Management System

A production-ready Photo Album Management web application built with Django, Cloudinary, and PostgreSQL, deployed on Render.

## Live Demo
[https://your-app-name.onrender.com](https://your-app-name.onrender.com)

## Features
- User authentication (login/logout)
- Role-Based Access Control (RBAC) — only album owners can edit or delete their own albums and photos
- Create, view, edit, and delete photo albums
- Upload photos to albums via Cloudinary cloud storage
- Search albums by name or description
- Paginated album listing
- Admin panel for superusers

## Tech Stack
- **Framework:** Django 6.x (Python)
- **Database:** PostgreSQL (via Render) / SQLite (local development)
- **Media Storage:** Cloudinary
- **Static Files:** WhiteNoise
- **Deployment:** Render

## Project Structure
cloud-render/
├── gallery/
│   ├── migrations/
│   ├── templates/gallery/
│   ├── admin.py
│   ├── forms.py
│   ├── models.py
│   ├── urls.py
│   └── views.py
├── recipe_project/
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── build.sh
├── manage.py
├── requirements.txt
└── README.md
## Local Setup

### 1. Clone the repository
```bash
git clone https://github.com/Kristianjayl/photo-album-django.git
cd photo-album-django
```

### 2. Create and activate virtual environment
```bash
python -m venv venv
venv\Scripts\activate   # Windows
# or: source venv/bin/activate  (Mac/Linux)
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Create a `.env` file in the project root
```env
SECRET_KEY=your-secret-key
DEBUG=True
CLOUDINARY_CLOUD_NAME=your-cloud-name
CLOUDINARY_API_KEY=your-api-key
CLOUDINARY_API_SECRET=your-api-secret
```

### 5. Run migrations and create superuser
```bash
python manage.py migrate
python manage.py createsuperuser
```

### 6. Start the server
```bash
python manage.py runserver
```

## Deployment (Render)

### Environment Variables to set in Render:
| Variable | Value |
|---|---|
| `SECRET_KEY` | Your Django secret key |
| `DEBUG` | `False` |
| `DATABASE_URL` | Provided by Render PostgreSQL |
| `CLOUDINARY_CLOUD_NAME` | Your Cloudinary cloud name |
| `CLOUDINARY_API_KEY` | Your Cloudinary API key |
| `CLOUDINARY_API_SECRET` | Your Cloudinary API secret |
| `DJANGO_SUPERUSER_USERNAME` | Admin username |
| `DJANGO_SUPERUSER_EMAIL` | Admin email |
| `DJANGO_SUPERUSER_PASSWORD` | Admin password |

### Build Command
`./build.sh`
### Start Command
`gunicorn recipe_project.wsgi:application`
## RBAC — Role Summary
| Action | Regular User | Album Owner | Staff/Admin |
|---|---|---|---|
| View albums | ✅ | ✅ | ✅ |
| Create album | ✅ | ✅ | ✅ |
| Edit own album | ❌ | ✅ | ✅ |
| Delete own album | ❌ | ✅ | ✅ |
| Add photo to own album | ❌ | ✅ | ✅ |
| Edit/delete any album | ❌ | ❌ | ✅ |

## Author
Christian Jile C. Balladares - IT383/BSIT-3A