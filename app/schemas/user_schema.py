from flask_restx import fields, Model
from marshmallow import Schema,fields as ma_fields

from app import api


# Модель пользователя
simpl_user_model = api.model('User', {
    'id': fields.String(description='User ID', required=True),
    'username': fields.String(description='Username', required=True),
    'email': fields.String(description='Email', required=True),
    'member_since': fields.DateTime(description='Member Since', required=True),
})

# Модель ответа с пользователями
all_users_response_model = api.model('All users', {
    'total': fields.Integer(description='Total number of users', required=True, readonly=True),
    'data': fields.List(fields.Nested(simpl_user_model), description='List of users', required=True, title="Users:"),
})


class SimplUserSchema(Schema):
    id = ma_fields.String(attribute='public_id')
    username = ma_fields.String(attribute='username')
    email = ma_fields.String(attribute='email')
    member_since = ma_fields.DateTime(attribute='member_since')

