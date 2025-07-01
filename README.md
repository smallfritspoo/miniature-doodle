# minicrud - A Simple CRUD REST API

minicrud is a simple RESTful API built with Flask, SQLAlchemy, and PostgreSQL. It provides basic Create, Read, Update, and Delete (CRUD) operations on data entries, with all requests requiring token-based authentication.

## Features

*   **Flask Framework**: Lightweight and flexible web framework.
*   **SQLAlchemy ORM**: Object Relational Mapper for database interactions.
*   **PostgreSQL Backend**: Robust and scalable relational database.
*   **Token-Based Authentication**: Secure API access using tokens.
*   **Docker Support**: Easy containerization for deployment.
*   **Google Style Python Docstrings**: Well-documented source code.

## Project Structure

```
minicrud/
├── minicrud/
│   ├── __init__.py
│   ├── app.py
│   ├── auth.py
│   ├── config.py
│   ├── database.py
│   └── models.py
├── sql/
│   └── init.sql
├── .env.example
├── Dockerfile
├── README.md
├── requirements.txt
└── wsgi.py
```

## Setup and Installation

### Prerequisites

*   Docker (recommended for easy setup)
*   Python 3.9+
*   PostgreSQL

### 1. Clone the Repository

```bash
git clone https://github.com/your-repo/minicrud.git
cd minicrud
```

### 2. Environment Variables

Create a `.env` file in the root directory of the project based on `.env.example`:

```bash
cp .env.example .env
```

Edit the `.env` file and provide your database connection string and a secret key:

```
DATABASE_URL=postgresql://user:password@host:port/database_name
SECRET_KEY=your_super_secret_key_here
```

**Note**: Replace `user`, `password`, `host`, `port`, and `database_name` with your PostgreSQL credentials. The `SECRET_KEY` should be a strong, randomly generated string.

### 3. Database Setup

Use the `sql/init.sql` script to create the `minicrud` schema, `users` table, and `data` table in your PostgreSQL database. You can execute this script using `psql` or any PostgreSQL client:

```bash
psql -h <host> -p <port> -U <user> -d <database_name> -f sql/init.sql
```

### 4. Running the Application

#### Using Docker (Recommended)

Build the Docker image:

```bash
docker build -t minicrud .
```

Run the Docker container:

```bash
docker run -p 5000:5000 --env-file ./.env minicrud
```

The API will be accessible at `http://localhost:5000`.

#### Local Development (without Docker)

1.  **Create a Python Virtual Environment and Install Dependencies:**

    ```bash
    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
    ```

2.  **Run the Flask Application:**

    Ensure your environment variables from the `.env` file are loaded. You can use a tool like `python-dotenv` or manually set them in your shell.

    ```bash
    # If using python-dotenv (install with: pip install python-dotenv)
    # from dotenv import load_dotenv
    # load_dotenv()

    export DATABASE_URL="postgresql://user:password@host:port/database_name"
    export SECRET_KEY="your_super_secret_key_here"

    flask run --host=0.0.0.0
    ```

The API will be accessible at `http://localhost:5000`.

## API Endpoints

All endpoints require an `x-access-token` header with a valid API token.

### Data Endpoints

*   **`POST /data`**
    *   **Description**: Creates a new data entry.
    *   **Request Body**: `{"text": "Your data text"}`
    *   **Authentication**: Required
    *   **Response**: `{"message": "New data created!"}`

*   **`GET /data`**
    *   **Description**: Retrieves all data entries.
    *   **Authentication**: Required
    *   **Response**: `{"data": [...]}`

*   **`GET /data/<data_id>`**
    *   **Description**: Retrieves a single data entry by ID.
    *   **Authentication**: Required
    *   **Response**: `{"id": ..., "text": ..., "last_modified": ..., "editor": ...}`

*   **`PUT /data/<data_id>`**
    *   **Description**: Updates an existing data entry by ID.
    *   **Request Body**: `{"text": "Updated data text"}`
    *   **Authentication**: Required
    *   **Response**: `{"message": "Data has been updated!"}`

*   **`DELETE /data/<data_id>`**
    *   **Description**: Deletes a data entry by ID.
    *   **Authentication**: Required
    *   **Response**: `{"message": "Data has been deleted!"}`

## Authentication

To authenticate, you need to have a user with an `api_token` in the `users` table. For initial setup, you might need to manually insert a user into the `minicrud.users` table with a generated `api_token`.

Example SQL to insert a user (replace with your desired values):

```sql
INSERT INTO minicrud.users (username, email, password_hash, api_token)
VALUES ('testuser', 'test@example.com', 'hashed_password_here', 'your_generated_api_token');
```

**Note**: In a real-world application, you would have a user registration and login endpoint to generate and manage API tokens securely.

## Contributing

Feel free to fork the repository, open issues, and submit pull requests.

## License

This project is open-source and available under the [MIT License](LICENSE). (You might want to create a LICENSE file if you plan to open source this project.)
