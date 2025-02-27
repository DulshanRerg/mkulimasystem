# Mkulima App

**Mkulima App** is a full-stack Django application that connects farmers and buyers in a streamlined marketplace. It provides product listings, real-time chat, secure payments, and subscription management — all designed to help farmers reach a wider audience and buyers find the best deals.

## Table of Contents

- [Features](#features)  
- [Tech Stack](#tech-stack)  
- [Architecture Overview](#architecture-overview)  
- [Installation](#installation)  
- [Usage](#usage)  
- [Project Structure](#project-structure)  
- [Environment Variables](#environment-variables)  
- [Running Tests](#running-tests)  
- [Contributing](#contributing)  
- [License](#license)

---

## Features

1. **User Authentication & Roles**  
   - Custom user model with roles: Farmer, Buyer, and Admin.  
   - Secure registration, login, and logout flows.

2. **Product Listings**  
   - Farmers can post crop details (title, price, location, image).  
   - Buyers can browse and filter listings.

3. **Real-Time Chat**  
   - WebSocket-based messaging system using Django Channels.  
   - Instant communication between buyers and farmers.

4. **Payments & Subscriptions**  
   - AzamPay integration for secure transactions.  
   - Tiered subscription plans (e.g., Basic, Premium) with expiry dates.

5. **Admin Dashboard**  
   - Manage users, products, and transactions.  
   - View analytics and subscription status.

---

## Tech Stack

- **Language:** Python 3.9+  
- **Framework:** Django 3.2+ (including Django Channels for real-time features)  
- **Database:** PostgreSQL (recommended), or any other supported RDBMS  
- **Payment Integration:** AzamPay API  
- **Front-End:** Django Templates, HTML5, CSS (Tailwind or Bootstrap recommended), JavaScript  
- **Real-Time:** Redis (as the Channels layer backend)  
- **Deployment:** Gunicorn & Nginx (production), Docker (optional)

---

## Architecture Overview

```mermaid
flowchart LR
    A[Client Browser] --> B[Django Templates]
    B --> C[(Django Backend)]
    C -->|HTTP| D[Products, Accounts, Payments, etc.]
    C -->|WebSockets| E[Channels + Redis]
    D --> F[(PostgreSQL DB)]
    C -->|API| G[AzamPay Service]
```

1. **Client** interacts via Django templates and WebSockets for real-time chat.  
2. **Django** processes requests using multiple apps (accounts, products, chat, subscriptions, payments).  
3. **Redis** handles WebSocket messages through **Channels**.  
4. **PostgreSQL** (or another RDBMS) stores persistent data (users, products, transactions).  
5. **AzamPay** processes secure payments.

---

## Installation

1. **Clone the Repository:**
   ```bash
   git clone https://github.com/DulshanRerg/mkulimasystem.git
   cd mkulimasystem
   ```

2. **Create a Virtual Environment (Recommended):**
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   venv\\Scripts\\activate   # Windows
   ```

3. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set Up the Database:**
   - Create a PostgreSQL database (or any other DB supported by Django).
   - Update `DATABASES` in `mkulima_project/settings.py` with your credentials.

5. **Apply Migrations:**
   ```bash
   python manage.py migrate
   ```

6. **Create a Superuser (Admin Account):**
   ```bash
   python manage.py createsuperuser
   ```

7. **Run the Server:**
   ```bash
   python manage.py runserver
   ```
   Access the site at [http://127.0.0.1:8000](http://127.0.0.1:8000).

---

## Usage

1. **Landing Page:**  
   Visit `/` to see the landing page with features and call-to-action buttons.

2. **Sign Up / Login:**  
   - `/accounts/signup/` for new users (choose role: farmer, buyer, or admin).  
   - `/accounts/login/` to log in.

3. **Posting a Product (Farmer):**  
   - Navigate to `/products/create/` (requires farmer role).  
   - Provide title, description, price, location, and an image.

4. **Browsing Products (Buyer):**  
   - Go to `/products/` to see all posted products.  
   - Click on any product to view details and start a chat with the farmer.

5. **Chat:**  
   - Real-time chat is accessible via `/chat/room/<room_name>/`.  
   - Initiate chat sessions based on product or user preferences.

6. **Subscription & Payments:**  
   - Subscribe at `/subscriptions/subscribe/`.  
   - Process payments at `/payments/initiate/` using AzamPay.

7. **Admin Panel:**  
   - `/admin/` to manage users, products, and transactions.

---

## Project Structure

```
mkulima-app/
├── mkulima_project/
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── routing.py        # Channels routing
├── accounts/
│   ├── models.py         # Custom User model
│   ├── forms.py          # CustomUserCreationForm
│   ├── views.py
│   └── urls.py
├── products/
│   ├── models.py         # Product model
│   ├── forms.py
│   ├── views.py
│   └── urls.py
├── chat/
│   ├── models.py
│   ├── consumers.py      # WebSocket consumers
│   └── urls.py
├── subscriptions/
│   ├── models.py         # Subscription model
│   ├── views.py
│   └── urls.py
├── payments/
│   ├── models.py         # Transaction model
│   ├── services.py       # AzamPay integration
│   ├── views.py
│   └── urls.py
├── templates/
│   ├── base.html
│   ├── landing_page.html
│   └── ...
├── static/
│   ├── css/
│   │   └── style.css
│   └── images/
├── requirements.txt
└── manage.py
```

---

## Environment Variables

Set the following variables in your `.env` file or environment settings:

```bash
SECRET_KEY=your_secret_key
DEBUG=True  # Switch to False in production
DATABASE_URL=postgres://username:password@localhost:5432/mkulima_db

# AzamPay credentials
AZAMPAY_BASE_URL=https://sandbox.azampay.co.tz
AZAMPAY_CLIENT_ID=your_client_id
AZAMPAY_CLIENT_SECRET=your_client_secret

# Redis (if using Channels)
REDIS_URL=redis://localhost:6379
```

Ensure you configure your `settings.py` to read these values using `os.environ` or a library like **python-dotenv**.

---

## Running Tests

Run unit tests and integration tests with:

```bash
python manage.py test
```

- **accounts/tests.py**: Tests for custom user creation and authentication.  
- **products/tests.py**: Tests for product listing, creation, and detail views.  
- **payments/tests.py**: Tests for AzamPay integration and transaction logic.  
- **subscriptions/tests.py**: Tests for subscription creation and expiration.  
- **chat/tests.py**: Tests for WebSocket connections and chat functionality.

---

## Contributing

1. **Fork** the repository and **clone** your fork.  
2. Create a **feature branch** (`git checkout -b feature/new-feature`).  
3. **Commit** your changes (`git commit -m 'Add new feature'`).  
4. **Push** to your fork (`git push origin feature/new-feature`).  
5. Open a **Pull Request** to the main branch of this repository.

Please make sure your code adheres to the project’s coding standards and includes relevant tests.

---

## License

This project is licensed under the [MIT License](LICENSE). Feel free to use, modify, and distribute this software. See the [LICENSE](LICENSE) file for details.

---

**Thank you for using the Mkulima App!** If you have any questions or feedback, please open an issue or reach out to the maintainers. Happy coding!