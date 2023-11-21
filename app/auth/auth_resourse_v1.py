from flask import jsonify
from flask_jwt_extended import (
    create_access_token,
    get_jwt_identity,
    jwt_required,
    get_jwt,
    create_refresh_token,
)
from flask_restx import Namespace, Resource, abort
from marshmallow import ValidationError
from werkzeug.exceptions import HTTPException

from app import db
from app.auth.auth_schema import (
    login_request_data,
    login_response_model,
    UserInputSchema,
    user_model,
    user_input_model,
)
from app.models.user import User

auth_namespace = Namespace("auth", description="Auth operations")


@auth_namespace.route("/register")
class UserRegister(Resource):
    @auth_namespace.expect(user_input_model, validate=True)
    @auth_namespace.marshal_with(user_model, as_list=False, code=201, mask=None)
    @auth_namespace.doc(responses={201: "Success", 404: "Invalid credentials"})
    def post(self):
        """Register user"""
        try:
            # Validate and load user data using Marshmallow schema
            data = auth_namespace.payload
            user_data = UserInputSchema().load(data)

            # Extract user data from the validated payload and create a new user instance
            new_user = User(
                username=user_data["username"],
                email=user_data["email"],
                password=user_data["password"],
            )

            # Add the new user to the database and commit the transaction
            db.session.add(new_user)
            db.session.commit()

            # Return the new user data with a 201 status code
            return new_user, 201

        except ValidationError as e:
            # Handle payload validation errors and return a 400 status code with error messages
            abort(400, f"Error validating user data: {str(e.messages)}")

        except HTTPException as e:
            # Handle other exceptions (e.g., database-related errors)
            db.session.rollback()
            abort(e.code, f"Error creating user.")

        except Exception as e:
            abort(500, massage="Internal Server Error")


@auth_namespace.route("/login")
class UserLogin(Resource):
    @auth_namespace.expect(login_request_data, validate=True)
    @auth_namespace.marshal_with(
        login_response_model, as_list=False, code=200, mask=None
    )
    @auth_namespace.doc(responses={200: "Success", 404: "Invalid credentials"})
    @jwt_required(optional=True)
    def post(self):
        """Login user"""

        # TODO user last login

        if get_jwt_identity():
            return jsonify({"message": "User is already logged in"}), 401

        data = auth_namespace.payload

        try:
            user = User.query.filter_by(email=data["email"]).one_or_none()
            if not user or not user.verify_password(data["password"]):
                return {"message": "Invalid email or password"}, 401

            access_token = create_access_token(identity=user.public_id, fresh=True)
            refresh_token = create_refresh_token(identity=user.public_id)
            return {"access_token": access_token, "refresh_token": refresh_token}

        except Exception as e:
            print(f"Error during login: {e}")
            return jsonify({"message": "Internal Server Error"}), 500
