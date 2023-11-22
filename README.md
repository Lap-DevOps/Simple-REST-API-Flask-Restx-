#  Social Media API

The Social Media API is a simple RESTful API built using Flask-RESTX, featuring user registration, 
CRUD operations for posts, a like mechanism, JSON Web Token (JWT) authentication, Swagger documentation, 
data validation with Marshmallow, and serialization/deserialization processes.

## Key Features:

1. **User Registration:**
   - Users can register with a unique username, email, and password.

2. **Post Operations:**
   - Create, read, update, and delete posts.

3. **Like Mechanism:**
   - Users can like and unlike posts.

4. **JWT Authentication:**
   - JSON Web Tokens are used to authenticate and authorize users.

5. **Swagger Documentation:**
   - Explore and interact with the API using Swagger UI.

6. **Data Validation (Marshmallow):**
   - Ensure data integrity through validation using the Marshmallow library.

7. **Serialization/Deserialization:**
   - Transform complex data types to and from Python objects using serialization/deserialization.
8. **Provide some analytics routes**
   - Simple analytic routes for likes and user 

## How to Use:

1. **Run the Application:**
   - Start the application using Flask's development server or Gunicorn.

2. **Access Swagger UI:**
   - Navigate to [http://127.0.0.1:5000/swagger](http://127.0.0.1:5000/swagger) to interact with the API using Swagger documentation.

3. **Register a User:**
   - Create a new user by making a POST request to the `/auth/register` endpoint.

4. **Explore CRUD Operations:**
   - Utilize CRUD operations for posts at the `/post` endpoint.

5. **Like and Unlike Posts:**
   - Interact with the like mechanism by sending requests to the `/post/{post_id}/like` endpoint.

6. **Secure Access with JWT:**
   - Obtain and use JWTs for secure access to protected endpoints.

7. **Data Validation and Serialization:**
   - Ensure valid data input through Marshmallow's validation and handle data transformation using serialization/deserialization.

Enjoy using the Social Media API for your basic social media functionality needs!

# How to run
## Setting up a Virtual Environment

1. **Install Virtualenv:**

    ```bash
    pip install virtualenv
    ```

2. **Create a Virtual Environment:**

    ```bash
    virtualenv venv
    ```

3. **Activate the Virtual Environment:**

    - On Windows:

        ```bash
        .\venv\Scripts\activate
        ```

    - On macOS/Linux:

        ```bash
        source venv/bin/activate
        ```

## Copying the Project

1. **Clone the Repository:**

    ```bash
    git clone https://github.com/Lap-DevOps/StarNavy_test_task.git
    ```

2. **Change Directory to the Project:**

    ```bash
    cd your-repository
    ```

3. **Install Dependencies:**

    ```bash
    pip install -r requirements.txt
    ```
# Before Running the Application

If you wish to use a custom configuration, create a file named `.env` in the project root directory and populate it with the desired settings. Here is an example:

```plaintext
# .env file

FLASK_ENV='development'
SECRET_KEY='hard to guess string'

# PRODUCTIONS Config
PROD_DATABASE_USER=admin               # user name
PROD_DATABASE_PASSWORD=passwoord       # user password          
PROD_DATABASE_HOST=localhost           # host address 
PROD_DATABASE_PORT=5432                # database port
PROD_DATABASE_NAME=starnavi_db         # data base port
```


# Running the Application

To start the application, you can use either Flask's built-in development server or Gunicorn.

1. **Using Flask's Development Server:**

    ```bash
    flask run
    ```

   This command will start the development server. Visit [http://127.0.0.1:5000/](http://127.0.0.1:5000/) in your browser to access the application.


2. **Using Gunicorn:**

    Install Gunicorn if you haven't already:

    ```bash
    pip install gunicorn
    ```

    Then, run the application with Gunicorn:

    ```bash
    gunicorn -w 4 -b 0.0.0.0:5000 wsgi:app
    ```

   Access the application at [http://127.0.0.1:5000/](http://127.0.0.1:5000/) after Gunicorn starts.

Choose the method that suits your needs, and enjoy using the application!


1. **Run the Media Generator:**

    ```bash
    python -m SocialMediaGeneratorBot.MediaGenerator
    ```

2. **Open Browser to View Posts:**



Open Swagger UI to Interact with the API:

Once the script execution is complete, navigate to [http://127.0.0.1:5000/swagger](http://127.0.0.1:5000/swagger) in your browser. Here, you can explore and interact with the API using Swagger UI.

Feel free to test different endpoints and functionalities provided by the API.


---

Feel free to modify the instructions based on the specifics of your project, such as the actual repository URL and the name of your main script or application. Additionally, you might want to include information about any configuration files or environment variables that need to be set before running the script.
