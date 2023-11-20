from flask import request
from flask_restx import Namespace, Resource

from app.models.user import User
from app.schemas.user_schema import all_users_response_model, SimplUserSchema

user_namespace = Namespace("user", description="User operations")


@user_namespace.route("/")
class AllUsers(Resource):
    @user_namespace.doc(params={"limit": 'limit', "page": 'page'})
    @user_namespace.marshal_with(all_users_response_model, as_list=False, code=200, mask=None)
    def get(self):
        """Get all users"""
        limit = request.args.get('limit', default=None, type=int)
        page = request.args.get('per_page', default=None, type=int)

        try:
            paginated_users = User.query.paginate(page=page, per_page=limit)
            users = paginated_users.items
            users_schema = SimplUserSchema(many=True)
            serialized_users = users_schema.dump(users)
            total_users = len(serialized_users)
            response_data = {"total": total_users, "data": serialized_users}
            return response_data, 200
        except Exception as e:
            print(e)
            return {"message": "Internal Server Error"}, 500
