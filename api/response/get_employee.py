from marshmallow import Schema, fields

from api.base import RequestDto, ResponseDto


class ResponseGetEmployeeDtoSchema(Schema):
    eid = fields.Int(required=True, allow_none=False)


class ResponseGetEmployeeDto(ResponseDto, ResponseGetEmployeeDtoSchema):
    __schema__ = ResponseGetEmployeeDtoSchema