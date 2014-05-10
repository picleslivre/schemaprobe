
__all__ = ['ensure', 'JsonProbe']

import functools
import json
try:
    import jsonschema
except ImportError:
    jsonschema = None
try:
    import requests
except ImportError:
    requests = None


__version__ = '0.1'


class JsonProbe:
    """
    An instance that knows how to perform validations against json-schema.
    """
    _jsonschema = jsonschema

    def __init__(self, schema):
        """
        :param schema: json-schema as json-encoded text or python datastructures.
        """
        if self._jsonschema is None:
            raise TypeError('Missing dependency `jsonschema`.')

        self.schema = self._normalize_input(schema)

    def validate(self, input):
        """
        Validate `input` agains the given schema.

        :param input: json-encoded text or python datastructures.
        :returns: boolean
        """
        data = self._normalize_input(input)

        try:
            jsonschema.validate(data, self.schema)
        except self._jsonschema.ValidationError:
            return False
        else:
            return True

    def _normalize_input(self, input):
        """
        Always return python datastructures.

        :param input: json-encoded text or python datastructures.
        """
        if isinstance(input, str):
            return json.loads(input)
        else:
            return input


def ensure(probe):
    """
    Decorator that asserts the returned value is valid against `probe`.
    """
    def ensure_decorator(f):
        @functools.wraps(f)
        def wrapper(*args, **kwargs):
            result = f(*args, **kwargs)
            if probe.validate(result):
                return result
            else:
                raise TypeError('Returned data does not conform with the given schema.')
        return wrapper
    return ensure_decorator


class TestCaseMixin:
    def assertSchemaIsValid(self, probe, resource_url, auth=None, msg=None):
        api_sample = requests.get(resource_url)

        if not probe.validate(api_sample.json()):
            raise self.failureException(msg or 'Schema is invalid.')

