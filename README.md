# Product Recommendation Application

This is a FastAPI application that provides a user, product and order API's for the demonstration 
of recommendation system for ecommerce website.

## Requirements

- Python 3.7+
- FastAPI
- Uvicorn

## Installation

1. Clone the repository:

```
git clone https://github.com/your-username/sms_magic.git
cd sms_magic
```

2. Create and activate a virtual environment:

```
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
```

3. Install the dependencies:

```
pip install -r requirements.txt
```

## Running the Application Locally

1. Start the FastAPI application using Uvicorn:

```
uvicorn main:app --reload
```

2. Open your browser and navigate to http://127.0.0.1:8000 to see the application running

## API Documentation

FastAPI automatically generates interactive API documentation:

- OpenAPI: http://127.0.0.1:8000/docs

- ReDoc: http://127.0.0.1:8000/redoc

## Project Structure

```
sms_magic
├── sms_magic_app
├  ├── database.py  # Defines the in-memory database for recommendation system
├  ├── schemas.py   # Defines Pydantic schema for input validation and response model
├  ├── utils.py     # Defines utility functions
├  ├── api.py       # Contains the route definitions
├
├── main.py        # The main entry point of the application
├── requirements.txt # Project dependencies
├── README.md        # Project documentation

```

## Example Usage

To test the API, you can use curl or any API client like Postman:

```
curl -X GET "http://127.0.0.1:8000/api/v1/users/1" -H "accept: application/json"
```
