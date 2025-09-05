# bkash-pgw-integration

A simple subscription service with bKash payment integration using Python.

## Tech Stack
- **Frontend**: Vue.js + JavaScript
- **Backend**: FastAPI (Python)
- **Database**: SQLite (development) / PostgreSQL (production)
- **Payment**: bKash Payment Gateway

## Project Structure
```
├── frontend/          # Vue.js frontend
├── backend/           # FastAPI backend
├── README.md          # This file
└── docker-compose.yml # PostgreSQL setup (optional)
```

## Prerequisites
- Python 3.8+
- Node.js 16+
- PostgreSQL 12+ (optional, SQLite used by default)

## Quick Setup (Local Development)

### 1. Clone and Setup Backend

```bash
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Setup environment variables
cp .env.example .env
```

### 2. Configure Environment Variables

Edit `backend/.env` file:

```bash
# Generate a secure JWT secret key
# Add the generated key to .env file
SECRET_KEY=your_generated_secret_key_here

# For bKash integration, get credentials from bKash merchant portal
```

### 3. Start Backend Server

```bash
cd backend
source venv/bin/activate
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### 4. Setup Frontend

```bash
cd frontend
npm install
npm run dev
```

### 5. Access Application

- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs

## Features

### Payment Integration
- Full bKash sandbox integration
- Secure token-based authentication with bKash API
- Complete payment lifecycle management
- Payment status tracking and verification
- Demo mode fallback when bKash API is unavailable

### User Experience
- User registration and authentication
- JWT-based session management
- Subscription plan selection
- Real-time payment processing
- User dashboard with subscription history

### Security
- JWT authentication
- Secure API endpoints
- Environment-based configuration
- Input validation and sanitization

## API Endpoints

### Authentication
- `POST /auth/register` - User registration
- `POST /auth/login` - User login

### Subscriptions
- `GET /subscriptions` - Get available plans
- `GET /user/subscriptions` - Get user's subscriptions

### Payments
- `POST /payment/create` - Create payment
- `POST /payment/execute` - Execute payment
- `GET /payment/status/{payment_id}` - Check payment status

## bKash Integration Details

The project uses bKash's tokenized checkout API with the following flow:

1. **Token Grant** - Get access token from bKash
2. **Create Payment** - Initialize payment with bKash
3. **Execute Payment** - Complete the payment process
4. **Query Payment** - Check payment status


### Developed By Shakil Ahmed
