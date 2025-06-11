# BaseAPI 🚀

<div align="center">

![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)
![Python](https://img.shields.io/badge/Python-3.8+-blue?style=for-the-badge&logo=python)
![MySQL](https://img.shields.io/badge/MySQL-8.0+-4479A1?style=for-the-badge&logo=mysql&logoColor=white)
![Redis](https://img.shields.io/badge/Redis-6.0+-DC382D?style=for-the-badge&logo=redis&logoColor=white)
![Celery](https://img.shields.io/badge/Celery-37814A?style=for-the-badge&logo=celery&logoColor=white)
![Mailgun](https://img.shields.io/badge/Mailgun-FF0000?style=for-the-badge&logo=mailgun&logoColor=white)
![Stripe](https://img.shields.io/badge/Stripe-626CD9?style=for-the-badge&logo=stripe&logoColor=white)

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=for-the-badge)](https://opensource.org/licenses/MIT)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg?style=for-the-badge)](http://makeapullrequest.com)

</div>

## 📝 Overview

BaseAPI is a comprehensive backend framework that eliminates the complexity of building scalable, secure web applications from scratch. Built on FastAPI's high-performance foundation, it provides everything you need to launch production-grade APIs in minutes, not months.

### 🎯 What is BaseAPI?

BaseAPI is more than just a boilerplate—it's a complete development ecosystem that combines the speed of FastAPI with enterprise-grade features. Think of it as your technical co-founder in a box, providing authentication, payment processing, background tasks, and database management out of the box.

### ✅ Perfect For:
- SaaS Applications requiring subscription management and payment processing
- Startups needing a robust, scalable backend without extensive development time
- Development Teams building APIs for web and mobile applications
- MVPs that need to move fast while maintaining production quality

## ✨ Core Features & How They Work

<div align="center">

| Feature | What It Does | How It Works |
|:--------|:------------|:------------|
| 🔐 **JWT Authentication** | Secure user sessions with industry-standard tokens | Uses python-jose library to generate and verify JWT tokens with configurable expiration |
| 💳 **Stripe Integration** | Complete payment and subscription processing | Built-in Stripe SDK integration with webhook handling for payments, subscriptions, and billing events |
| ⚙️ **Background Tasks** | Handle long-running processes without blocking requests | Celery + Redis implementation for email sending, data processing, and scheduled jobs |
| 🗃️ **Database Management** | Full MySQL integration with migrations | SQLAlchemy ORM with Alembic migrations for schema versioning and database evolution |
| 📧 **Email System** | Automated email delivery with templates | Mailgun integration with development mode for testing and production-ready templates |
| 🏗️ **Modular Architecture** | Clean, maintainable code structure | Follows FastAPI best practices with separated controllers, services, and models |

</div>

## 🏗️ Architecture Overview

BaseAPI follows a modular, production-ready architecture that separates concerns and promotes maintainability:

```bash
baseapi/
├── backend/
│   ├── controllers/          # API route handlers (REST endpoints)
│   │   ├── user/            # User authentication & management
│   │   ├── payment/         # Stripe payment processing
│   │   └── subscription/    # Subscription lifecycle management
│   ├── services/            # Business logic layer
│   │   ├── stripe/          # Payment service integration
│   │   └── subscription/    # Subscription management logic
│   ├── models/              # Database models (SQLAlchemy)
│   ├── tasks/               # Background job definitions (Celery)
│   └── core/                # Configuration & utilities
```

## 🚀 How BaseAPI Works

### 1. Request Processing Flow
When a request hits your API, BaseAPI processes it through several layers:

- **Authentication Layer**: JWT tokens validate user identity
- **Controller Layer**: Route handlers process the request
- **Service Layer**: Business logic executes the operation
- **Database Layer**: SQLAlchemy manages data persistence

### 2. Background Task Processing
Long-running operations are handled asynchronously:

- Tasks are queued in Redis for processing
- Celery workers pick up and execute tasks
- Results are stored and can be retrieved later
- Email notifications and data processing happen without blocking API responses

### 3. Payment Processing Workflow
Stripe integration handles the complete payment lifecycle:

- Customer creation and management
- Subscription setup with multiple pricing tiers
- Webhook handling for payment events
- Automatic retry logic for failed payments

## 🛠️ Quick Start Guide

### Prerequisites
- Python 3.8+
- MySQL 8.0+
- Redis 6.0+
- Stripe Account (for payments)

### Installation
```bash
# Clone and setup
git clone https://github.com/matiasbaglieri/baseapi.git
cd baseapi/backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
make install

# Configure environment
cp .env.example .env
# Edit .env with your configuration
```

### Configuration
BaseAPI uses environment variables for configuration, making it deployment-ready:

```env
# Database Configuration
DB_HOST=localhost
DB_PORT=3306
DB_USER=your_user
DB_PASSWORD=your_password
DB_NAME=baseapi

# Stripe Configuration
STRIPE_API_KEY=your-stripe-secret-key
STRIPE_WEBHOOK_SECRET=your-stripe-webhook-secret

# Celery Configuration
CELERY_BROKER_URL=redis://localhost:6379/0
CELERY_RESULT_BACKEND=redis://localhost:6379/0

# Mailgun Configuration
MAILGUN_API_KEY=your-api-key-here
MAILGUN_DOMAIN=your-domain.com
```

### Running the Application
```bash
# Start the development server
make start

# Run database migrations
make migrate

# Start background worker (separate terminal)
make celery
```

Your API will be available at http://localhost:8000 with automatic documentation at /docs.

## 💼 Business Model Support

### Subscription Management
- Multiple subscription tiers with different features
- Automatic billing and renewal handling
- Proration support for plan changes
- Grace period handling for failed payments

### Payment Methods
- Credit card processing through Stripe
- Bank transfer support
- Multiple currency handling
- Automatic invoice generation

## 🔧 Development Tools

BaseAPI includes a comprehensive Makefile for development automation:

```bash
make install      # Install dependencies
make start        # Start development server
make migrate      # Run database migrations
make celery       # Start background worker
make test         # Run tests (when implemented)
make clean-install # Clean reinstall
```

## 📊 Production Readiness

BaseAPI is designed for production deployment with enterprise-grade features:

- **Docker Support**: Container-ready for Kubernetes deployment
- **Environment Configuration**: Separate configs for development, staging, and production
- **Database Migrations**: Version-controlled schema changes with Alembic
- **Error Handling**: Comprehensive error handling and logging
- **Security**: JWT authentication, CORS configuration, and input validation

## 🌟 Why Choose BaseAPI?

Traditional API development can take weeks or months to set up properly. BaseAPI eliminates this overhead by providing:

- **Instant Development**: Start building features immediately, not infrastructure
- **Battle-Tested Components**: All integrations are production-ready and thoroughly tested
- **Scalable Architecture**: Modular design supports teams and complex applications
- **Complete Feature Set**: Authentication, payments, background jobs, and email—all included
- **Developer Experience**: Automatic API documentation, type hints, and modern Python practices

## 📚 API Documentation

Once running, BaseAPI provides interactive documentation:

- **Swagger UI**: http://localhost:8000/docs - Interactive API testing
- **ReDoc**: http://localhost:8000/redoc - Clean documentation format

## 🤝 Contributing

BaseAPI welcomes contributions following standard open-source practices:

1. Fork the repository
2. Create a feature branch
3. Make your changes with proper testing
4. Submit a pull request with clear description

## 📄 License

This project is licensed under the MIT License, making it free for commercial and personal use.

---

<div align="center">
BaseAPI transforms months of backend development into minutes of configuration. Whether you're building your first startup or your hundredth API, BaseAPI provides the solid foundation you need to focus on what matters most—your unique business logic.

Made with ❤️ by Matias Baglieri
</div>