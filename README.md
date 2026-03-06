# DevInsight AI - Developer Productivity Platform

AI-powered developer productivity tracking and code risk analysis platform.

## Features

- **User Authentication**: JWT-based auth with role-based access (Admin, Manager, Developer)
- **Project Management**: Create and manage software projects with team members
- **Activity Tracking**: Manual entry or CSV upload of developer activity data
- **Analytics Dashboard**: Real-time metrics with charts
- **AI Risk Prediction**: Machine learning model (Random Forest) predicts module risk scores
- **Developer Analytics**: Per-developer productivity metrics and contributions
- **AI Insights**: Automated recommendations for code improvements

## Tech Stack

- **Frontend**: React + TailwindCSS + Recharts
- **Backend**: FastAPI (Python)
- **Database**: SQLite (easily switchable to PostgreSQL)
- **ML**: scikit-learn (Random Forest Classifier)

## Quick Start

### Prerequisites
- Python 3.9+
- Node.js 18+
- npm or yarn

### Installation

```bash
# Clone the repository
git clone https://github.com/ashishnin/Ai-developer-productivity-platform.git
cd Ai-developer-productivity-platform

# Backend setup
cd backend
pip install -r requirements.txt
python -m uvicorn main:app --reload

# Frontend setup (in new terminal)
cd frontend
npm install
npm run dev
```

### Access the App
- Frontend: http://localhost:5173
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/docs

### Default Login
- Email: newuser@example.com
- Password: newpass123

## API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/auth/register` | POST | Register new user |
| `/auth/login` | POST | Login user |
| `/projects` | GET/POST | List/Create projects |
| `/activity/manual` | POST | Add activity data |
| `/activity/upload` | POST | Upload CSV |
| `/analytics/productivity` | GET | Developer metrics |
| `/ai/predict-risk` | POST | AI risk prediction |

## Screenshots

The dashboard displays:
- Developer productivity charts
- Module risk heatmap
- Code churn trends
- AI-generated insights and recommendations
