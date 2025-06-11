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

BaseAPI is a modern, production-ready backend framework built with FastAPI, designed to accelerate the development of secure, scalable, and modular web applications.

It provides a clean architecture out of the box, featuring user authentication, background task processing, email support, and database integration. Whether you're building an MVP or deploying an enterprise-grade system, BaseAPI gives you the foundation to move fast without compromising on structure or performance.

### ✅ Perfect For:
- SaaS applications requiring subscription management
- Startups needing a clean, extensible backend
- Teams building APIs for web/mobile apps
- Projects requiring payment processing
- Developers who want asynchronous performance and modern Python

### 🔍 Why BaseAPI?
- **Fast to develop with**, thanks to FastAPI
- **Robust structure** built for real-world use cases
- **Scalable** with Celery + Redis for background jobs
- **Ready for Docker, Kubernetes, and cloud deployments**
- **Secure and configurable** out of the box (JWT, Mailgun, Stripe, .env)
- **Flexible payment options** (Stripe, Bank Check, etc.)

## ✨ Key Features

<div align="center">

| Feature | Description |
|:--------|:------------|
| 🔐 **Authentication** | JWT-based user authentication with session management |
| 💳 **Payment Processing** | Stripe integration with multiple payment methods |
| 📊 **Subscription Management** | Flexible subscription plans with status tracking |
| ⚙️ **Task Processing** | Background tasks with Celery + Redis |
| 🗃️ **Database** | MySQL support with SQLAlchemy/SQLModel |
| 📦 **Architecture** | Modular, production-ready project structure |
| 🔧 **Configuration** | Environment-based configuration for flexibility |
| 📈 **Scalability** | Ready for Docker/Kubernetes environments |
| 📧 **Email System** | Mailgun integration with development mode |

</div>

## 🏗️ Project Structure

```bash
baseapi/
├── backend/
│   ├── alembic/              # Database migrations
│   ├── controllers/          # API route handlers
│   │   ├── base.py          # Base routes
│   │   ├── user/            # User-related routes
│   │   ├── admin/           # Admin routes
│   │   ├── payment/         # Payment routes
│   │   └── subscription/    # Subscription routes
│   ├── core/                # Core functionality
│   │   ├── celery_app.py    # Celery configuration
│   │   ├── init_db.py       # Database initialization
│   │   ├── mail.py         # Mailgun service
│   │   └── utils.py         # Utility functions
│   ├── models/              # SQLAlchemy models
│   │   ├── user.py         # User model
│   │   ├── payment.py      # Payment model
│   │   ├── subscription.py # Subscription model
│   │   └── session.py      # Session model
│   ├── services/           # Business logic
│   │   ├── stripe/         # Stripe integration
│   │   ├── payment/        # Payment processing
│   │   └── subscription/   # Subscription management
│   ├── tasks/              # Celery tasks
│   │   └── email_tasks.py  # Email-related tasks
│   ├── .env                # Environment variables
│   ├── app.py             # FastAPI application
│   ├── requirements.txt   # Python dependencies
│   └── Makefile          # Build automation
└── README.md             # Project documentation
```

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- MySQL 8.0+
- Redis 6.0+
- Stripe Account
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

# Development Mode
DEV_MODE=true  # Set to false in production

# Mailgun Configuration
MAILGUN_API_KEY=your-api-key-here
MAILGUN_DOMAIN=your-domain.com
MAILGUN_FROM_EMAIL=noreply@your-domain.com

# Stripe Configuration
STRIPE_API_KEY=your-stripe-secret-key
STRIPE_WEBHOOK_SECRET=your-stripe-webhook-secret
STRIPE_PRICE_ID=your-stripe-price-id
STRIPE_PRODUCT_ID=your-stripe-product-id
```

## 💳 Payment & Subscription Features

### Stripe Integration

BaseAPI includes comprehensive Stripe integration for handling payments and subscriptions:

1. **Payment Methods**
   - Credit Card processing
   - Bank Check support
   - Multiple currency support
   - Payment status tracking

2. **Subscription Management**
   - Multiple subscription tiers
   - Subscription status tracking
   - Automatic renewal handling
   - Proration support

3. **Webhook Handling**
   - Payment success/failure
   - Subscription updates
   - Invoice events
   - Customer events

### Using Payment Service

```python
from services.stripe.subscription_user_service import SubscriptionUserService

# Create a subscription with bank check
subscription_data = {
    "subscription_id": 123,
    "payment_type": "bank_check",
    "amount": 100.00,
    "currency": "USD"
}
result = await subscription_service.create_user_subscription(user_id, subscription_data)

# Create a subscription with Stripe
subscription_data = {
    "subscription_id": 123,
    "payment_type": "stripe",
    "payment_method_id": "pm_123456"
}
result = await subscription_service.create_user_subscription(user_id, subscription_data)
```

## 📧 Email Configuration

### Mailgun Setup

BaseAPI uses Mailgun for sending emails. To set up Mailgun:

1. **Create a Mailgun Account**
   - Sign up at [Mailgun](https://www.mailgun.com/)
   - Verify your domain or use the sandbox domain for testing

2. **Get Your API Key**
   - Go to Mailgun Dashboard → Settings → API Keys
   - Copy your Private API Key

3. **Configure Environment Variables**
   ```env
   MAILGUN_API_KEY=your-api-key-here
   MAILGUN_DOMAIN=your-domain.com
   MAILGUN_FROM_EMAIL=noreply@your-domain.com
   ```

### Available Email Templates

- Welcome Email
- Email Verification
- Password Reset
- Payment Confirmation
- Subscription Updates
- Custom Emails

## 🛠️ Usage

### Development

```bash
# Start development server
make start

# Run database migrations
make migrate
```

### Makefile Commands

```bash
# Create virtual environment
make venv

# Install dependencies
make install

# Start the application
make start
# or
make run

# Database migrations
make alembic              # Initialize Alembic
make alembic-revision     # Create new migration
make alembic-upgrade      # Apply migrations
make alembic-downgrade    # Rollback last migration

# Celery tasks
make celery              # Start Celery worker
make celery-beat         # Start Celery beat scheduler

# Clean installation
make clean-install       # Clean and reinstall dependencies
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
| 📧 Mailgun | Email Service |
| 💳 Stripe | Payment Processing |

</div>

---

<div align="center">
Made with ❤️ by Matias Baglieri
</div>