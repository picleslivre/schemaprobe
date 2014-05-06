import json
import unittest
from unittest import mock

from schemaprobe import JsonProbe, ensure

#------------------
# Fixtures
#------------------
json_schema = '''{
    "$schema": "http://json-schema.org/schema#",
    "type": "array",
    "items": {
        "type": "object",
        "properties": {
            "date": {"type": "number"},
            "price": {"type": "number"},
            "amount": {"type": "number"},
            "tid": {"type": "number"},
            "price_currency": {"type": "string"},
            "item": {"type": "string"},
            "trade_type": {"type": "string"}
        }
    }
}'''


json_data = '''[{"date":1399339082,
            "price":423.188,
            "amount":0.01,
            "tid":36961108,
            "price_currency":"USD",
            "item":"BTC",
            "trade_type":"bid"}]'''


#------------------
# Unit tests
#------------------
class JsonProbeTests(unittest.TestCase):
    @mock.patch.object(JsonProbe, '_jsonschema', None)
    def test_jsonschema_must_be_present(self):
        self.assertRaises(TypeError, lambda: JsonProbe(json_schema))

    def test_normalize_input(self):
        probe = JsonProbe(json_schema)
        expected = json.loads(json_schema)

        self.assertEqual(probe._normalize_input(json_schema), expected)

    def test_schema_normalized_during_init(self):
        probe = JsonProbe(json_schema)
        expected = json.loads(json_schema)

        self.assertEqual(probe.schema, expected)

    def test_valid_json_data(self):
        probe = JsonProbe(json_schema)

        self.assertTrue(probe.validate(json_data))

    def test_valid_python_data(self):
        probe = JsonProbe(json_schema)
        py_data = json.loads(json_data)

        self.assertTrue(probe.validate(py_data))

    def test_invalid_python_data(self):
        probe = JsonProbe(json_schema)
        py_data = ['foo', 'bar']

        self.assertFalse(probe.validate(py_data))

    def test_invalid_json_data(self):
        probe = JsonProbe(json_schema)
        data = json.dumps(['foo', 'bar'])

        self.assertFalse(probe.validate(data))


class EnsureDecoratorTests(unittest.TestCase):
    def test_valid_python_data(self):
        @ensure(JsonProbe(json_schema))
        def FixtureFactory():
            return json.loads(json_data)

        self.assertTrue(FixtureFactory())

    def test_invalid_python_data(self):
        @ensure(JsonProbe(json_schema))
        def FixtureFactory():
            return ['foo', 'bar']

        self.assertRaises(TypeError, lambda: FixtureFactory())

    def test_metadata_is_maintained(self):
        @ensure(JsonProbe(json_schema))
        def FixtureFactory():
            """Docstring"""
            return json.loads(json_data)

        self.assertEqual(FixtureFactory.__doc__, 'Docstring')
        self.assertEqual(FixtureFactory.__name__, 'FixtureFactory')


#class FooBar(SchemaProbeMixin, unittest.TestCase):
#    def test_foo(self):
#        self.assertSchemaIsValid(JsonProbe(json_schema), 'http://...', auth=Auth)
