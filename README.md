schemaprobe
===========

Platform for testing JSON-based RESTful API resources.


Writing test doubles representing the remote endpoints your app depends on 
is very common, right? But how do you ensure the data model that your double 
is producing is still valid? 

SchemaProbe helps you to test your tests. 


Usage example
-------------

```python
import schemaprobe

# First, declare the endpoint's data model using JSON-schema. 
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

# Then you can ensure your fixtures factory functions return 
# valid data models.
@schemaprobe.ensure(schemaprobe.JsonProbe(json_schema))
def FooResourceFixture():
    return  '''[{"date":1399339082,
                 "price":423.188,
                 "amount":0.01,
                 "tid":36961108,
                 "price_currency":"USD",
                 "item":"BTC",
                 "trade_type":"bid"}]'''
 
fixture = FooResourceFixture()

# If the returned data is invalid, an exception is raised.
@schemaprobe.ensure(schemaprobe.JsonProbe(json_schema))
def Invalid_FooResourceFixture():
    return  '''[{"date":1399339082,
                 "price":423.188,
                 "amount":0.01,
                 "tid":36961108,
                 "price_currency":"USD",
                 "item":"BTC",
                 "trade_type":999999}]'''  # should be string
 
i_fixture = Invalid_FooResourceFixture()
Traceback (most recent call last):
  ...  # omitted
TypeError: Returned data does not conform with the given schema.
```

Validating the schema against the actual endpoint
-------------------------------------------------

In order to ensure your schema is still valid for the remote endpoint 
it represents, the method `assertSchemaIsValid` is added to 
`unittest.TestCase` subclasses by using the `schemaprobe.TestCaseMixin`: 

```python
class FooBar(schemaprobe.TestCaseMixin, unittest.TestCase):
    def test_foo(self):
        self.assertSchemaIsValid(schemaprobe.JsonProbe(json_schema),
                                 'https://foo.com/api/2/listing.json')
```
