# Multi-Vendor E-Commerce Platform 🛒

A full-featured multi-vendor e-commerce backend 
built with Python and Django REST Framework.

## 🚀 Features

- Multi-vendor support with separate dashboards
- Product listing and management APIs
- Order processing and tracking system
- User authentication and authorization
- Customer and vendor role management
- REST API endpoints tested with Postman

## 🛠️ Tech Stack

- **Language:** Python
- **Framework:** Django & Django REST Framework
- **Database:** SQLite
- **Authentication:** Django Auth / Token Auth
- **API Testing:** Postman
- **Version Control:** Git & GitHub

## 📁 Project Structure

├── vendors/      # Vendor management
├── products/     # Product listings
├── orders/       # Order processing
├── users/        # Authentication
├── api/          # API endpoints
└── manage.py

## 🔗 API Endpoints

### Auth
- POST /api/auth/register/
- POST /api/auth/login/
- POST /api/auth/logout/

### Vendors
- GET    /api/vendors/
- POST   /api/vendors/create/
- PUT    /api/vendors/{id}/update/
- DELETE /api/vendors/{id}/delete/

### Products
- GET    /api/products/
- POST   /api/products/create/
- PUT    /api/products/{id}/update/
- DELETE /api/products/{id}/delete/

### Orders
- GET    /api/orders/
- POST   /api/orders/create/
- PUT    /api/orders/{id}/update/

## ⚙️ Installation & Setup

# Clone the repository
git clone https://github.com/username/multi-vendor-ecommerce

# Go to project directory
cd multi-vendor-ecommerce

# Install dependencies
pip install -r requirements.txt

# Run migrations
python manage.py migrate

# Start server
python manage.py runserver

## 🧪 API Testing

All endpoints tested with Postman.

## 👨‍💻 Developer

**Your Name**
Backend Developer | Python & Django
GitHub: https://github.com/faizarajpoot1505/
LinkedIn: https://linkedin.com/in/faiza-ali
