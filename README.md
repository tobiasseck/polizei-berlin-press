# Polizei Berlin Press

## Overview

Polizei Berlin Press is a web application designed to scrape, store, and display press releases from the Berlin Police Department. This project aims to provide an easy-to-use interface for accessing and analyzing police reports.

## Features

1. Automated scraping of Berlin Police press releases
2. Secure user authentication system
3. Database storage of scraped reports
4. Web interface for browsing and viewing reports
5. API endpoints for programmatic access to the data

## Technology Stack

- Backend: FastAPI (Python)
- Database: SQLModel (SQLAlchemy ORM)
- Frontend: HTML, CSS, JavaScript
- Authentication: JWT (JSON Web Tokens)
- Web Scraping: BeautifulSoup4
- ASGI Server: Uvicorn

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/polizei-berlin-press.git

   cd polizei-berlin-press
   ```

2. Create a virtual environment and activate it:
   ```
   python -m venv venv

   # On Windows
   venv\Scripts\activate

   # On macOS and Linux
   source venv/bin/activate
   ```

3. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

4. Set up environment variables:
   Create a `.env` file in the project root and add the following:
   ```
   DATABASE_URL=sqlite:///./sql_app.db

   SECRET_KEY=your_secret_key_here
   ```

## Usage

1. Start the application:
   ```
   uvicorn app.main:app --reload
   ```

2. Open a web browser and navigate to `http://localhost:8000`

3. Register a new user account or log in with existing credentials

4. Use the web interface to browse police reports or trigger a new scraping process

## Project Structure

The main application code is located in the `app` directory:

```
app/
├── main.py
├── models.py
├── auth.py
├── controller.py
├── scraper.py
├── create_user.py
└── static/
    ├── index.html
    ├── login.html
    └── browse.html
```

- `main.py`: Contains the FastAPI application and route definitions
- `models.py`: Defines the database models using SQLModel
- `auth.py`: Implements the authentication system
- `controller.py`: Handles the scraping logic and database operations
- `scraper.py`: Implements the scraping logic
- `create_user.py`: Creates a new user in the database
- `static/`: Contains HTML (Jinja2) templates for the web interface

## API Endpoints

- `/`: Home page
- `/login`: Login page
- `/browse`: Browse reports page
- `/token`: POST endpoint for obtaining JWT tokens
- `/users/me/`: GET endpoint for retrieving current user information
- `/trigger-scraping`: POST endpoint to initiate the scraping process
- `/reports`: GET endpoint to retrieve all stored reports
- `/reports/{report_id}`: GET endpoint to retrieve a specific report by ID

## Authentication

The application uses JWT for authentication. To access protected endpoints, include the JWT token in the Authorization header:

```
Authorization: username & password --> set through create_user.py
```

For any questions or issues, please open an issue on the GitHub repository.