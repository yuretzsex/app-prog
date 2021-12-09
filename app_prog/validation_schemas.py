from marshmallow import Schema, fields
from marshmallow.validate import Length, Range


class user_schema(Schema):
    username = fields.String(validate=Length(min=4))
    firstName = fields.String(validate=Length(min=3))
    lastName = fields.String(validate=Length(min=3))
    password = fields.String(validate=Length(min=8))
    email = fields.Email()
    phone = fields.Number()
    city = fields.String(validate=Length(min=2))

class announcement_schema(Schema):
    tittle = fields.String(validate=Length(min=4))
    content = fields.String(validate=Length(min=4))
    author = fields.String()
    isLocal = fields.Boolean()

class login_schema(Schema):
    username = fields.String(validate=Length(min=4))
    password = fields.String(validate=Length(min=8))
