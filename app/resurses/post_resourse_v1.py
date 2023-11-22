from flask import request
from flask_jwt_extended import get_jwt_identity, jwt_required
from flask_restx import Namespace, Resource
from flask_restx.errors import abort
from marshmallow.exceptions import ValidationError
from sqlalchemy import desc
from werkzeug.exceptions import HTTPException

from app import db
from app.models.post import Post
from app.schemas.post_schema import (
    PostInputSchema,
    SimplPostSchema,
    all_posts_response_model,
    delete_confirmation_model,
    post_input_model,
    post_model,
)

post_namespace = Namespace("post", description="Post operations")


@post_namespace.route("/")
class AllPosts(Resource):
    # Document the expected query parameters for the 'get' operation
    @post_namespace.doc(
        params={"limit": "Limit for pagination", "page": "Page number"},
        security="jsonWebToken", description="Endpoint to retrieve all posts with optional pagination."
    )
    # Specify the response model and status code for the 'get' operation
    @post_namespace.marshal_with(
        all_posts_response_model, as_list=False, code=200, mask=None
    )
    @jwt_required()
    def get(self):
        """Get all posts"""
        # Retrieve 'limit' and 'page' from query parameters
        limit = request.args.get("limit", default=None, type=int)
        page = request.args.get("per_page", default=None, type=int)

        try:
            # Paginate the posts and retrieve the current page items
            if limit is None:
                # If the per_page parameter is not specified, return all records
                posts = Post.query.order_by(desc(Post.date_posted)).all()

            else:
                # Otherwise, use pagination
                paginated_posts = Post.query.order_by(desc(Post.date_posted)).paginate(
                    page=page, per_page=limit
                )
                posts = paginated_posts.items

            # Serialize post data using SimplPostSchema
            posts_schema = SimplPostSchema(many=True)
            serialized_posts = posts_schema.dump(posts)

            # Create a response data structure with total count and serialized post data
            total_posts = len(serialized_posts)
            response_data = {"total": total_posts, "data": serialized_posts}

            # Return the response data with a 200 status code
            return response_data, 200
        except HTTPException as e:
            # Handle exceptions and return a 500 status code on error
            abort(e.code, f"Error creating Post.")

        except Exception as e:
            abort(500, massage="Internal Server Error")

    @post_namespace.expect(post_input_model, validate=True)
    @post_namespace.marshal_with(post_model, as_list=False, code=201, mask=None)
    @post_namespace.doc(
        responses={200: "Success", 404: "Post not found"},
        security="jsonWebToken",  description="Endpoint to create a new post.",
    )
    @jwt_required()
    def post(self):
        """Create a new post."""
        try:
            # Validate and load post data using Marshmallow schema
            data = post_namespace.payload
            post_data = PostInputSchema().load(data)

            # Receive current user id
            current_user_id = get_jwt_identity()

            # Extract post data from the validated payload and create a new post instance
            new_post = Post(
                title=post_data["title"],
                content=post_data["content"],
                author_id=current_user_id,
            )

            # Add the new post to the database and commit the transaction
            db.session.add(new_post)
            db.session.commit()

            # Return the new post data with a 201 status code
            return new_post, 201

        except ValidationError as e:
            # Handle payload validation errors and return a 400 status code with error messages
            abort(400, f"Error validating post data: {str(e.messages)}")

        except HTTPException as e:
            # Handle other exceptions (e.g., database-related errors)
            db.session.rollback()
            abort(e.code, f"Error creating Post.")

        except Exception as e:
            abort(400, massage="Internal Server Error")


@post_namespace.route("/<int:post_id>")
class PostResource(Resource):
    @post_namespace.marshal_with(post_model, as_list=False, code=200, mask=None)
    @post_namespace.doc(
        responses={200: "Success", 404: "Post not found"},
        security="jsonWebToken", description="Get details of a specific post by ID."
    )
    @jwt_required()
    def get(self, post_id):
        """Get a specific post by ID."""
        try:
            post = Post.query.get_or_404(
                post_id, description=f"Post with ID {post_id} not found"
            )
            return post, 200
        except Exception as e:
            abort(e.code, e)

    @post_namespace.expect(post_input_model, validate=True)
    @post_namespace.marshal_with(post_model, as_list=False, code=200, mask=None)
    @post_namespace.doc(
        responses={200: "Success", 404: "Post not found"},
        security="jsonWebToken", description="Update a specific post by ID.",
    )
    @jwt_required()
    def put(self, post_id):
        """Update a specific post by ID."""
        try:
            # Validate and load post data using Marshmallow schema
            data = post_namespace.payload
            post_data = PostInputSchema().load(data)

            # Retrieve the post by ID or return a 404 error if not found
            post = Post.query.get_or_404(
                post_id, description=f"Post with ID {post_id} not found"
            )

            # Update post data
            post.title = post_data.get("title", post.title)
            post.content = post_data.get("content", post.content)

            # Commit changes to the database
            db.session.commit()

            # Return the updated post with a 200 status code
            return post, 200

        except ValidationError as e:
            # Handle payload validation errors and return a 400 status code with error messages
            abort(400, f"Error validating post data: {str(e.messages)}")

        except HTTPException as e:
            # Handle exceptions and return a 500 status code on error
            print(f"Error updating post: {str(e)}")
            abort(e.code, f"Error updating Post.")

        except Exception as e:
            abort(400, massage="Internal Server Error")

    @post_namespace.marshal_with(
        delete_confirmation_model, as_list=False, code=200, mask=None
    )
    @post_namespace.doc(
        responses={200: "Success", 404: "Post not found"},
        security="jsonWebToken", description="Delete a specific post by ID."
    )
    @jwt_required()
    def delete(self, post_id):
        """Delete a specific post by ID."""
        try:
            # Retrieve the post by ID
            post = Post.query.get_or_404(post_id)
            # Delete the post from the database
            db.session.delete(post)
            db.session.commit()

            # Return a success message with a 200 status code
            return {"message": f"Post with ID {post_id} deleted successfully"}, 200

        except HTTPException as e:
            # Handle exceptions and return a 404 status code on error
            abort(e.code, f"Error deleting Post:")

        except Exception as e:
            abort(400, massage="Internal Server Error")
