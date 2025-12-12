# FastAPI Portfolio Web Application

This project is a personal portfolio web application developed using the FastAPI framework. It showcases various projects, skills, and provides a contact form for inquiries. The application utilizes JSON file storage for data management, making it lightweight and easy to maintain.

## Table of Contents

1. [Project Structure](#project-structure)
2. [Installation](#installation)
3. [Usage](#usage)
4. [Features](#features)
5. [Contributing](#contributing)
6. [License](#license)

## Project Structure

```
my-portfolio
├── app                   # Main application code
│   ├── __init__.py
│   ├── main.py          # Entry point of the application
│   ├── models           # Pydantic models for data validation
│   ├── routes           # API routes for the application
│   ├── services         # Utility functions and services
│   └── utils            # Helper functions
├── data                 # JSON files for data storage
├── static               # Static files (CSS, JS, images)
├── templates            # HTML templates for rendering
├── tests                # Unit tests for the application
├── requirements.txt     # Project dependencies
├── runtime.txt          # Python version for deployment
├── render.yaml          # Render deployment configuration
├── .env.example         # Example environment variables
├── .gitignore           # Files to ignore in Git
└── README.md            # Project documentation
```

## Installation

1. Clone the repository:

   ```
   git clone <repository-url>
   cd my-portfolio
   ```

2. Create a virtual environment:

   ```
   python -m venv venv
   ```

3. Activate the virtual environment:

   - On Windows:
     ```
     venv\Scripts\activate
     ```
   - On macOS/Linux:
     ```
     source venv/bin/activate
     ```

4. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

## Usage

### Local Development

```
uvicorn app.main:app --reload
```

Visit `http://127.0.0.1:8000` in your browser.

### Production Deployment (Render)

1. Create a new Web Service on Render
2. Connect your GitHub/GitLab repository
3. Use the following settings:
   - Runtime: Python 3
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `gunicorn app.main:app`
4. Set environment variables:
   - `PORT`: 8000
   - `PYTHON_VERSION`: 3.9.13

## Features

- Dynamic portfolio sections (About, Projects, Skills, Contact)
- Admin interface for content management
- User authentication for admin access
- Responsive design with CSS styling
- JSON file storage for easy data management

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any improvements or features.

## License

This project is licensed under the MIT License. See the LICENSE file for details.
