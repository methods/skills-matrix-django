**Skills Matrix**

## About this application

### Purpose of this app

This is a Django application for collating and mapping employee skills, making it easier for the organisation and individuals to identify areas of strength and areas requiring further development.  The application also provides a framework for detailing skills required in specific job roles, and for grouping roles together into career paths, making progression more transparent.

### Tech stack

This application utilises:

- Python/Django framework
- jQuery
- SASS

## Getting Started

You need to have Python (3.6.8), PIP and PostgreSQL installed. There are multiple ways to install Python, either download from the official [Python site](https://www.python.org/downloads/) or use the package manager [Homebrew](https://brew.sh/) `brew install python3`. PIP comes installed with Python 3.4(or greater) by default.

To install Postgres you can also use [Homebrew](https://brew.sh/)

```
brew update
brew doctor
brew install postgresql
```

Create a local database

```
CREATE DATABASE skillsmatrix;
```

### Running the site

Create a Python 3.6.8 virtual environment and run the following commands from the root directory of the project:

```
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

You may need to create a secret key to run the service, in which case run the following command:
```
python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'
```
Then copy the secret key generated and run the following command:
```
export SECRET_KEY="insert_secret_key_here"
```

#### Initial access



```

```

There are three user groups in the project: user, admin, and super admin.  The project is currently split into ten apps: admin_user, app, auth_processes, career_paths, common, error, job_roles, skills, super_admin, and user_management.

**admin_user**

Currently contains the dashboard that is visible to all admin or super admin users, directing them to sections of the app that only they can access.

**app**

Contains the main dashboard that is accessible to all users, as well as views for CRUD operations on skills associated with the logged in user.

**auth_processes**

Contains login and logout views and functionality.

**career_paths**

Currently contains a single view without functionality.

**common**

Contains a number of utils for use in mutiple apps, including a custom view class, mixins to check user groups and authentication status, and custom test cases.

**error**

Contains functionality for handling 401 and 403 errors.

**job_roles**

Contains job and competency models, forms and views for handling CRUD operations on these models.  A 'competency' is here defined as a job (e.g. Junior Developer), a skill (e.g. test driven development) and a skill level (e.g. intermediate).

**skills**

Contains skill and user competency models, together with forms and views for handling CRUD operations on these models.  In this case a user competency is defined as a user, a skill and a skill level.

**super_admin**

Contains models and functionality over which super admins have exclusive control - team and skill level.

**user_management**

Contains user model and views and functionality relating to the signup and managing user profile processes.