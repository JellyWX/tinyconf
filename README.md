# tinyconf
## A small library for declarative config interpretation

### Installing 

* Download `tinyconf`
* `pip install .` within the folder
* `import tinyconf`
* `tinyconf.__version__`

### Usage

An example usage:

`main.py`
```
from tinyconf.deserializers import IniDeserializer
from tinyconf.fields import *

class Config(IniDeserializer):
    token = Field(strict=True) # Loads field called 'token'. Fails if not present

    client_id = IntegerField('client') # Loads field called 'client'

    api_version = Field('apiv', default="8") # Loads field called 'apiv', if not present uses "8"

    permitted_users = ListField(map=lambda x: int(x.strip()), default=[], delimiter=";")


config = Config(filename="conf.ini", section="DEFAULT")

assert(config.token == "abcdefghijklmno")
assert(config.client_id == 123456789)
assert(config.api_version == "8")
assert(config.permitted_users == [1111, 2222])
```

`conf.ini`
```
[DEFAULT]
token = "abcdefghijklmno"
client = 123456789
permitted_users = 1111; 2222
```

### Docs

https://tinyconf.readthedocs.io/en/latest/tinyconf.html

Docs can be built with Sphinx in `docs` folder