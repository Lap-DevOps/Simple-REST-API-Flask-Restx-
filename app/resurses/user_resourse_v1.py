from flask import request
from flask_jwt_extended import jwt_required
from flask_restx import Namespace, Resource
from flask_restx.errors import abort
from werkzeug.exceptions import HTTPException

from app.models.user import User
from app.schemas.user_schema import SimplUserSchema, all_users_response_model

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
    @jwt_required()
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
            abort(400, massage="Internal Server Error")
