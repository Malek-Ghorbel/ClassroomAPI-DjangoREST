# ClassroomAPI-DjangoREST

## Overview

This repository contains the code for the technical test of Funclass. A virtual classroom api that will handle a live class interaction scenario. This manage questions posted during a live class session, where students can post questions.
This application was built with Django Rest Framework
## Features

- User Authentication (Login/Signup)
- Classroom creation
- Student Enrollment in Classrooms
- Posting and Retrieving Questions in classrooms

## Getting Started

### Prerequisites

- Python 3.8 or higher
- Other dependencies in 'requirements.txt'

### Installation

1. **Clone the Repository**

    ```
    git clone https://github.com/Malek-Ghorbel/ClassroomAPI-DjangoREST.git
    cd  ClassroomAPI-DjangoREST
    ```

2. **Set up a virtual environment and install dependencies:**

    ```
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    pip install -r requirements.txt
    ```
   
3.  **Running the Server**

    ```
    python manage.py runserver
    ```
The API will be available at 'http://localhost:8000/'.

## Swagger Documentation

For a detailed and interactive API documentation, navigate to http://localhost:8000/swagger/ after starting the server.

## Testing

To Run the tests for this project:
    ```
    python manage.py test
    ```
