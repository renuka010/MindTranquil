# MindTranquil

## Overview

MindTranquil is a personal meditation application made using Django. It features registration and login functionality, allowing users to set meditation time and track their meditation habits. Unlike other meditation apps with excessive features, MindTranquil focuses on creating a distraction-free environment for meditation and easy habit tracking. The application is designed to be used on both desktop and mobile devices.



https://github.com/renuka010/MindTranquil/assets/72569696/502f31d5-7010-4698-a4bd-fc3584202689




## Features

- User registration and authentication
- Customizable Music selection for each session
- Mediatation and Breathing session stats feature
- Integrated Celery beat with RabbitMQ for automated tasks.
- Utilized Django Rest Framework to implement REST APIs.

## Tech Stack

- Backend: Django
- Database: PostgreSQL
- Frontend: HTML/CSS, JavaScript
- Styling: TailwindCSS
- Background Tasks: RabbitMQ with Celery

## Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/renuka010/MindTranquil.git
    ```
2. Change into the project directory:
    ```bash
    cd MindTranquil
    ```
3. Create and Activate the virtual environment:
    ```bash
    python3 -m venv venv  # Create
    venv\Scripts\activate    # Activate
    ```
4. Install the dependencies:
    ```bash
    pip install -r requirements.txt
    ```
5. Create a `.env` file with database details.
6. Run the server:
    ```bash
    python manage.py runserver
    ```
7. Run Celery worker and beat
    ```bash
    celery -A tasks worker --loglevel=INFO
    celery -A tasks beat --loglevel=info
    ```
8. Access the application in your browser at http://localhost:8000
   
## Future Scope

The application is highly scalable. Following are the future scope of this application.
- Setting reminders to get notified.
- Adding few guided meditation sessions for beginners.

## License

Licensed under MIT License.

## Contributing

Contributions are welcome! If you'd like to contribute, please submit a pull request or open an issue with your proposed changes or bug reports.
