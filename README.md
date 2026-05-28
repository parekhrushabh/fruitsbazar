# 🍎 Fruit Bazar — Django E-Commerce Web Application

A fully featured fruit & grocery e-commerce web application built with **Django**, supporting user authentication, product management, shopping cart, Razorpay payment integration, order tracking, and an admin dashboard.

---

## 📋 Table of Contents

- [Features](#-features)
- [Project Structure](#-project-structure)
- [Tech Stack](#-tech-stack)
- [Requirements](#-requirements)
- [Installation & Setup](#-installation--setup)
- [Environment Variables](#-environment-variables)
- [Running the Project](#-running-the-project)
- [Admin Panel](#-admin-panel)
- [Payment Integration](#-payment-integration)
- [Database Models](#-database-models)
- [URL Structure](#-url-structure)
- [Screenshots](#-screenshots)

---

## ✨ Features

### 👤 User Side
- User Registration & Login / Logout
- Session-based Shopping Cart (add, remove, increment, decrement)
- Product listing with Search & Category Filter
- Single Product Detail Page with Customer Reviews & Ratings
- Checkout with shipping details form
- Payment via **Cash on Delivery** or **Razorpay (Card)**
- Invoice generation after successful order
- Newsletter Subscription
- Contact Us form
- About & News pages

### 🛠️ Admin Side
- Secure Admin Dashboard (superuser only)
- Product & Category Management (Add / Edit / Delete)
- Multiple Product Image Upload
- Order Management with Status Updates (Pending → Processing → Shipped → Delivered → Cancelled)
- Payment Records & History
- User Management (Block / Unblock users)
- Real-time Notifications (new user registrations, contact messages)
- Subscriber list management

---

## 📁 Project Structure

```
fruit_bazar/
│
├── app_module/
│   ├── admin_app/          # Admin panel logic
│   │   ├── models.py       # All database models
│   │   ├── views.py        # Admin views
│   │   ├── urls.py         # Admin URL routes
│   │   ├── forms.py        # Admin forms
│   │   ├── admin.py        # Django admin registration
│   │   └── context_processors.py
│   │
│   ├── user_app/           # User-facing logic
│   │   ├── views.py        # User views (shop, cart, checkout, auth)
│   │   ├── urls.py         # User URL routes
│   │   └── forms.py
│   │
│   └── cart_app/           # Session-based cart engine
│       ├── cart.py         # Cart class
│       └── context_processors.py
│
├── fruit_bazar/            # Django project config
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
│
├── templates/
│   ├── user_app/           # User-facing HTML templates
│   └── admin_app/          # Admin panel HTML templates
│
├── static/                 # CSS, JS, images
├── media/                  # User-uploaded product images
├── manage.py
├── db.sqlite3
├── requirements.txt
└── README.md
```

---

## 🛠️ Tech Stack

| Layer       | Technology                         |
|-------------|-------------------------------------|
| Backend     | Python 3.x, Django 4.x             |
| Database    | SQLite3 (dev) / PostgreSQL (prod)  |
| Frontend    | HTML5, CSS3, JavaScript, Bootstrap |
| Payments    | Razorpay API                        |
| Auth        | Django built-in Auth System         |
| Media       | Pillow (image handling)             |
| Sessions    | Django DB-backed sessions           |

---

## 📦 Requirements

Make sure you have **Python 3.9+** installed.

Install all dependencies using:

```bash
pip install -r requirements.txt
```

Key packages:
- `Django>=4.2`
- `Pillow>=10.0.0`
- `razorpay>=1.4.1`
- `python-dotenv>=1.0.0`

---

## ⚙️ Installation & Setup

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/fruit_bazar.git
cd fruit_bazar
```

### 2. Create a Virtual Environment

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS / Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Apply Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### 5. Create a Superuser (Admin)

```bash
python manage.py createsuperuser
```

Follow the prompts to set username, email, and password.

### 6. Collect Static Files (optional, for production)

```bash
python manage.py collectstatic
```

---

## 🔐 Environment Variables

For security, move sensitive credentials out of `settings.py`. Create a `.env` file in the project root:

```env
SECRET_KEY=your-django-secret-key-here
DEBUG=True
RAZORPAY_KEY_ID=rzp_test_xxxxxxxxxxxxxxxx
RAZORPAY_KEY_SECRET=your_razorpay_secret_here
```

> ⚠️ **Never commit `.env` or expose your secret keys in production!**

---

## 🚀 Running the Project

```bash
python manage.py runserver
```

Then open your browser and go to:

```
http://127.0.0.1:8000/
```

---

## 🖥️ Admin Panel

Access the custom admin dashboard at:

```
http://127.0.0.1:8000/admin_app/
```

Or the built-in Django admin at:

```
http://127.0.0.1:8000/admin/
```

Login with the superuser credentials you created.

---

## 💳 Payment Integration

This project integrates **Razorpay** for card payments.

### How it works:
1. User selects **Card** at checkout
2. A Razorpay order is created server-side
3. Razorpay payment modal opens on the client
4. On success, the callback verifies the signature and updates order status to `Processing`

### Test Credentials (Razorpay Test Mode):
- Use any test card from [Razorpay Test Cards](https://razorpay.com/docs/payments/payments/test-card-upi-details/)
- Card Number: `4111 1111 1111 1111`
- Expiry: Any future date
- CVV: Any 3 digits

> ⚠️ Replace `RAZORPAY_KEY_ID` and `RAZORPAY_KEY_SECRET` in `settings.py` or `.env` with your own keys.

---

## 🗄️ Database Models

| Model           | Description                                      |
|-----------------|--------------------------------------------------|
| `category`      | Product categories                               |
| `product`       | Products with price, stock, unit                 |
| `productimage`  | Multiple images per product                      |
| `Order`         | Customer orders with shipping details            |
| `OrderItem`     | Individual items within an order                 |
| `Payment`       | Payment records linked to orders                 |
| `ProductReview` | User reviews and ratings for products            |
| `UserStatus`    | Tracks online/offline and blocked status         |
| `Notification`  | Admin notifications for new users/messages       |
| `contect`       | Contact form submissions                         |
| `subscribe`     | Newsletter subscriber emails                     |
| `comments`      | Blog/news comment data                           |

---

## 🌐 URL Structure

### User URLs (`/`)
| URL Pattern              | View                  | Description              |
|--------------------------|-----------------------|--------------------------|
| `/`                      | `index_view`          | Home page                |
| `/shop/`                 | `shop_view`           | Product listing          |
| `/shop/<id>/`            | `single_product_view` | Product detail           |
| `/cart/`                 | `cart_view`           | Shopping cart            |
| `/checkout/`             | `checkout_view`       | Checkout page            |
| `/invoice/<id>/`         | `invoice_view`        | Order invoice            |
| `/contact/`              | `contact_view`        | Contact page             |
| `/about/`                | `about_view`          | About page               |
| `/register/`             | `pages_register`      | User registration        |
| `/login/`                | `pages_login`         | User login               |
| `/logout/`               | `logout_view`         | User logout              |

### Admin URLs (`/admin_app/`)
| URL Pattern              | Description              |
|--------------------------|--------------------------|
| `/admin_app/`            | Admin dashboard          |
| `/admin_app/products/`   | Manage products          |
| `/admin_app/orders/`     | Manage orders            |
| `/admin_app/users/`      | Manage users             |
| `/admin_app/payments/`   | View payments            |

---

## 🖼️ Screenshots

> Add screenshots of your application here.

```
/static/screenshots/home.png
/static/screenshots/shop.png
/static/screenshots/checkout.png
/static/screenshots/admin_dashboard.png
```

---

## 👨‍💻 Author

**Your Name**  
📧 parekh1224@gmail.com  
🔗 [GitHub Profile](https://github.com/parekhrushabh/fruitsbazar)

---

## 📄 License

This project is licensed under the **MIT License**.  
Feel free to use, modify, and distribute with attribution.

---

> Made with ❤️ using Django & Python
