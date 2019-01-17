Flask-MM-GeoIP2
===============
Flask-MM-GeoIP2 is a wrapper extension for MaxMind's [GeoIP2-python](https://github.com/maxmind/GeoIP2-python/) API.

Disclaimer
----------
This code is VERY alpha.  I'm talking "it-works-but-I-have-no-idea-why" alpha.  It's completely untested apart from a small handful of use cases.  USE AT YOUR OWN RISK!

Installation
------------
Assuming the disclaimer didn't scare you off, install the module like this:

```bash
    $ git clone git@github.com:TheOneTrueLX/Flask-MM-GeoIP2.git
    $ python ./setup.py install
```

If this code ever gets to a point where it is relatively safe to use in production, I'll throw it up on PyPI.

Setup
-----
To use this plugin with your Flask app:

```python
from flask import Flask
from flask_mm_geoip2 import GeoIP2

app = Flask(__name__)

# See "usage" below for an explanation of the configuration options
app.config['MAXMIND_SERVICE_TYPE'] = 'local'
app.config['MAXMIND_DB_PATH'] = '/path/to/your/GeoLite2-City.mmdb'

geoip = GeoIP2(app)
```
Or if you're doing the whole Flask application factory thing...
```python
from flask import Flask
from flask_mm_geoip2 import GeoIP2

geoip = GeoIP2()

def create_app():
    app = Flask(__name__)
    
    app.config['MAXMIND_SERVICE_TYPE'] = 'local'
    app.config['MAXMIND_DB_PATH'] = '/path/to/your/GeoLite2-City.mmdb'

    geoip.init_app(app)

    return app
```

Usage
-----
MaxMind provides two different methods of obtaining GeoIP data:
* Via API calls to a MaxMind-hosted web service
* Via lookups to a local database

The GeoIP2 class in Flask-MM-GeoIP2 exposes a single function: get_geoip_data().  What that function does varies wildly depending on the configuration settings you provide it.

* MAXMIND_SERVICE_TYPE: can be either 'local' or 'webservice'.
* MAXMIND_WEBSERVICE_ID: if MAXMIND_SERVICE_TYPE is set to 'webservice', this configuration option should be your MaxMind user ID.
* MAXMIND_WEBSERVICE_LICENSE: if MAXMIND_SERVICE_TYPE is set to 'webservice', this configuration option should be your MaxMind license number.
* MAXMIND_DB_PATH: if MAXMIND_SERVICE_TYPE is set to 'local', this is the absolute path to your MaxMind database file.

Flask-MM-GeoIP2 is (in theory, at least) compatible with all of MaxMind's free and paid services.  MaxMind makes three of their databases available under a Creative Commons Attribution-ShareAlike 4.0 License.  Those can be [downloaded from here](https://dev.maxmind.com/geoip/geoip2/geolite2/).

This comes with a BIG WARNING: For the love of God and all that is good and holy, **DO NOT RENAME THE DATABASE FILE!!*** Flask-MM-GeoIP2 uses the filename to determine what GeoIP2 function call to make, so renaming the file will break things.

Once the setup and configuration is in place, you can perform GeoIP lookups like this:

```python
response = geoip.get_geoip_data('1.1.1.1')
```

This returns a GeoIP2-python response object.  Depending whether you're doing a local or web service lookup, and depending on the type of database you're using, the contents of the response object can vary wildly, so due care should be exercised when consuming the contents of the response object.

See the [MaxMind GeoIP2-Python documentation](https://github.com/maxmind/GeoIP2-python) for more information.

To-Do
-----
* Create some unit tests
* Improve error handling for web service tests - the GeoIP2 Python API implements custom exceptions that probably make sense in the context of a standalone Python app, but will probably behave clumsily in the context of a Flask application.
* Handling for invalid IP addresses is probably very ugly.  Liberal use of try/except is recommended until better error handling is implemented.
