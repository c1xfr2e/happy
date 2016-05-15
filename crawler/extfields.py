# coding: utf-8

from marshmallow import fields
from util import cntext_to_int, cntext_to_float


class ExtField(fields.Field):
    default_error_messages = {
        'invalid': 'Not a valid {type}: [{value}].',
    }

    def __init__(self, *args, **kwargs):
        fields.Field.__init__(self, *args, **kwargs)
        if 'value_on_fail' in kwargs:
            self.value_on_fail = kwargs['value_on_fail']

    def _convert_value(self, value):
        return value

    def _deserialize(self, value, attr, data):
        try:
            result_value = self._convert_value(value)
        except Exception:
            if hasattr(self, 'value_on_fail'):
                return getattr(self, 'value_on_fail')
            else:
                self.fail('invalid', type=self.__class__.__name__, value=value)
        return result_value


class CnNumberInt(ExtField):
    def _convert_value(self, value):
        return cntext_to_int(value)


class CnNumberFloat(ExtField):
    def _convert_value(self, value):
        return cntext_to_float(value)
