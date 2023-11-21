from flask_restx import fields
from marshmallow import Schema, fields as ma_fields, validate
from app import api

# User model for simplified representation
simpl_user_model = api.model(
    "User",
    {
        "id": fields.String(description="User ID", required=True),
        "username": fields.String(description="Username", required=True),
        "email": fields.String(description="Email", required=True),
        "member_since": fields.DateTime(description="Member Since", required=True),
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

# Response model for all users
all_users_response_model = api.model(
    "All Users",
    {
        "total": fields.Integer(
            description="Total number of users", required=True, readonly=True
        ),
        "data": fields.List(
            fields.Nested(simpl_user_model),
            description="List of users",
            required=True,
            title="Users:",
        ),
    },
)


class SimplUserSchema(Schema):
    id = ma_fields.String(attribute="public_id")
    username = ma_fields.String(attribute="username")
    email = ma_fields.String(attribute="email")
    member_since = ma_fields.DateTime(attribute="member_since")


# Input model for creating a new user
user_input_model = api.model(
    "Create user",
    {
        "username": fields.String(description="Username", required=True, default=None),
        "email": fields.String(description="Email", required=True),
        "password": fields.String(description="Password", required=True),
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
