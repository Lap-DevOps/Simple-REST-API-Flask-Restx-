from flask_restx import fields
from marshmallow import Schema, fields as ma_fields, validate

from app import api

# Input model for login  user
login_request_data = api.model(
    "Login form",
    {
        "email": fields.String(description="Email", required=True),
        "password": fields.String(description="Password", required=True),
    },
)

login_response_model = api.model(
    "Login success form",
    {
        "access_token": fields.String(description="access_token", required=True),
        "refresh_token": fields.String(description="Password", required=True),
    },
)

# Detailed user model
user_model = api.model(
    "Detailed User",
    {
        "id": fields.String(description="User ID", required=True),
        "username": fields.String(description="Username", required=True),
        "email": fields.String(description="Email", required=True),
        "member_since": fields.DateTime(description="Member Since", required=True),
        "last_login": fields.DateTime(description="Last_login", required=False),
        "last_api_request": fields.DateTime(
            description="Last_api_request", required=False
        ),
    },
)


class UserInputSchema(Schema):
    username = ma_fields.String(
        required=True,
        validate=validate.Length(
            min=4, error="Username must be at least 4 characters long"
        ),
        error_messages={
            "required": "Username is required",
            "null": "Username cannot be empty",
        },
    )
    email = ma_fields.Email(
        required=True,
        error_messages={
            "required": "Email is required",
            "null": "Email cannot be empty",
            "invalid": "Invalid email format",
        },
    )
    password = ma_fields.String(
        required=True,
        validate=validate.Length(
            min=8, error="Password must be at least 8 characters long"
        ),
        error_messages={
            "required": "Password is required",
            "null": "Password cannot be empty",
        },
    )


# Input model for creating a new user
user_input_model = api.model(
    "Create user",
    {
        "username": fields.String(description="Username", required=True, default=None),
        "email": fields.String(description="Email", required=True),
        "password": fields.String(description="Password", required=True),
    },
)


