from marshmallow import Schema, fields, validate, pre_load

class OwnerSchema(Schema):
    id = fields.Str(dump_only=True)
    name = fields.Str(dump_only=True)
    email = fields.Email(dump_only=True)

class ProjectSchema(Schema):
    id = fields.Str(dump_only=True)
    name = fields.Str(required=True, validate=validate.Length(min=3, max=100))
    description = fields.Str(required=False, allow_none=True, validate=validate.Length(max=500))
    dueDate = fields.Date(required=True)
    status = fields.Str(required=True, validate=validate.OneOf(["not-started", "in-progress", "completed"]))
    imageId = fields.Str(required=False, allow_none=True, validate=validate.Length(max=100))
    imageUrl = fields.Str(required=False, allow_none=True, validate=validate.Length(max=200))
    owner = fields.Nested(OwnerSchema, required=False, allow_none=True, dump_only=True)
    createdAt = fields.DateTime(dump_only=True)
    updatedAt = fields.DateTime(dump_only=True)

class ProjectInputSchema(Schema):
    name = fields.Str(required=True, validate=validate.Length(min=3, max=100))
    description = fields.Str(required=False, allow_none=True, validate=validate.Length(max=500))
    dueDate = fields.Date(required=True)
    status = fields.Str(required=True, validate=validate.OneOf(["not-started", "in-progress", "completed"]))
    imageId = fields.Str(required=False, allow_none=True, validate=validate.Length(max=100))
    imageUrl = fields.Str(required=False, allow_none=True, validate=validate.Length(max=200))
    owner = fields.Str(required=False, allow_none=True)  # User ID for input

    @pre_load
    def normalize_data(self, data, **kwargs):
        # Trim whitespace from string fields
        if 'name' in data and data['name']:
            data['name'] = data['name'].strip()
        if 'description' in data and data['description']:
            data['description'] = data['description'].strip()
        return data
