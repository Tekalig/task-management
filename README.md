# Task Management REST API

A secure, production-ready **Task Management REST API** built with **FastAPI**, **MySQL**, and **SQLAlchemy**.

## Features

- User registration and login with **JWT** authentication
- Full **CRUD** operations for tasks (Create, Read, Update, Delete)
- Password hashing with **bcrypt**
- **CORS** middleware support
- Clean, modular project structure with separated routers, services, models, and schemas

## Project Structure

```
task-management/
├── app/
│   ├── core/
│   │   ├── config.py        # Environment configuration (pydantic-settings)
│   │   └── security.py      # Password hashing & JWT token utilities
│   ├── db/
│   │   └── database.py      # SQLAlchemy engine & session dependency
│   ├── models/
│   │   ├── user.py          # User ORM model
│   │   └── task.py          # Task ORM model
│   ├── routers/
│   │   ├── auth.py          # /auth/register and /auth/login endpoints
│   │   └── tasks.py         # /tasks CRUD endpoints (JWT protected)
│   ├── schemas/
│   │   ├── user.py          # User Pydantic schemas
│   │   └── task.py          # Task Pydantic schemas
│   └── services/
│       ├── auth_service.py  # Authentication business logic
│       └── task_service.py  # Task business logic
├── main.py                  # FastAPI app entry point
├── migration.sql            # MySQL DDL to create tables
├── requirements.txt
├── .env.example             # Example environment variables
└── README.md
```

## Getting Started

### Prerequisites

- Python 3.10+
- MySQL 8.0+

### Installation

1. **Clone the repository**

   ```bash
   git clone https://github.com/Tekalig/task-management.git
   cd task-management
   ```

2. **Create a virtual environment and install dependencies**

   ```bash
   python -m venv venv
   source venv/bin/activate   # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. **Set up environment variables**

   ```bash
   cp .env.example .env
   # Edit .env with your MySQL credentials and a strong SECRET_KEY
   ```

4. **Set up the MySQL database**

   ```bash
   mysql -u root -p < migration.sql
   ```

5. **Run the application**

   ```bash
   uvicorn main:app --reload
   ```

   The API will be available at `http://localhost:8000`.  
   Interactive docs: `http://localhost:8000/docs`

## API Endpoints

### Authentication

| Method | Endpoint             | Description               |
|--------|----------------------|---------------------------|
| POST   | `/auth/register`     | Register a new user       |
| POST   | `/auth/login`        | Login and receive JWT     |

### Tasks (JWT required)

| Method | Endpoint             | Description               |
|--------|----------------------|---------------------------|
| GET    | `/tasks/`            | List all tasks for the user |
| POST   | `/tasks/`            | Create a new task         |
| GET    | `/tasks/{task_id}`   | Get a task by ID          |
| PUT    | `/tasks/{task_id}`   | Update a task             |
| DELETE | `/tasks/{task_id}`   | Delete a task             |

## Environment Variables

| Variable                    | Description                             | Default  |
|-----------------------------|-----------------------------------------|----------|
| `DATABASE_URL`              | MySQL connection string                 | —        |
| `SECRET_KEY`                | JWT signing secret (keep this secure!)  | —        |
| `ALGORITHM`                 | JWT algorithm                           | `HS256`  |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | Token lifetime in minutes             | `30`     |

## Security Notes

- Never commit your `.env` file — it is listed in `.gitignore`.
- Generate a strong `SECRET_KEY` with: `openssl rand -hex 32`
- All task endpoints require a valid `Authorization: Bearer <token>` header.