from marshmallow import Schema, EXCLUDE, ValidationError
from sanic.exceptions import SanicException


class ApiValidationException(SanicException):
    status = 400


class ApiResponseValidationException(SanicException):
    status = 500


class RequestDto:
    __schema__ = Schema

    def __init__(self, data: dict):
        try:
            valid_data = self.__schema__(unknown=EXCLUDE).load(data)
        except ValidationError as error:
            raise ApiValidationException(message=error.messages)
        else:
            self._import(valid_data)

    def _import(self, data: dict):
        for key, value in data.items():
            self.set(key, value)

    def set(self, key, value):
        setattr(key, value)

class ResponseDto:
    __schema__ = Schema

    def __init__(self, obj, many: bool = False):
        if many:
            properties = [self.parse_obj(o) for o in obj]
        else:
            properties = self.parse_obj(obj)

        try:
            self._data = self.__schema__(unknown=EXCLUDE, many=many).load(properties)
        except ValidationError as error:
            raise ApiResponseValidationException(error.messages)

    @staticmethod
    def parse_obj(obj: object) -> dict:
        return {
            prop: value
            for prop in dir(obj)
            if not prop.startswith('_')
                and not prop.endswith('_')
                and not callable(value := getattr(obj, prop))
        }

    def dump(self) -> dict:
        return self._data




