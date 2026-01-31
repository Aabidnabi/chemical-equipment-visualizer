Chemical Equipment Parameter Visualizer
A hybrid web + desktop application for visualizing and analyzing chemical equipment parameters. The application allows users to upload CSV files containing equipment data and provides interactive charts, summary statistics, and PDF reports.

🏗️ Architecture
This is a hybrid application with three main components:

Backend API (Django REST Framework) - Data processing and storage

Web Frontend (React + Chart.js) - Browser-based interface

Desktop Frontend (PyQt5) - Standalone desktop application

Both frontends connect to the same backend API, providing consistent functionality across platforms.

✨ Features
📊 CSV Upload - Upload equipment data via web or desktop

📈 Interactive Charts - Visualize equipment distribution and parameters

📋 Data Summary - Automatic calculation of statistics (averages, ranges, counts)

📜 History Management - Stores last 5 uploaded datasets

📄 PDF Reports - Generate downloadable analysis reports

🔐 Authentication - Basic HTTP authentication for API security

💾 Database Storage - SQLite database for data persistence

🌐 Cross-Platform - Works on web browsers and as a desktop application

🛠️ Technology Stack
Layer	Technology	Purpose
Backend	Django + Django REST Framework	API development & data processing
Database	SQLite	Data storage
Web Frontend	React + Chart.js	Browser-based visualization
Desktop Frontend	PyQt5 + Matplotlib/PyQtChart	Native desktop application
Data Processing	Python (csv module)	CSV parsing and analysis
PDF Generation	ReportLab	Report generation
📁 Project Structure
text

Copy

Download
chemical-equipment-visualizer/
├── backend/                    # Django backend API
│   ├── config/                # Django configuration
│   ├── equipment_api/         # Main application
│   ├── media/uploads/         # Uploaded CSV files
│   ├── venv/                  # Python virtual environment
│   ├── db.sqlite3            # Database file
│   └── manage.py             # Django management script
├── frontend-web/              # React web application
│   ├── src/components/       # React components
│   ├── public/               # Static files
│   └── package.json          # Node.js dependencies
├── frontend-desktop/          # PyQt5 desktop application
│   ├── venv/                 # Python virtual environment
│   └── main.py               # Desktop application entry point
└── sample_equipment_data.csv  # Sample data for testing
🚀 Quick Start Guide
Prerequisites
Python 3.8 or higher

Node.js 16 or higher

Git

Step 1: Clone and Setup Backend
bash

Copy

Download
# Navigate to backend folder
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On Mac/Linux:
source venv/bin/activate

# Install dependencies
pip install Django==4.2.7 djangorestframework==3.14.0 django-cors-headers==4.2.0 reportlab==4.0.4 PyPDF2==3.0.1

# Apply database migrations
python manage.py migrate

# Create superuser (follow prompts)
python manage.py createsuperuser
# Username: admin
# Password: password123

# Create media directory
mkdir media\uploads

# Start Django server
python manage.py runserver
Backend runs at: http://localhost:8000

Step 2: Setup Web Frontend
bash

Copy

Download
# Open new terminal, navigate to frontend-web
cd frontend-web

# Install Node.js dependencies
npm install

# Start React development server
npm start
Web app runs at: http://localhost:3000

Step 3: Setup Desktop Application
bash

Copy

Download
# Open new terminal, navigate to frontend-desktop
cd frontend-desktop

# Create virtual environment
python -m venv venv

# Activate virtual environment
venv\Scripts\activate

# Install dependencies
pip install PyQt5==5.15.9 requests==2.31.0

# Run desktop application
python main.py
📊 CSV File Format
The application expects CSV files with the following columns:

csv

Copy

Download
Equipment Name,Equipment Type,Flowrate,Pressure,Temperature
Reactor-001,Reactor,150.5,10.2,85.0
Mixer-001,Mixer,200.0,5.5,65.0
Separator-001,Separator,120.3,8.7,75.5
A sample file sample_equipment_data.csv is provided in the project root.

🎯 Usage Guide
Web Application (http://localhost:3000)
Upload CSV: Click "Select CSV File" and choose your equipment data file

View Analysis: Automatic charts and statistics will appear

Explore Data: Switch between charts and data table tabs

Generate Report: Click "Generate PDF" to download analysis report

View History: Recent datasets appear in the left panel

Desktop Application
Launch Application: Run python main.py from frontend-desktop folder

Upload CSV: Click "Select CSV File" button

View Analysis: Charts and summary update automatically

Navigate Tabs: Switch between Summary & Charts and Data Table tabs

Generate Reports: Click "Generate PDF" for reports

API Access
The backend API is accessible at http://localhost:8000/api/

Endpoints:

GET /api/datasets/ - List all datasets

POST /api/datasets/ - Upload new dataset (multipart/form-data)

GET /api/history/ - Get last 5 datasets

GET /api/datasets/{id}/generate_report/ - Generate PDF report

Authentication:
Use Basic HTTP authentication:

Username: admin

Password: password123

🔧 Troubleshooting
Common Issues
CORS Errors

Ensure Django-cors-headers is installed

Check CORS_ALLOWED_ORIGINS includes http://localhost:3000

Port Conflicts

bash

Copy

Download
# Check if ports are in use
netstat -ano | findstr :8000
netstat -ano | findstr :3000

# Kill processes using ports
taskkill /PID [PID] /F
Python Package Installation Failures

bash

Copy

Download
# Try installing with no binary dependencies
pip install --no-binary :all: [package-name]

# Or use specific versions
pip install matplotlib==3.5.3
React Build Errors

bash

Copy

Download
# Clear npm cache and reinstall
npm cache clean --force
rm -rf node_modules package-lock.json
npm install
Running All Components
Option A: Manual (3 terminals)

bash

Copy

Download
# Terminal 1 - Backend
cd backend && venv\Scripts\activate && python manage.py runserver

# Terminal 2 - Web Frontend
cd frontend-web && npm start

# Terminal 3 - Desktop App
cd frontend-desktop && venv\Scripts\activate && python main.py
Option B: Batch Files (Windows)

Create start_all.bat in project root:

batch

Copy

Download
@echo off
start cmd /k "cd backend && venv\Scripts\activate && python manage.py runserver"
timeout /t 5
start cmd /k "cd frontend-web && npm start"
timeout /t 5
start cmd /k "cd frontend-desktop && venv\Scripts\activate && python main.py"
echo All applications started!
📝 API Documentation
Upload CSV
http

Copy

Download
POST /api/datasets/
Content-Type: multipart/form-data
Authorization: Basic YWRtaW46cGFzc3dvcmQxMjM=

file: [CSV_FILE]
Get Dataset History
http

Copy

Download
GET /api/history/
Authorization: Basic YWRtaW46cGFzc3dvcmQxMjM=
Generate PDF Report
http

Copy

Download
GET /api/datasets/{uuid}/generate_report/
Authorization: Basic YWRtaW46cGFzc3dvcmQxMjM=
🗂️ Database Schema
EquipmentDataset: Stores uploaded dataset metadata

EquipmentData: Stores individual equipment records

🔒 Security Notes
Basic authentication is used for API protection

Uploaded files are validated before processing

SQLite database is suitable for development (use PostgreSQL for production)

CORS is configured to allow only specific origins

🚀 Deployment Considerations
For production deployment:

Use Production Database: Replace SQLite with PostgreSQL/MySQL

Set DEBUG to False: In Django settings

Use Environment Variables: For secret keys and credentials

Implement HTTPS: Use SSL certificates

Add Rate Limiting: For API endpoints

Use Production WSGI Server: Gunicorn or uWSGI

Configure Static Files: Use WhiteNoise or CDN

Set Up Logging: For monitoring and debugging

📚 Development
Adding New Features
Extend Models: Add new fields to EquipmentDataset or EquipmentData

Add API Endpoints: Create new views in equipment_api/views.py

Update Frontends: Modify React components or PyQt5 interface

Add Charts: Extend Chart.js or PyQtChart configurations

Testing
bash

Copy

Download
# Backend tests
cd backend
python manage.py test

# Frontend tests (React)
cd frontend-web
npm test
🤝 Contributing
Fork the repository

Create a feature branch

Make your changes

Add tests if applicable

Submit a pull request

📄 License
This project is for educational purposes as part of an intern screening task.

📞 Support
For issues or questions:

Check the troubleshooting section

Ensure all prerequisites are installed

Verify all services are running on correct ports

Review the CSV file format requirements

🎉 Success Criteria Checklist
CSV upload works in both web and desktop applications

Data analysis and statistics are calculated correctly

Charts display equipment distribution and parameter analysis

History of last 5 datasets is maintained

PDF reports can be generated and downloaded

Basic authentication protects API endpoints

Application works as both web and desktop interface

Sample data file is provided for testing

Happy Analyzing! 🧪📊🚀

Intern Screening Task – Hybrid Web + Desktop Application You are required to build a hybrid application that runs both as a Web Application and a Desktop Application. The project focuses on data visualization and analytics for chemical equipment. Project Title: Chemical Equipment Parameter Visualizer (Hybrid Web + Desktop App) Project Overview Create a Web + Desktop application that allows users to upload a CSV file containing a list of chemical equipment with columns such as Equipment Name, Type, Flowrate, Pressure, and Temperature. The Django backend will parse the data, perform analysis, and provide summary statistics via API. Both React (Web) and PyQt5 (Desktop) frontends will consume this API to display data tables, charts, and summaries. Tech Stack (Fixed) Layer Technology Purpose Frontend (Web) React.js + Chart.js Show table + charts Frontend (Desktop) PyQt5 + Matplotlib Same visualization in desktop Backend Python Django + Django REST Framework Common backend API Data Handling Pandas Reading CSV & analytics Database SQLite Store last 5 uploaded datasets Version Control Git & GitHub Collaboration & submission Sample Data sample_equipment_data.csv Sample CSV file provided for testing & demo Key Features Required CSV Upload – Web and Desktop must allow users to upload a CSV file to the backend. Data Summary API – Django API should return total count, averages, and equipment type distribution. Visualization – Display charts using Chart.js (Web) and Matplotlib (Desktop). History Management – Store last 5 uploaded datasets with summary. Generate PDF report and add basic authentication. (Extra) Use the provided sample CSV (sample_equipment_data.csv) for demo and testing.
how to setup tell me from scartch
PS C:\Users\AABID> # Check Python PS C:\Users\AABID> python --version Python 3.13.7 PS C:\Users\AABID> # or PS C:\Users\AABID> python3 --version Python was not found; run without arguments to install from the Microsoft Store, or disable this shortcut from Settings > Apps > Advanced app settings > App execution aliases. PS C:\Users\AABID> PS C:\Users\AABID> # Check pip (Python package manager) PS C:\Users\AABID> pip --version pip 25.3 from C:\Users\AABID\AppData\Local\Programs\Python\Python313\Lib\site-packages\pip (python 3.13) PS C:\Users\AABID> PS C:\Users\AABID> # Check Node.js PS C:\Users\AABID> node --version v20.14.0 PS C:\Users\AABID> PS C:\Users\AABID> # Check npm (Node package manager) PS C:\Users\AABID> npm --version 10.7.0 PS C:\Users\AABID> PS C:\Users\AABID> # Check Git PS C:\Users\AABID> git --version git version 2.47.0.windows.1 PS C:\Users\AABID>
Windows PowerShell Copyright (C) Microsoft Corporation. All rights reserved. Install the latest PowerShell for new features and improvements! https://aka.ms/PSWindows PS F:\chemical-equipment-visualizer> # Navigate to backend folder PS F:\chemical-equipment-visualizer> cd backend PS F:\chemical-equipment-visualizer\backend> PS F:\chemical-equipment-visualizer\backend> # Create virtual environment PS F:\chemical-equipment-visualizer\backend> python -m venv venv PS F:\chemical-equipment-visualizer\backend> PS F:\chemical-equipment-visualizer\backend> # Activate virtual environment PS F:\chemical-equipment-visualizer\backend> .\venv\Scripts\activate .\venv\Scripts\activate : File F:\chemical-equipment-visualizer\backend\venv\Scripts\Activate.ps1 cannot be loaded because running scripts is disabled on this system. For more information, see about_Execution_Policies at https:/go.microsoft.com/fwlink/?LinkID=135170. At line:1 char:1 + .\venv\Scripts\activate + ~~~~~~~~~~~~~~~~~~~~~~~ + CategoryInfo : SecurityError: (:) [], PSSecurityException + FullyQualifiedErrorId : UnauthorizedAccess PS F:\chemical-equipment-visualizer\backend> PS F:\chemical-equipment-visualizer\backend> # You should see (venv) in your prompt
opying pandas\_libs\tslibs\parsing.pyi -> build\lib.win-amd64-cpython-313\pandas\_libs\tslibs copying pandas\_libs\tslibs\parsing.pyx -> build\lib.win-amd64-cpython-313\pandas\_libs\tslibs copying pandas\_libs\tslibs\period.pxd -> build\lib.win-amd64-cpython-313\pandas\_libs\tslibs copying pandas\_libs\tslibs\period.pyi -> build\lib.win-amd64-cpython-313\pandas\_libs\tslibs copying pandas\_libs\tslibs\period.pyx -> build\lib.win-amd64-cpython-313\pandas\_libs\tslibs copying pandas\_libs\tslibs\strptime.pxd -> build\lib.win-amd64-cpython-313\pandas\_libs\tslibs copying pandas\_libs\tslibs\strptime.pyi -> build\lib.win-amd64-cpython-313\pandas\_libs\tslibs copying pandas\_libs\tslibs\strptime.pyx -> build\lib.win-amd64-cpython-313\pandas\_libs\tslibs copying pandas\_libs\tslibs\timedeltas.pxd -> build\lib.win-amd64-cpython-313\pandas\_libs\tslibs copying pandas\_libs\tslibs\timedeltas.pyi -> build\lib.win-amd64-cpython-313\pandas\_libs\tslibs copying pandas\_libs\tslibs\timedeltas.pyx -> build\lib.win-amd64-cpython-313\pandas\_libs\tslibs copying pandas\_libs\tslibs\timestamps.pxd -> build\lib.win-amd64-cpython-313\pandas\_libs\tslibs copying pandas\_libs\tslibs\timestamps.pyi -> build\lib.win-amd64-cpython-313\pandas\_libs\tslibs copying pandas\_libs\tslibs\timestamps.pyx -> build\lib.win-amd64-cpython-313\pandas\_libs\tslibs copying pandas\_libs\tslibs\timezones.pxd -> build\lib.win-amd64-cpython-313\pandas\_libs\tslibs copying pandas\_libs\tslibs\timezones.pyi -> build\lib.win-amd64-cpython-313\pandas\_libs\tslibs copying pandas\_libs\tslibs\timezones.pyx -> build\lib.win-amd64-cpython-313\pandas\_libs\tslibs copying pandas\_libs\tslibs\tzconversion.pxd -> build\lib.win-amd64-cpython-313\pandas\_libs\tslibs copying pandas\_libs\tslibs\tzconversion.pyi -> build\lib.win-amd64-cpython-313\pandas\_libs\tslibs copying pandas\_libs\tslibs\tzconversion.pyx -> build\lib.win-amd64-cpython-313\pandas\_libs\tslibs copying pandas\_libs\tslibs\util.pxd -> build\lib.win-amd64-cpython-313\pandas\_libs\tslibs copying pandas\_libs\tslibs\vectorized.pyi -> build\lib.win-amd64-cpython-313\pandas\_libs\tslibs copying pandas\_libs\tslibs\vectorized.pyx -> build\lib.win-amd64-cpython-313\pandas\_libs\tslibs copying pandas\_libs\window\aggregations.pyi -> build\lib.win-amd64-cpython-313\pandas\_libs\window copying pandas\_libs\window\aggregations.pyx -> build\lib.win-amd64-cpython-313\pandas\_libs\window copying pandas\_libs\window\indexers.pyi -> build\lib.win-amd64-cpython-313\pandas\_libs\window copying pandas\_libs\window\indexers.pyx -> build\lib.win-amd64-cpython-313\pandas\_libs\window UPDATING build\lib.win-amd64-cpython-313\pandas/_version.py set build\lib.win-amd64-cpython-313\pandas/_version.py to '2.0.3' running build_ext building 'pandas._libs.algos' extension error: Microsoft Visual C++ 14.0 or greater is required. Get it with "Microsoft C++ Build Tools": https://visualstudio.microsoft.com/visual-cpp-build-tools/ [end of output] note: This error originates from a subprocess, and is likely not a problem with pip. ERROR: Failed building wheel for pandas Failed to build pandas [notice] A new release of pip is available: 25.3 -> 26.0 [notice] To update, run: C:\Users\AABID\AppData\Local\Programs\Python\Python313\python.exe -m pip install --upgrade pip error: failed-wheel-build-for-install × Failed to build installable wheels for some pyproject.toml based projects ╰─> pandas (venv) PS F:\chemical-equipment-visualizer\backend> (venv) PS F:\chemical-equipment-visualizer\backend> # Create Django project (venv) PS F:\chemical-equipment-visualizer\backend> django-admin startproject config . django-admin : The term 'django-admin' is not recognized as the name of a cmdlet, function, script file, or operable program. Check the spelling of the name, or if a path was included, verify that the path is correct and try again. At line:1 char:1 + django-admin startproject config . + ~~~~~~~~~~~~ + CategoryInfo : ObjectNotFound: (django-admin:String) [], CommandNotFoundException + FullyQualifiedErrorId : CommandNotFoundException (venv) PS F:\chemical-equipment-visualizer\backend> (venv) PS F:\chemical-equipment-visualizer\backend> # Create equipment_api app (venv) PS F:\chemical-equipment-visualizer\backend> python manage.py startapp equipment_api
Install the latest PowerShell for new features and improvements! https://aka.ms/PSWindows PS C:\Users\AABID> # Deactivate virtual environment if active PS C:\Users\AABID> deactivate PS C:\Users\AABID> PS C:\Users\AABID> # Remove the virtual environment PS C:\Users\AABID> Remove-Item -Recurse -Force venv Remove-Item : Cannot find path 'C:\Users\AABID\venv' because it does not exist. At line:1 char:1 + Remove-Item -Recurse -Force venv + ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ + CategoryInfo : ObjectNotFound: (C:\Users\AABID\venv:String) [Remove-Item], ItemNotFoundException + FullyQualifiedErrorId : PathNotFound,Microsoft.PowerShell.Commands.RemoveItemCommand PS C:\Users\AABID> PS C:\Users\AABID> # Create new virtual environment PS C:\Users\AABID> python -m venv venv
PS F:\chemical-equipment-visualizer\backend> # Create new virtual environment PS F:\chemical-equipment-visualizer\backend> python -m venv venv PS F:\chemical-equipment-visualizer\backend> PS F:\chemical-equipment-visualizer\backend> # Activate it (we'll handle the execution policy issue) PS F:\chemical-equipment-visualizer\backend> Set-ExecutionPolicy -ExecutionPolicy Bypass -Scope Process PS F:\chemical-equipment-visualizer\backend> .\venv\Scripts\activate (venv) PS F:\chemical-equipment-visualizer\backend> # First, install Django (venv) PS F:\chemical-equipment-visualizer\backend> pip install Django==4.2.7 Collecting Django==4.2.7 Using cached Django-4.2.7-py3-none-any.whl.metadata (4.1 kB) Collecting asgiref<4,>=3.6.0 (from Django==4.2.7) Using cached asgiref-3.11.0-py3-none-any.whl.metadata (9.3 kB) Collecting sqlparse>=0.3.1 (from Django==4.2.7) Using cached sqlparse-0.5.5-py3-none-any.whl.metadata (4.7 kB) Collecting tzdata (from Django==4.2.7) Using cached tzdata-2025.3-py2.py3-none-any.whl.metadata (1.4 kB) Using cached Django-4.2.7-py3-none-any.whl (8.0 MB) Using cached asgiref-3.11.0-py3-none-any.whl (24 kB) Using cached sqlparse-0.5.5-py3-none-any.whl (46 kB) Using cached tzdata-2025.3-py2.py3-none-any.whl (348 kB) Installing collected packages: tzdata, sqlparse, asgiref, Django Successfully installed Django-4.2.7 asgiref-3.11.0 sqlparse-0.5.5 tzdata-2025.3 [notice] A new release of pip is available: 25.2 -> 26.0 [notice] To update, run: python.exe -m pip install --upgrade pip (venv) PS F:\chemical-equipment-visualizer\backend> (venv) PS F:\chemical-equipment-visualizer\backend> # Check if Django installed (venv) PS F:\chemical-equipment-visualizer\backend> python -m django --version 4.2.7 (venv) PS F:\chemical-equipment-visualizer\backend>
yes working fne both
Make sure Django backend is running i closed thuis how to runn it
got this output
charts are also sjowing
copying lib\matplotlib\backends\web_backend\css\mpl.css -> build\lib.win-amd64-cpython-313\matplotlib\backends\web_backend\css copying lib\matplotlib\mpl-data\images\filesave-symbolic.svg -> build\lib.win-amd64-cpython-313\matplotlib\mpl-data\images copying lib\matplotlib\backends\web_backend\.prettierrc -> build\lib.win-amd64-cpython-313\matplotlib\backends\web_backend copying lib\matplotlib\mpl-data\images\home.png -> build\lib.win-amd64-cpython-313\matplotlib\mpl-data\images running build_ext toml section missing WindowsPath('pyproject.toml') does not contain a tool.setuptools_scm section Extracting /project/freetype/freetype2/2.6.1/freetype-2.6.1.tar.gz Building freetype in build\freetype-2.6.1 error: Microsoft Visual C++ 14.0 or greater is required. Get it with "Microsoft C++ Build Tools": https://visualstudio.microsoft.com/visual-cpp-build-tools/ [end of output] note: This error originates from a subprocess, and is likely not a problem with pip. ERROR: Failed building wheel for matplotlib Failed to build matplotlib [notice] A new release of pip is available: 25.2 -> 26.0 [notice] To update, run: python.exe -m pip install --upgrade pip error: failed-wheel-build-for-install × Failed to build installable wheels for some pyproject.toml based projects ╰─> matplotlib (venv) PS F:\chemical-equipment-visualizer\frontend-desktop>
ok all woeking now , so next time i have to run or check this project how to run both backend frintend as well as desktop
Page not found (404) Request Method: GET Request URL: http://localhost:8000/ Using the URLconf defined in config.urls, Django tried these URL patterns, in this order: admin/ api/ ^media/(?P<path>.*)$ The empty path didn’t match any of these. You’re seeing this error because you have DEBUG = True in your Django settings file. Change that to False, and Django will display a standard 404 page.
good write • README file with setup instructions along with complete setup guide for running your project next time. provide me README file like code i should just copy and past there
