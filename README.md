# Smartiqa

Smartiqa is a comprehensive educational platform that provides various features to facilitate online learning and teaching. It is built using Django, a high-level Python Web framework.

## Features

1. **User Authentication**: The platform supports user registration and login functionality. It provides separate signup and login pages for users and instructors. It also supports social login via Google.

2. **Course Management**: Instructors can create and manage courses. Each course has a dedicated page displaying course details. Users can view all available courses and their details.

3. **Attendance Management**: The platform provides an attendance management system where attendance can be added either manually or through an Excel or CSV file. It also supports facial recognition for attendance.

4. **Online Test**: The platform supports online testing. It provides a test page where users can take tests. The test page includes instructions and rules for the test. It also includes an AI cheating detection system to ensure the integrity of the tests.

5. **User Profile**: Each user has a profile page where they can view and update their profile details.

6. **User Settings**: Users can update their settings, including linking their account with Google.

7. **Online Courses**: The platform provides a feature to view online courses from different organizations. Users can search for courses by course name or organization.

8. **Themes**: The platform supports light and dark themes. Users can switch between these themes according to their preference.

9. **Responsive Design**: The platform is designed to be responsive and works well on different devices and screen sizes.

10. **Security**: The platform uses Django's built-in security features to protect against common attacks like Cross-Site Scripting (XSS), Cross-Site Request Forgery (CSRF), and SQL Injection.

## Installation

To install dependencies, run the following command:
```commandline
pip install -r requirements.txt
```

## Database Configuration

To configure the database, run the following commands:
```commandline
python manage.py makemigrations
python manage.py migrate
```

## Superuser Creation

To create a superuser, run the following command:
```commandline
python manage.py createsuperuser
```

## Live Deployment

You can view the live deployment of the project [here](https://smartiqa.pythonanywhere.com/).

## Video

You can view a video demonstration of the project [here](https://drive.google.com/file/d/1lCzEpWQqOiwyafmwArWc_4QNYE5lUSKk/view?usp=share_link).
