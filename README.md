# BaseAPI 🚀

<div align="center">

![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)
![Python](https://img.shields.io/badge/Python-3.8+-blue?style=for-the-badge&logo=python)
![MySQL](https://img.shields.io/badge/MySQL-8.0+-4479A1?style=for-the-badge&logo=mysql&logoColor=white)
![Redis](https://img.shields.io/badge/Redis-6.0+-DC382D?style=for-the-badge&logo=redis&logoColor=white)
![Celery](https://img.shields.io/badge/Celery-37814A?style=for-the-badge&logo=celery&logoColor=white)

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=for-the-badge)](https://opensource.org/licenses/MIT)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg?style=for-the-badge)](http://makeapullrequest.com)

</div>

## 📝 Overview

BaseAPI is a modern, scalable backend framework built with FastAPI, designed for rapid development of production-grade applications. It includes built-in user authentication, asynchronous task processing with Celery, and MySQL database integration — making it ideal for applications that require performance, extensibility, and clean architecture from day one.

## ✨ Key Features

<div align="center">

| Feature | Description |
|:--------|:------------|
| 🔐 **Authentication** | JWT-based user authentication with session management |
| ⚙️ **Task Processing** | Background tasks with Celery + Redis |
| 🗃️ **Database** | MySQL support with SQLAlchemy/SQLModel |
| 📦 **Architecture** | Modular, production-ready project structure |
| 🔧 **Configuration** | Environment-based configuration for flexibility |
| 📈 **Scalability** | Ready for Docker/Kubernetes environments |

</div>

## 🏗️ Project Structure

```bash
baseapi/
├── backend/
│   ├── alembic/              # Database migrations
│   ├── controllers/          # API route handlers
│   │   ├── base.py          # Base routes
│   │   └── user/            # User-related routes
│   ├── core/                # Core functionality
│   │   ├── celery_app.py    # Celery configuration
│   │   ├── init_db.py       # Database initialization
│   │   └── utils.py         # Utility functions
│   ├── models/              # SQLAlchemy models
│   │   ├── user.py         # User model
│   │   ├── password_reset.py # Password reset model
│   │   └── session.py      # Session model
│   ├── tasks/               # Celery tasks
│   │   └── email_tasks.py  # Email-related tasks
│   ├── .env                 # Environment variables
│   ├── app.py              # FastAPI application
│   ├── requirements.txt    # Python dependencies
│   └── Makefile           # Build automation
└── README.md              # Project documentation
```

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- MySQL 8.0+
- Redis 6.0+
- Make (for build automation)

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/yourusername/baseapi.git
cd baseapi
```

2. **Set up virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
cd backend
make install
```

4. **Configure environment**
```bash
cp .env.example .env
# Edit .env with your configuration
```

## ⚙️ Configuration

Create a `.env` file in the backend directory:

```env
# Database Configuration
DB_HOST=localhost
DB_PORT=3306
DB_USER=your_user
DB_PASSWORD=your_password
DB_NAME=baseapi

# Server Configuration
HOST=0.0.0.0
PORT=8000

# CORS Configuration
CORS_ORIGINS=["*"]
CORS_CREDENTIALS=true
CORS_METHODS=["*"]
CORS_HEADERS=["*"]

# Celery Configuration
CELERY_BROKER_URL=redis://localhost:6379/0
CELERY_RESULT_BACKEND=redis://localhost:6379/0
```

## 🛠️ Usage

### Development

```bash
# Start development server
make start

# Run database migrations
make migrate

# Start Celery worker
make celery

# Start Celery beat
make celery-beat
```

### API Documentation

Once the server is running, access the API documentation:

- 📚 Swagger UI: `http://localhost:8000/docs`
- 📖 ReDoc: `http://localhost:8000/redoc`

## 🤝 Contributing

We welcome contributions! Please follow these steps:

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

<div align="center">

| Technology | Purpose |
|:-----------|:--------|
| 🚀 FastAPI | Web Framework |
| 🗃️ SQLAlchemy | ORM |
| ⚙️ Celery | Task Queue |
| 🔄 Redis | Message Broker |
| 🐬 MySQL | Database |

</div>

---

<div align="center">
Made with ❤️ by Your Name
</div>
