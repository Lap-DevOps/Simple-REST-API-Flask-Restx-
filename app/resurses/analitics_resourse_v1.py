from datetime import datetime

from flask import request
from flask_jwt_extended import jwt_required
from flask_restx import Namespace, Resource, abort
from sqlalchemy import func

from app import db
from app.extensions import authorizations
from app.models.like import Like
from app.models.user import User
from app.schemas.analytics_schema import (like_stats_response_model,
                                          user_activity_model)

analytics_namespace = Namespace(
    "analytics", description="Analytics", authorizations=authorizations
)


@analytics_namespace.route("/analytic")
class LikeAnalytic(Resource):
    @analytics_namespace.marshal_with(
        like_stats_response_model, as_list=False, code=200, mask=None
    )
    @analytics_namespace.doc(
        responses={200: "Success", 500: "Internal Server Error"},
        security="jsonWebToken",
    )
    @analytics_namespace.doc(
        params={
            "date_from": "Start date for the like statistics (Date format YYYY-MM-DD)",
            "date_to": "End date for the like statistics (Date format YYYY-MM-DD)",
        },
        description="Get like statistics for a specified date range.",
    )
    @jwt_required()
    def get(self):
        """Get like statistics"""
        try:
            # Retrieve parameters from the request
            date_from = request.args.get("date_from")
            date_to = request.args.get("date_to")

            # Convert strings to date objects
            date_from = datetime.strptime(date_from, "%Y-%m-%d")
            date_to = datetime.strptime(date_to, "%Y-%m-%d")

            # Execute a database query with daily aggregation
            result = (
                db.session.query(
                    func.date(Like.created_at).label("date"),
                    func.count().label("like_count"),
                )
                .filter(Like.created_at.between(date_from, date_to))
                .group_by(func.date(Like.created_at))
                .all()
            )

            # Convert the result to a dictionary for the response
            analytics_data = [
                {"date": row.date.strftime("%Y-%m-%d"), "like_count": row.like_count}
                for row in result
            ]

            # Calculate the total number of likes
            total_likes = sum(entry["like_count"] for entry in analytics_data)

            # Create a complete response using the new model
            response_data = {
                "title": "Likes Statistics",
                "data": analytics_data,
                "total_likes": total_likes,
            }

            return response_data
        except ValueError as e:
            abort(404, f"Internal Server Error. {str(e)}")

        except Exception as e:
            abort(500, massage="Internal Server Error")


@analytics_namespace.route("/user/<user_id>")
class UserAnalytic(Resource):
    @analytics_namespace.marshal_with(
        user_activity_model, as_list=False, code=200, mask=None
    )
    @analytics_namespace.doc(
        responses={200: "Success", 404: "User not found"},
        security="jsonWebToken",
        description="Retrieve user analytics, including the timestamp of the last login and the last API request.",
    )
    @jwt_required()
    def get(self, user_id):
        """Retrieve user analytics by user ID."""
        # Retrieve the user from the database based on the provided user ID
        user = User.query.get(user_id)

        # Check if the user exists
        if not user:
            abort(404, "User not found")

        # Prepare the response with user analytics data
        response = {
            "id": user.public_id,
            "last_login": user.last_login.strftime("%Y-%m-%d %H:%M:%S")
            if user.last_login
            else None,
            "last_api_request": user.last_api_request.strftime("%Y-%m-%d %H:%M:%S")
            if user.last_api_request
            else None,
        }

        return response, 200
