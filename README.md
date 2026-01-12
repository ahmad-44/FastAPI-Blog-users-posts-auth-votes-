# FastAPI Social Media API

A RESTful API built with FastAPI, SQLAlchemy, and PostgreSQL. Features user authentication, posts management, and a voting system.

## Tech Stack

- **FastAPI** - Modern Python web framework
- **PostgreSQL** - Database
- **SQLAlchemy** - ORM
- **Alembic** - Database migrations
- **Pydantic** - Data validation
- **JWT** - Authentication (via PyJWT)
- **Argon2** - Password hashing
- **Docker** - Containerization

## API Endpoints

### Authentication
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/auth/login` | Login and get access token |

### Users
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/users/` | Create a new user |
| GET | `/users/{id}` | Get user by ID |

### Posts
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/posts/` | Get all posts (with pagination & search) |
| GET | `/posts/{id}` | Get a single post |
| POST | `/posts/` | Create a post (auth required) |
| PUT | `/posts/{id}` | Update a post (auth required) |
| DELETE | `/posts/{id}` | Delete a post (auth required) |

### Votes
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/vote/` | Vote/unvote on a post (auth required) |

## Getting Started

### Prerequisites

- Docker and Docker Compose

### Quick Start with Docker

1. **Clone the repository**
   ```bash
   git clone <your-repo-url>
   cd fastapi
   ```

2. **Configure environment variables**
   ```bash
   cp .env.example .env
   # Edit .env with your values
   ```

3. **Start the services**
   ```bash
   docker compose up -d
   ```

4. **Run database migrations**
   ```bash
   docker compose exec api alembic upgrade head
   ```

5. **Access the API**
   - API: http://localhost:8000
   - Swagger Docs: http://localhost:8000/docs
   - ReDoc: http://localhost:8000/redoc

### Environment Variables

| Variable | Description | Example |
|----------|-------------|---------|
| `DATABASE_HOSTNAME` | Database host | `db` (Docker) / `localhost` |
| `DATABASE_PORT` | Database port | `5432` |
| `DATABASE_NAME` | Database name | `fastapi` |
| `DATABASE_USERNAME` | Database user | `postgres` |
| `DATABASE_PASSWORD` | Database password | `your_password` |
| `SECRET_KEY` | JWT secret key | `your_secret_key` |
| `ALGORITHM` | JWT algorithm | `HS256` |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | Token expiry | `30` |

## Docker Commands

```bash
# Start services
docker compose up -d

# View logs
docker compose logs -f api

# Run migrations
docker compose exec api alembic upgrade head

# Create a new migration
docker compose exec api alembic revision --autogenerate -m "description"

# Stop services
docker compose down

# Stop and remove volumes
docker compose down -v
```

## Local Development (without Docker)

1. **Create a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up PostgreSQL** and create a database

4. **Configure `.env`** with your local database credentials

5. **Run migrations**
   ```bash
   alembic upgrade head
   ```

6. **Start the server**
   ```bash
   uvicorn app.main:app --reload
   ```

## Project Structure

```
.
├── app/
│   ├── __init__.py
│   ├── main.py          # FastAPI application
│   ├── config.py        # Settings/environment variables
│   ├── database.py      # Database connection
│   ├── models.py        # SQLAlchemy models
│   ├── schemas.py       # Pydantic schemas
│   ├── oauth2.py        # JWT authentication
│   ├── utils.py         # Utility functions
│   └── routers/
│       ├── auth.py      # Authentication routes
│       ├── user.py      # User routes
│       ├── post.py      # Post routes
│       └── vote.py      # Vote routes
├── alembic/             # Database migrations
├── docker-compose.yml
├── Dockerfile
├── requirements.txt
└── .env.example
```
