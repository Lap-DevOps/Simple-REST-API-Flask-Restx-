from flask_restx import fields

from app import api

user_activity_model = api.model(
    "User analytic",
    {
        "id": fields.String(description="User ID"),
        "last login": fields.DateTime(description="Last login", dt_format="iso8601"),
        "last api request": fields.DateTime(
            description="Last API request", dt_format="iso8601"
        ),
    },
)

like_stats_model = api.model(
    "Like Statistics",
    {
        "date": fields.String(
            description="Date of the statistics entry", example="2023-11-21"
        ),
        "like_count": fields.Integer(
            description="Number of likes on the given date", example=4
        ),
    },
)

like_stats_response_model = api.model(
    "Like Statistics Response",
    {
        "title": fields.String(
            description="Title of the statistics", example="Likes Statistics"
        ),
        "data": fields.List(fields.Nested(like_stats_model)),
        "total_likes": fields.Integer(description="Total number of likes", example=4),
    },
)
