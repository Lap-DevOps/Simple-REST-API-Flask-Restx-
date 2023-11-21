from flask_jwt_extended import get_jwt_identity, jwt_required
from flask_restx import Namespace, Resource, abort
from werkzeug.exceptions import HTTPException

from app import db
from app.extensions import authorizations
from app.models.like import Like
from app.models.post import Post
from app.schemas.like_schema import like_response_model

like_namespace = Namespace(
    "like", description="Like operations", authorizations=authorizations
)


@like_namespace.route("/<int:post_id>/like")
class AllPosts(Resource):
    @like_namespace.marshal_with(
        like_response_model, as_list=False, code=200, mask=None
    )
    @like_namespace.doc(
        responses={200: "Success", 404: "Post not found"}, security="jsonWebToken"
    )
    @jwt_required()
    def post(self, post_id):
        """Like post"""

        # Receive current user id
        current_user_id = get_jwt_identity()

        try:
            like = Like(user_id=current_user_id, post_id=post_id)
            db.session.add(like)
            db.session.commit()
            return {"message": f"Post with ID {post_id} was liked"}, 200

        except HTTPException as e:
            # Handle exceptions and return a  status code on error
            abort(e.code, f"Error liking Post:")

        except Exception as e:
            abort(500, massage="Internal Server Error")

    @like_namespace.marshal_with(
        like_response_model, as_list=False, code=200, mask=None
    )
    @like_namespace.doc(responses={200: "Success", 404: "Post not found"})
    @jwt_required()
    def delete(self, post_id):
        """Remove a like from a specific post."""

        # Receive current user id
        current_user_id = get_jwt_identity()

        try:
            post = Post.query.get_or_404(post_id)
            if post.author_id != current_user_id:
                abort(403, message=f"Unauthorized: User is not the author of the post")
            like = Like.query.filter_by(
                user_id=current_user_id, post_id=post.id
            ).first()
            if like is None:
                return {"message": "User has not liked this post"}, 404

            db.session.delete(like)
            db.session.commit()
            return {
                "message": f"Post with ID {post_id} was unliked by user {current_user_id}"
            }, 200

        except HTTPException as e:
            abort(e.code, f"Internal Server Error. {str(e)}")

        except Exception as e:
            abort(500, massage="Internal Server Error")
