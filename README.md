# Profile Management System - Backend

A secure RESTful API built with FastAPI for user profile management with JWT authentication.

## Tech Stack

- **Framework**: FastAPI 0.123.0
- **Database**: MySQL with SQLAlchemy ORM
- **Authentication**: JWT (JSON Web Tokens)
- **Password Hashing**: Bcrypt
- **Migrations**: Alembic
- **Validation**: Pydantic

## Features

- ✅ User registration with secure password hashing
- ✅ JWT-based authentication
- ✅ Protected profile endpoints
- ✅ Profile management (view, update, soft delete)
- ✅ Input validation with Pydantic
- ✅ Database migrations with Alembic
- ✅ Interactive API documentation (Swagger UI)
- ✅ CORS enabled for cross-origin requests

## Project Structure
```
backend/
├── app/
│   ├── models/
│   │   └── user.py          # SQLAlchemy User model
│   ├── schemas/
│   │   ├── auth.py          # Pydantic schemas for authentication
│   │   └── profile.py       # Pydantic schemas for profile
│   ├── routers/
│   │   ├── auth.py          # Authentication endpoints
│   │   └── profile.py       # Profile endpoints
│   ├── utils/
│   │   ├── auth.py          # JWT token utilities
│   │   └── security.py      # Password hashing utilities
│   ├── config.py            # Configuration settings
│   ├── database.py          # Database connection
│   ├── dependencies.py      # FastAPI dependencies
│   └── app.py               # Main application
├── alembic/
│   └── versions/            # Database migrations
├── .env                     # Environment variables (not in repo)
├── .gitignore
├── requirements.txt
└── README.md
```

## Setup Instructions

### Prerequisites

- Python 3.10+
- MySQL 8.0+
- pip (Python package manager)

### 1. Clone the Repository
```bash
git clone https://github.com/YOUR_USERNAME/profile-management-backend.git
cd profile-management-backend
```

### 2. Create Virtual Environment
```bash
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate

# macOS/Linux:
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Setup MySQL Database
```bash
# Login to MySQL
mysql -u root -p

# Create database
CREATE DATABASE profile_management;
EXIT;
```

### 5. Configure Environment Variables

Create a `.env` file in the backend directory:
```env
DATABASE_URL=mysql+pymysql://root:YOUR_PASSWORD@localhost:3306/profile_management
JWT_SECRET_KEY=your-super-secret-key-change-in-production
```

**Important**: Replace `YOUR_PASSWORD` with your MySQL password. If your password contains special characters like `@`, URL-encode them (e.g., `@` becomes `%40`).

### 6. Run Database Migrations
```bash
alembic upgrade head
```

This creates the `users` table in your database.

### 7. Start the Server
```bash
uvicorn app.app:app --reload
```

The API will be available at: `http://localhost:8000`

## API Documentation

Once the server is running, visit:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## API Endpoints

### Authentication

#### POST /auth/signup
Register a new user.

**Request Body:**
```json
{
  "email": "user@example.com",
  "password": "securepassword123",
  "name": "John Doe"
}
```

**Response:**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

#### POST /auth/login
Authenticate an existing user.

**Request Body:**
```json
{
  "email": "user@example.com",
  "password": "securepassword123"
}
```

**Response:**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

### Profile (Protected Routes)

All profile endpoints require authentication. Include the JWT token in the Authorization header:
```
Authorization: Bearer <your_token_here>
```

#### GET /profile/me
Get current user's profile.

**Response:**
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "email": "user@example.com",
  "name": "John Doe",
  "bio": "Software Developer"
}
```

#### PUT /profile/me
Update current user's profile.

**Request Body:**
```json
{
  "name": "Jane Doe",
  "bio": "Full Stack Developer"
}
```

**Response:**
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "email": "user@example.com",
  "name": "Jane Doe",
  "bio": "Full Stack Developer"
}
```

#### DELETE /profile/me
Soft delete current user's profile.

**Response:**
```json
{
  "message": "Profile deleted successfully"
}
```

## Security Features

- **Password Hashing**: Bcrypt with salt for secure password storage
- **JWT Authentication**: Stateless authentication with 30-minute token expiry
- **Input Validation**: Pydantic schemas validate all incoming data
- **SQL Injection Prevention**: SQLAlchemy ORM prevents SQL injection attacks
- **CORS**: Configured to allow cross-origin requests from frontend

## Logging

The application implements comprehensive logging:

- **Console Logs**: Real-time logs visible in terminal
- **File Logs**: Stored in `logs/` directory
  - `app_YYYYMMDD.log` - All logs (DEBUG, INFO, WARNING, ERROR)
  - `error_YYYYMMDD.log` - Error logs only
- **Log Rotation**: New log files created daily

### View Logs
```bash
# View today's logs
cat logs/app_$(date +%Y%m%d).log

# View errors only
cat logs/error_$(date +%Y%m%d).log

# Real-time log monitoring
tail -f logs/app_$(date +%Y%m%d).log
```

### Log Levels

- **DEBUG**: Detailed diagnostic information
- **INFO**: General informational messages
- **WARNING**: Warning messages
- **ERROR**: Error messages and stack traces

## Database Schema

### Users Table

| Column   | Type         | Constraints                    |
|----------|--------------|--------------------------------|
| id       | CHAR(36)     | PRIMARY KEY (UUID)             |
| email    | VARCHAR(255) | UNIQUE, NOT NULL, INDEXED      |
| password | VARCHAR(255) | NOT NULL (bcrypt hashed)       |
| name     | VARCHAR(255) | NULLABLE                       |
| bio      | TEXT         | NULLABLE                       |

## Development

### Create New Migration

After modifying models:
```bash
alembic revision --autogenerate -m "description of changes"
alembic upgrade head
```

### Run Tests
```bash
# Install pytest
pip install pytest pytest-asyncio httpx

# Run tests
pytest
```

## Troubleshooting

### MySQL Connection Error

If you get "Can't connect to MySQL server":
- Verify MySQL is running
- Check credentials in `.env` file
- Ensure database exists: `CREATE DATABASE profile_management;`

### Import Errors

If you get module import errors:
- Ensure virtual environment is activated
- Reinstall dependencies: `pip install -r requirements.txt`

### Alembic Migration Errors

If migrations fail:
- Check database connection in `.env`
- Verify Alembic configuration in `alembic/env.py`
- Drop and recreate database if needed (development only)

## Time Spent

**Estimated Development Time: 6-8 hours**

- Project setup and configuration: 1 hour
- Database models and migrations: 1 hour
- Authentication endpoints (signup, login): 1.5 hours
- Profile endpoints (CRUD operations): 1.5 hours
- JWT implementation and security: 1 hour
- Testing and debugging: 1-2 hours
- Documentation: 1 hour

## Future Improvements

- [ ] Add refresh tokens for extended sessions
- [ ] Implement email verification
- [ ] Add password reset functionality
- [ ] Rate limiting for API endpoints
- [ ] Comprehensive unit and integration tests
- [ ] Docker containerization
- [ ] CI/CD pipeline

## Author

Sahil Koshti - [GitHub Profile](https://github.com/SupRaKoshti)

## License

This project is part of the GenAI Engineering Accelerator assessment.
