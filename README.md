---

# Тек Блок - Daily Task Management API  

This project is a FastAPI-based application designed to manage daily tasks with role-based access control and authentication. The API allows users to create, read, update, and delete tasks while ensuring secure access through JWT authentication.  

## Features  
- **User Authentication & Authorization**: JWT-based authentication with role checks for admin and user roles.  
- **Task Management**: CRUD operations for tasks, including bulk upload from Excel files and downloading task reports.  
- **Role-Based Access Control**: Fine-grained access control with role checking for specific routes.  
- **Excel Integration**: Supports uploading tasks from Excel and downloading reports in Excel format.  
- **CORS Support**: Configured CORS to allow requests from any origin.  

---

## Technologies Used  
- **FastAPI**: Web framework for building APIs.  
- **SQLAlchemy**: ORM for database interactions.  
- **OpenPyXL**: Reading and writing Excel files.  
- **PostgreSQL**: Database for storing user and task data.  
- **Docker**: Containerization for development and deployment.  

---

## Prerequisites  
Ensure you have the following installed on your system:  
- **Python 3.10+**  
- **Docker & Docker Compose**  

---

## Installation  

1. **Clone the repository:**  
```bash
git clone https://github.com/dinoru/---.git
cd your-repo-name
```

2. **Create a virtual environment and activate it:**  
```bash
python -m venv venv
source venv/bin/activate # On Windows use `venv\Scripts\activate`
```

3. **Install dependencies:**  
```bash
pip install -r requirements.txt
```

4. **Environment Configuration:**  
Create a `.env` file in the root directory and configure the following:  
```
DATABASE_URL=postgresql+asyncpg://username:password@db_host:db_port/db_name
SECRET_KEY=your_secret_key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

5. **Apply database migrations:**  
```bash
alembic upgrade head
```

---

## Running the Application  

### Locally  
```bash
python main.py
```

Access the API documentation at:  
- **Swagger UI**: `http://127.0.0.1:8000/docs`  
- **ReDoc**: `http://127.0.0.1:8000/redoc`  

### Using Docker  
```bash
docker-compose up --build
```

This will start the FastAPI application along with a PostgreSQL container.  

---

## API Endpoints  

### Authentication  
- `POST /auth/signup`: Create a new user account.  
- `POST /auth/login`: Authenticate user and get access and refresh tokens.  
- `GET /auth/refresh_token`: Get a new access token using the refresh token.  

### User Management  
- `GET /auth/me`: Get the current authenticated user's details.  
- `DELETE /auth/user/{username}`: Delete a user (Admin only).  

### Task Management  
- `GET /task/`: Get all tasks (Admin and User).  
- `GET /task/{task_id}`: Get a task by ID.  
- `POST /task/`: Create a new task.  
- `POST /task/upload`: Upload tasks from an Excel file.  
- `PATCH /task/{task_id}`: Update a task.  
- `DELETE /task/{task_id}`: Delete a task (Admin only).  
- `DELETE /task/clear`: Delete all tasks.  
- `POST /task/download`: Download task reports as Excel.  

---

## Role-Based Access Control  
The API uses role-based access control with the following roles:  
- **Admin**: Full access to all endpoints.  
- **User**: Limited access to view and manage their own tasks.  

---

## Excel File Integration  
The API supports the following Excel functionalities:  
- **Upload**: Upload an Excel file containing tasks with specific columns.  
- **Download**: Download task reports as an Excel file.  

**Note**: Ensure the Excel file follows the required column structure when uploading.  

---

## Running Tests  
Tests can be written using `pytest`. To run the tests:  
```bash
pytest
```

---

## Deployment  
This application can be deployed using Docker. Make sure to set the environment variables in your deployment environment.  

---

## Contributing  
Contributions are welcome!  
1. Fork the repository.  
2. Create a new branch (`feature/new-feature`).  
3. Make your changes and commit them.  
4. Push to your branch (`git push origin feature/new-feature`).  
5. Open a pull request.  

---

## License  
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.  

---

## Contact  
For any inquiries or issues, please contact:  
**Diarra Moustapha**  
- Email: diarra.msa@gmail.com  

---

## Acknowledgments  
- Thanks to the FastAPI community for their amazing work.  
- OpenPyXL for seamless Excel file integration.  

---

Feel free to adjust the content, add your GitHub link, or modify the contact details before publishing it on your repository. If you need any more sections or customization, let me know!
