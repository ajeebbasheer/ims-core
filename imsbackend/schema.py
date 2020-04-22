from marshmallow import Schema, fields

class CommonSchema(Schema):
  _id = fields.Str()
  id = fields.Str(required=True)
  name = fields.Str(required=True)


class BranchSchema(CommonSchema):
  code = fields.Str(required=True)
  rent = fields.Float()
  uuid = fields.String()
  phone = fields.String()
  email = fields.String()
