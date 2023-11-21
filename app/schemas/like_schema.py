from flask_restx import fields

from app import api

like_response_model = api.model(
    "Delete Confirmation",
    {
        "message": fields.String(description="message", required=True),
    },
)
