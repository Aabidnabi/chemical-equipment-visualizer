# Chemical Equipment Parameter Visualizer

A hybrid web and desktop application for visualizing and analyzing chemical equipment parameters.  
The system supports CSV uploads, interactive visualizations, statistical summaries, dataset history, and PDF report generation.

The application uses a shared backend API that serves both a web frontend and a desktop frontend.

---

## Architecture

The system has three core components.

### Backend API
- Django
- Django REST Framework
- Central data processing and storage
- Shared by both frontends

### Web Frontend
- React
- Chart.js
- Runs in a browser

### Desktop Frontend
- PyQt5
- Matplotlib or PyQtChart
- Runs as a standalone desktop application

Both frontends communicate with the same REST API to ensure consistent behavior.

---

## Features

- CSV upload from web and desktop
- Interactive charts for equipment parameters
- Automatic summary statistics
- History of the last 5 uploaded datasets
- PDF report generation
- Basic HTTP authentication
- SQLite database for persistence
- Cross platform support

---

## Technology Stack

| Layer | Technology | Purpose |
|-----|-----------|---------|
| Backend | Django, Django REST Framework | API and data processing |
| Database | SQLite | Data storage |
| Web Frontend | React, Chart.js | Browser visualization |
| Desktop Frontend | PyQt5, Matplotlib or PyQtChart | Desktop visualization |
| Data Processing | Python csv module | CSV parsing |
| PDF Generation | ReportLab | Report creation |

---

## Screenshots

<img width="1908" height="879" alt="Screenshot 2026-01-31 160003" src="https://github.com/user-attachments/assets/21401732-80cb-4fca-b8d7-4f0867d24837" />

<img width="1919" height="866" alt="Screenshot 2026-01-31 192007" src="https://github.com/user-attachments/assets/70088abe-9dbe-4404-857a-ae50128be2cb" />


<img width="1403" height="834" alt="Screenshot 2026-01-31 154742" src="https://github.com/user-attachments/assets/da555d3a-6c0e-4395-9a2b-a88a58ab69b4" />

<img width="1917" height="899" alt="Screenshot 2026-01-31 160020" src="https://github.com/user-attachments/assets/6985ca5f-b24f-497a-ab41-677ba6e6651c" />

<img width="1919" height="858" alt="Screenshot 2026-01-31 160041" src="https://github.com/user-attachments/assets/8a98e96f-8c43-4d3d-8df2-7fdb47ca5dca" />


<img width="1879" height="749" alt="Screenshot 2026-01-31 160032" src="https://github.com/user-attachments/assets/0791c5ba-4dd9-445f-82c4-012cce5ae00c" />
## Project Structure
```cmd
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
```
---

🚀 Quick Start (One-Time Setup)
Step 1: Backend Setup
```cmd
cd backend
```
# Create virtual environment
```cmd
python -m venv venv
```
# Activate (Windows)
```cmd
venv\Scripts\activate
```
# Install packages
```cmd
pip install Django==4.2.7 djangorestframework==3.14.0 django-cors-headers==4.2.0 reportlab==4.0.4 PyPDF2==3.0.1
```
# Setup database
```cmd
python manage.py migrate
```
# Create admin user 
```cmd
python manage.py createsuperuser
```
# Create uploads folder
```cmd
mkdir media\uploads
```

Step 2: Web Frontend Setup
```cmd
cd frontend-web
```
# Install dependencies
```cmd
npm install
```
Step 3: Desktop App Setup
```cmd
cd frontend-desktop
```
# Create virtual environment
```cmd
python -m venv venv
```
# Activate
```cmd
venv\Scripts\activate
```
# Install packages
```cmd
pip install PyQt5==5.15.9 requests==2.31.0
```
## How to Run
Method 1: Manual (3 Terminals)

Terminal 1: Start Backend
```bash
cd F:\chemical-equipment-visualizer\backend
venv\Scripts\activate
python manage.py runserver
```
Backend running: http://localhost:8000

Terminal 2: Start Web App
```bash
cd F:\chemical-equipment-visualizer\frontend-web
npm start
```
Web app opens: http://localhost:3000

Terminal 3: Start Desktop App
```bash
cd F:\chemical-equipment-visualizer\frontend-desktop
venv\Scripts\activate
python main.py
```
 Desktop app opens as window

## 🔗 Application URLs & Access
- Application	URL
- Backend API	http://localhost:8000	
- Admin Panel	http://localhost:8000/admin	
- Web App	http://localhost:3000
- Desktop App	Run python main.py	

## API Endpoints:
- GET /api/datasets/ - List datasets
- POST /api/datasets/ - Upload CSV
- GET /api/history/ - Get history
- GET /api/datasets/{id}/generate_report/ - PDF report

## How to Use
- Web Application (http://localhost:3000)
- Click "Select CSV File"
- Choose your CSV file
- View automatic charts & statistics
- Click "Generate PDF" for report
- View history in left panel


## Desktop Application
- Click "Select CSV File" button
- Choose CSV file
- View charts in "Summary & Charts" tab
- See raw data in "Data Table" tab
- Generate PDF reports

## Both interfaces:
- Upload same CSV to see consistent results
- History shared between both apps
- Same backend API serves both


## Database Schema
EquipmentDataset: Stores uploaded dataset metadata

EquipmentData: Stores individual equipment records

## 🔒 Security Notes
Basic authentication is used for API protection

Uploaded files are validated before processing

SQLite database is suitable for development (use PostgreSQL for production)

CORS is configured to allow only specific origins

🤝 Contributing
Fork the repository

Create a feature branch

Make your changes

Add tests if applicable

Submit a pull request

📄 License
This project is for educational purposes.



















