# 💼 Smart Business Management System

Welcome to the **Smart Business Management System** (SBMS), a state-of-the-art, modern enterprise resource planning and management platform designed to streamline business operations, track performance, and enhance decision-making through intuitive data visualization and advanced tooling.

---

## 🏗️ Project Architecture

The system is structured as a Microservices-ready decoupled monorepo:

```
smart-business-management-system/
├── client/          # Frontend client application (Angular 17 / TypeScript)
├── server/          # Main Backend server application (FastAPI / Python)
├── auth-service/    # Upcoming Centralized Auth Microservice (JWT / IAM)
├── docs/            # Project documentation and architectural specs
├── README.md        # Main entrypoint documentation
└── .gitignore       # Git exclusion specifications
```

---

## 🌟 Key Features

- **🔒 Role-Based Access Control (RBAC):** Secure JWT authentication, route guards, and granular permissions for staff, managers, and administrators via a Centralized Auth Service.
- **📊 Dynamic Dashboard:** High-level metrics, revenue tracking, and business health monitoring with rich interactive charts.
- **👥 Customer Relationship Management (CRM):** Track client interactions, pipeline stages, and contact info.
- **📦 Inventory & Product Control:** Real-time stock alerts, inventory turnover, and product catalogs.
- **📄 Invoicing & Finance:** Seamless invoice generation, automated payment reminders, and expense reporting.
- **📈 Analytics & Reporting:** Advanced business intelligence, forecasting, and downloadable reports.

---

## 🛠️ Technology Stack

### **Frontend (client)**
- **Framework:** Angular 17+ (Standalone / NgModule Architecture)
- **Styling:** Vanilla SCSS & modern glassmorphic components
- **Routing:** Lazy-Loaded Feature Modules
- **State/API:** RxJS, Angular HttpClient Interceptors

### **Backend (server / auth-service)**
- **Runtime:** Python 3.10+
- **Framework:** FastAPI
- **Database:** MySQL / SQLite
- **ORM:** SQLAlchemy
- **Auth:** JSON Web Tokens (PyJWT) & bcrypt

---

## 🚀 Getting Started

### Prerequisites
Make sure you have [Node.js](https://nodejs.org/) (for Angular CLI) and [Python](https://www.python.org/) installed.

### Setup Instructions

1. **Clone the repository:**
   ```bash
   git clone https://github.com/KartikV27/smart-business-management-system.git
   cd smart-business-management-system
   ```

2. **Run Frontend (Client):**
   ```bash
   cd client
   npm install
   ng serve -o
   ```

3. **Run Backend (Server):**
   ```bash
   cd ../server
   python -m venv venv
   .\venv\Scripts\activate
   pip install -r requirements.txt
   uvicorn main:app --reload
   ```

---

## 📖 Documentation
Detailed specifications, API reference manuals, database schema diagrams, and wireframes are stored inside the `docs/` directory.

---

## 📄 License
This project is licensed under the MIT License - see the LICENSE file for details.
