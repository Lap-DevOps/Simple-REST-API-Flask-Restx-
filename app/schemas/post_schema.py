from flask_restx import fields
from marshmallow import Schema
from marshmallow import fields as ma_fields
from marshmallow import validate

from app import api


class ListCount(fields.Integer):
    def output(self, key, obj, *args, **kwargs):
        return int(len(obj.likes))


# Post model for simplified representation
simpl_post_model = api.model(
    "Post",
    {
        "id": fields.String(description="User ID", required=True),
        "title": fields.String(description="Post title", required=True),
        "author": fields.String(description="Post author", required=True),
        "date_posted": fields.DateTime(description="Date_posted", required=True),
    },
)

# Detailed post model
post_model = api.model(
    "Detailed Post",
    {
        "id": fields.String(description="User ID", required=True),
        "title": fields.String(description="Post title", required=True),
        "content": fields.String(description="Post content", required=True),
        "slug": fields.String(description="Post slug", required=True),
        "author_id": fields.String(description="Post author", required=True),
        "date_posted": fields.DateTime(description="Date_posted", required=True),
        "likes": ListCount(description="Likes", required=True),
    },
)

# Response model for all posts
all_posts_response_model = api.model(
    "All Posts",
    {
        "total": fields.Integer(description="Total number of posts", required=True),
        "data": fields.List(
            fields.Nested(simpl_post_model),
            description="List of posts",
            required=True,
            title="Posts:",
        ),
    },
)

post_input_model = api.model(
    "Create post",
    {
        "title": fields.String(description="Title", required=True),
        "content": fields.String(description="Content", required=True),
    },
)

delete_confirmation_model = api.model(
    "Delete Confirmation",
    {
        "message": fields.String(description="message", required=True),
    },
)


class SimplPostSchema(Schema):
    id = ma_fields.String(attribute="id")
    title = ma_fields.String(attribute="title")
    author = ma_fields.String(attribute="author.public_id")
    date_posted = ma_fields.DateTime(attribute="date_posted")


class PostInputSchema(Schema):
    title = ma_fields.String(
        required=True,
        validate=validate.Length(min=4, error="Title must be at least 4 characters long"),
        error_messages={
            "required": "Title is required",
            "null": "Title cannot be empty",
        },
    )
    content = ma_fields.String(
        required=True,
        validate=validate.Length(min=4, error="Content must be at least 4 characters long"),
        error_messages={
            "required": "Title is required",
            "null": "Title cannot be empty",
        },
    )
