from flask import request
from flask_restx import Namespace, Resource
from flask_restx.errors import abort
from marshmallow.exceptions import ValidationError
from werkzeug.exceptions import HTTPException

from app import db
from app.models.user import User
from app.schemas.user_schema import (
    all_users_response_model,
    SimplUserSchema,
    user_input_model,
    user_model,
    UserInputSchema,
)

# Create a namespace for user operations
user_namespace = Namespace("user", description="User operations")


# Define a resource for handling all user-related operations
@user_namespace.route("/")
class AllUsers(Resource):
    # Document the expected query parameters for the 'get' operation
    @user_namespace.doc(params={"limit": "Limit for pagination", "page": "Page number"})
    # Specify the response model and status code for the 'get' operation
    @user_namespace.marshal_with(
        all_users_response_model, as_list=False, code=200, mask=None
    )
    def get(self):
        """Get all users"""
        # Retrieve 'limit' and 'page' from query parameters
        limit = request.args.get("limit", default=None, type=int)
        page = request.args.get("per_page", default=None, type=int)

        try:
            # Paginate the users and retrieve the current page items
            if limit is None:
                # If the per_page parameter is not specified, return all records
                users = User.query.all()
            else:
                # Otherwise, use pagination
                paginated_users = User.query.paginate(page=page, per_page=limit)
                users = paginated_users.items

            # Serialize user data using SimplUserSchema
            users_schema = SimplUserSchema(many=True)
            serialized_users = users_schema.dump(users)

            # Create a response data structure with total count and serialized user data
            total_users = len(serialized_users)
            response_data = {"total": total_users, "data": serialized_users}

            # Return the response data with a 200 status code
            return response_data, 200
        except HTTPException as e:
            # Handle exceptions and return a status code on error
            abort(e.code, f"Error receiving users.")

        except Exception as e:
            abort(500, massage="Internal Server Error")

    # Specify the expected input model, response model, and status code for the 'post' operation
    @user_namespace.expect(user_input_model, validate=True)
    @user_namespace.marshal_with(user_model, as_list=False, code=201, mask=None)
    def post(self):
        """Create a new user."""
        try:
            # Validate and load user data using Marshmallow schema
            data = user_namespace.payload
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
