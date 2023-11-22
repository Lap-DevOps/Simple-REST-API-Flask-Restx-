from app import db, jwt
from app.models.user import User


# Method to update user last API request time
@jwt.user_lookup_loader
def user_lookup_callback(_jwt_header, jwt_data):
    identity = jwt_data["sub"]
    user = User.query.filter_by(public_id=identity).one_or_none()
    if user:
        user.update_last_api_request()
        db.session.commit()
    return user
