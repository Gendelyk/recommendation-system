# Recommendation API

## Project Description

This project is a Recommendation API that provides article recommendations based on a given title and user identifier. It uses FastAPI, FAISS for finding similar articles, and SentenceTransformer for generating embeddings.

## Requirements

- Python 3.8+
- PostgreSQL
- Python packages used in the project are listed in `requirements.txt`:

  ```
  fastapi
  uvicorn
  sqlalchemy
  pandas
  sentence-transformers
  faiss-cpu
  python-dotenv
  ```

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/Gendelyk/recommendation-system.git
   cd recommendation-system
   ```

2. Create a virtual environment and activate it:

   ```bash
   python -m venv venv
   source venv/bin/activate  # for Linux and macOS
   venv\Scripts\activate  # for Windows
   ```

3. Install dependencies from `requirements.txt`:

   ```bash
   pip install -r requirements.txt
   ```

4. Set up the database:
   - Create a PostgreSQL database.
   - Create a `.env` file in the root directory of the project and add the following environment variables for configuring the database connection:

     ```env
     DB_USER=
     DB_PASSWORD=
     DB_HOST=
     DB_PORT=
     DB_NAME=
     ```

5. Initialize the database:
   - Use the database initialization function, which will automatically create the required tables by connecting through SQLAlchemy.

## Running the Application

1. Start the FastAPI application:

   ```bash
   uvicorn app.main:app --reload
   ```

   After this, the application will be available at `http://127.0.0.1:8000`.

2. Open the interactive Swagger UI documentation:

   - Go to `http://127.0.0.1:8000/docs` to see all available endpoints and test them.

3. You can also use ReDoc to view the documentation at `http://127.0.0.1:8000/redoc`.

## Endpoints

### 1. **POST /recommend** - Get Recommendations

   **Description**: Returns a list of recommendations based on the given title.

   **Request Parameters**:
   - `user_id` (int): User identifier.
   - `title` (str): Article title or search query.
   - `quantity` (int, optional): Number of recommendations. Default is 3.

   **Example Request**:
   ```json
   {
     "user_id": 1,
     "title": "Crypto trends",
     "quantity": 3
   }
   ```

   **Response**: A list of recommended articles similar to the given title.

### 2. **GET /** - Server Status Check

   **Description**: Returns a message confirming that the server is running.

   **Response**:
   ```json
   {
     "message": "Welcome! The application is running."
   }
   ```

### 3. **POST /search** - Search Posts

   **Description**: Returns a list of posts based on the given search query.

   **Request Parameters**:
   - `query` (str): Text to search for.
   - `quantity` (int, optional): Number of results. Default is 5.

   **Example Request**:
   ```json
   {
     "query": "Crypto",
     "quantity": 5
   }
   ```

   **Response**: A list of posts with titles containing the given keyword.
  
