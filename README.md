```markdown
# Chemical Equipment Parameter Visualizer

A hybrid web and desktop application for visualizing and analyzing chemical equipment parameters.  
The application allows users to upload CSV files containing equipment data and provides interactive charts, summary statistics, dataset history, and PDF reports.

Both the web frontend and the desktop application communicate with a shared backend API.

## Architecture

The system consists of three components.

Backend API  
Django and Django REST Framework handle data ingestion, validation, processing, storage, and report generation.

Web Frontend  
React with Chart.js provides a browser based interface for visualization and analysis.

Desktop Frontend  
PyQt5 with Matplotlib or PyQtChart provides a native desktop interface with the same functionality.

## Features

CSV upload from web and desktop  
Interactive charts for equipment parameters  
Automatic summary statistics  
History of the last 5 uploaded datasets  
PDF report generation  
Basic HTTP authentication  
SQLite database persistence  
Cross platform support

## Technology Stack

Backend: Django, Django REST Framework  
Database: SQLite  
Web Frontend: React, Chart.js  
Desktop Frontend: PyQt5, Matplotlib or PyQtChart  
Data Processing: Python csv module  
PDF Generation: ReportLab

## Project Structure

chemical-equipment-visualizer/
├── backend/
│   ├── config/
│   ├── equipment_api/
│   ├── media/
│   │   └── uploads/
│   ├── venv/
│   ├── db.sqlite3
│   └── manage.py
├── frontend-web/
│   ├── src/
│   │   └── components/
│   ├── public/
│   └── package.json
├── frontend-desktop/
│   ├── venv/
│   └── main.py
└── sample_equipment_data.csv

## Quick Start Guide

### Prerequisites

Python 3.8 or higher  
Node.js 16 or higher  
Git

### Backend Setup

cd backend  
python -m venv venv  

Activate virtual environment.

Windows  
venv\Scripts\activate  

Linux or macOS  
source venv/bin/activate  

Install dependencies.

pip install Django==4.2.7 djangorestframework==3.14.0 django-cors-headers==4.2.0 reportlab==4.0.4 PyPDF2==3.0.1  

Apply migrations.

python manage.py migrate  

Create superuser.

python manage.py createsuperuser  

Example credentials  
Username: admin  
Password: password123  

Create upload directory.

mkdir media\uploads  

Start server.

python manage.py runserver  

Backend URL  
http://localhost:8000  

### Web Frontend Setup

cd frontend-web  
npm install  
npm start  

Web application URL  
http://localhost:3000  

### Desktop Application Setup

cd frontend-desktop  
python -m venv venv  

Activate environment and install dependencies.

pip install PyQt5==5.15.9 requests==2.31.0  

Run application.

python main.py  

## CSV File Format

Equipment Name,Equipment Type,Flowrate,Pressure,Temperature  
Reactor-001,Reactor,150.5,10.2,85.0  
Mixer-001,Mixer,200.0,5.5,65.0  
Separator-001,Separator,120.3,8.7,75.5  

A sample file is included as sample_equipment_data.csv.

## Usage

Web Application  
Upload CSV file.  
Charts and statistics render automatically.  
Switch between charts and data table.  
Generate and download PDF reports.  
View last 5 uploaded datasets.

Desktop Application  
Upload CSV file.  
View charts and summaries.  
Navigate between summary and data table tabs.  
Generate PDF reports.

## API Access

Base URL  
http://localhost:8000/api/

Endpoints  

GET /api/datasets/  
POST /api/datasets/  
GET /api/history/  
GET /api/datasets/{id}/generate_report/

Authentication uses Basic HTTP auth.

Username: admin  
Password: password123  

## Database Schema

EquipmentDataset stores dataset metadata.  
EquipmentData stores individual equipment records.

## Troubleshooting

CORS errors  
Ensure django-cors-headers is installed.  
Ensure CORS_ALLOWED_ORIGINS includes http://localhost:3000.

Port conflicts  

netstat -ano | findstr :8000  
netstat -ano | findstr :3000  
taskkill /PID <PID> /F  

## Running All Components Manually

Terminal 1  
cd backend  
venv\Scripts\activate  
python manage.py runserver  

Terminal 2  
cd frontend-web  
npm start  

Terminal 3  
cd frontend-desktop  
venv\Scripts\activate  
python main.py  

## Deployment Notes

Use PostgreSQL or MySQL in production.  
Set DEBUG to False.  
Use environment variables for secrets.  
Enable HTTPS.  
Use Gunicorn or uWSGI.  
Configure static files and logging.

## License

Educational project for intern screening.
```
