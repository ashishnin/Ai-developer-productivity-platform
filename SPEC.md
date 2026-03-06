# AI Developer Productivity & Code Risk Analysis Platform

## Project Overview

**Project Name:** DevInsight AI  
**Type:** Full-stack Web Application  
**Core Functionality:** Analyze developer activity and code change patterns to generate productivity insights and predict risky modules using machine learning  
**Target Users:** Software development teams, Engineering managers, Team leads

---

## Technical Stack

### Frontend
- React.js 18+
- TailwindCSS for styling
- Recharts for analytics charts
- Axios for API calls
- React Router for navigation

### Backend
- Python FastAPI
- REST API architecture
- JWT authentication
- Modular backend structure

### Database
- SQLite (for development simplicity)
- SQLAlchemy ORM

### Machine Learning
- scikit-learn
- Random Forest Classifier
- pandas, numpy for data processing

---

## UI/UX Specification

### Color Palette
- **Background Primary:** #0f172a (slate-900)
- **Background Secondary:** #1e293b (slate-800)
- **Background Card:** #334155 (slate-700)
- **Primary Accent:** #3b82f6 (blue-500)
- **Secondary Accent:** #10b981 (emerald-500)
- **Warning:** #f59e0b (amber-500)
- **Danger:** #ef4444 (red-500)
- **Success:** #22c55e (green-500)
- **Text Primary:** #f8fafc (slate-50)
- **Text Secondary:** #94a3b8 (slate-400)
- **Border:** #475569 (slate-600)

### Typography
- **Font Family:** Inter, system-ui, sans-serif
- **Headings:** Bold, sizes 2rem-1.25rem
- **Body:** Regular, 0.875rem-1rem
- **Monospace:** JetBrains Mono (for code/metrics)

### Layout Structure
- **Sidebar:** Fixed left, 256px width, dark background
- **Main Content:** Fluid, with 24px padding
- **Cards:** Rounded corners (12px), subtle shadows
- **Responsive:** Collapsible sidebar on mobile

### Components
1. **Sidebar Navigation**
   - Logo at top
   - Navigation links with icons
   - User profile section at bottom

2. **Dashboard Cards**
   - Summary metrics with icons
   - Gradient borders on hover
   - Animated counters

3. **Charts**
   - Line charts for trends
   - Bar charts for comparisons
   - Pie charts for distributions
   - Heatmap for risk analysis

4. **Data Tables**
   - Sortable columns
   - Pagination
   - Row hover effects
   - Action buttons

5. **Forms**
   - Floating labels
   - Validation states
   - Loading states on buttons

---

## Pages & Features

### 1. Login Page
- Email/password form
- "Remember me" checkbox
- Link to register page
- Error message display
- Clean centered card layout

### 2. Register Page
- Username, email, password fields
- Role selection (Admin/Developer/Manager)
- Terms acceptance checkbox
- Link to login page

### 3. Dashboard (Home)
- Summary cards: Total Projects, Active Developers, Avg Productivity, Risk Alerts
- Developer productivity chart (bar chart)
- Module risk heatmap
- Recent activity feed
- AI recommendations panel
- Quick actions

### 4. Projects Page
- Project cards grid
- Create project modal
- Project details: name, team members, repo link, description
- Status indicators
- Edit/delete actions

### 5. Developer Analytics Page
- Developer list with productivity scores
- Individual developer detailed view
- Commit history chart
- Code churn trends
- Bug count tracking

### 6. Module Risk Analysis Page
- Risk heatmap by module
- Risk score cards
- Detailed risk breakdown
- Historical risk trends
- AI recommendations per module

### 7. Data Upload Page
- CSV upload interface
- Manual entry form
- Upload history
- Data validation feedback
- Sample data download

### 8. AI Insights Page
- AI-generated insights list
- Risk predictions summary
- Productivity recommendations
- Trend analysis

---

## Backend API Structure

### Authentication Endpoints
- `POST /auth/register` - User registration
- `POST /auth/login` - User login, returns JWT
- `GET /auth/me` - Get current user
- `POST /auth/refresh` - Refresh token

### Project Endpoints
- `GET /projects` - List all projects
- `POST /projects` - Create project
- `GET /projects/{id}` - Get project details
- `PUT /projects/{id}` - Update project
- `DELETE /projects/{id}` - Delete project

### Activity Endpoints
- `POST /activity/upload` - Upload CSV
- `POST /activity/manual` - Manual entry
- `GET /activity` - List activities

### Analytics Endpoints
- `GET /analytics/productivity` - Developer productivity
- `GET /analytics/commits` - Commit analysis
- `GET /analytics/churn` - Code churn metrics

### AI Endpoints
- `POST /ai/predict-risk` - Predict module risk
- `GET /ai/insights` - Get AI recommendations
- `POST /ai/train` - Retrain model

---

## Database Schema

### Users Table
- id (PK)
- username
- email
- password_hash
- role (admin/developer/manager)
- created_at

### Projects Table
- id (PK)
- name
- description
- repo_link
- owner_id (FK)
- created_at

### Project Members Table
- id (PK)
- project_id (FK)
- user_id (FK)
- role

### Activities Table
- id (PK)
- project_id (FK)
- developer_name
- commit_count
- lines_added
- lines_deleted
- files_modified
- module_name
- bug_count
- last_modified_date

### Metrics Table
- id (PK)
- activity_id (FK)
- code_churn
- instability_score
- calculated_at

---

## Machine Learning Model

### Input Features
- commit_count
- lines_added
- lines_deleted
- files_modified
- code_churn
- bug_count
- modification_frequency

### Model
- Random Forest Classifier
- Outputs: Low/Medium/High risk
- Risk score: 0-100

### Training Data
- Synthetic dataset with labeled examples
- Balanced classes

---

## Acceptance Criteria

1. ✅ User can register and login
2. ✅ JWT authentication works
3. ✅ User can create/view projects
4. ✅ User can upload CSV data
5. ✅ Dashboard displays analytics charts
6. ✅ AI risk prediction works
7. ✅ Productivity metrics calculated
8. ✅ AI recommendations generated
9. ✅ Responsive UI works
10. ✅ API documentation available at /docs

---

## File Structure

```
/workspace/project/
├── backend/
│   ├── main.py
│   ├── requirements.txt
│   ├── database.py
│   ├── models.py
│   ├── schemas.py
│   ├── routers/
│   │   ├── auth.py
│   │   ├── projects.py
│   │   ├── activities.py
│   │   ├── analytics.py
│   │   └── ai.py
│   └── ml/
│       └── risk_model.py
├── frontend/
│   ├── package.json
│   ├── tailwind.config.js
│   ├── src/
│   │   ├── App.jsx
│   │   ├── main.jsx
│   │   ├── index.css
│   │   ├── api/
│   │   ├── components/
│   │   ├── pages/
│   │   └── context/
│   └── public/
└── data/
    └── sample_data.csv
```
