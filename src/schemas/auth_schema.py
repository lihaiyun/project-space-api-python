from marshmallow import Schema, fields, validate, pre_load

class UserRegisterSchema(Schema):
    name = fields.Str(
        required=True, 
        validate=[
            validate.Length(max=100),
            validate.Regexp(r"^[a-zA-Z '-,.]+$", 
                error="Name can only contain letters, spaces, apostrophes, hyphens, commas, and periods")
        ]
    )
    email = fields.Email(required=True)
    password = fields.Str(
        required=True, 
        validate=[
            validate.Length(min=8),
            validate.Regexp(r"^(?=.*[a-zA-Z])(?=.*[0-9]).*$", 
                error="Password must contain at least one letter and one number")
        ]
    )

    @pre_load
    def normalize_data(self, data, **kwargs):
        if 'email' in data and data['email']:
            data['email'] = data['email'].lower().strip()
        if 'name' in data and data['name']:
            data['name'] = data['name'].strip()
        if 'password' in data and data['password']:
            data['password'] = data['password'].strip()
        return data

class UserLoginSchema(Schema):
    email = fields.Email(required=True)
    password = fields.Str(
        required=True, 
        validate=[
            validate.Length(min=8),
            validate.Regexp(r"^(?=.*[a-zA-Z])(?=.*[0-9]).*$", 
                error="Password must contain at least one letter and one number")
        ]
    )

    @pre_load
    def normalize_data(self, data, **kwargs):
        if 'email' in data and data['email']:
            data['email'] = data['email'].lower().strip()
        if 'password' in data and data['password']:
            data['password'] = data['password'].strip()
        return data

