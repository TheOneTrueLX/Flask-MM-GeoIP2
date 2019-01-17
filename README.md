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
app.config['FLASK_MM_GEOIP2_DB_PATH'] = '/path/to/your/GeoLite2-City.mmdb'

geoip = GeoIP2(app)
```
Or if you're doing the whole Flask application factory thing...
```python
from flask import Flask
from flask_mm_geoip2 import GeoIP2

geoip = GeoIP2()

def create_app():
    app = Flask(__name__)
    
    app.config['FLASK_MM_GEOIP2_DB_PATH'] = '/path/to/your/GeoLite2-City.mmdb'

    geoip.init_app(app)

    return app
```

Usage
-----
Flask-MM-GeoIP2 provides two functions for consuming MaxMind's GeoIP services:
* `get_webservice_geoip_data()`: Performs GeoIP lookups via API calls to MaxMind's [GeoIP2 Precision Web Services](https://dev.maxmind.com/geoip/geoip2/web-services/).
* `get_local_geoip_data()`: Performs GeoIP lookups via lookups to a local MaxMind database file.

The `get_webservice_geoip_data()` function requires the following configuration directives be set:
* `FLASK_MM_GEOIP2_WEBSERVICE_ID`: This should be your MaxMind user ID.
* `FLASK_MM_GEOIP2_WEBSERVICE_LICENSE`: This configuration option should be your MaxMind license number.
The usual warnings and caveats about leaking API keys on Github apply.

The `get_local_geoip_data()` function requires the following configuration directive be set:
* `FLASK_MM_GEOIP2_DB_PATH`: This is the absolute path to your MaxMind database file.  This comes with a **BIG WARNING**: For the love of God and all that is good and holy, **DO NOT RENAME THE DATABASE FILE!!** Flask-MM-GeoIP2 uses the filename to determine what GeoIP2 function call to make, so renaming the file will break things.

Flask-MM-GeoIP2 is (in theory, at least) compatible with all of MaxMind's free and paid databases.  Flask-MM-GeoIP2 does not distribute with any of MaxMind's databases -- it is up to you to obtain one.  MaxMind makes three of their databases available under a Creative Commons Attribution-ShareAlike 4.0 License, which can be [downloaded from here](https://dev.maxmind.com/geoip/geoip2/geolite2/).

Once the setup and configuration is in place, you can perform GeoIP lookups like this:

```python
# Webservice Lookup
response = geoip.get_webservice_geoip_data('1.1.1.1')  # defaults to 'city' lookups
response = geoip.get_webservice_geoip_data('1.1.1.1', query_type='country')

# Local Database Lookup
# Does not accept a 'query_type' parameter.  Instead, it determines which style of
# lookup to perform based on the type of local database it's performing its
# lookups against.
response = geoip.get_local_geoip_data('1.1.1.1')
```

These functions return the appropriate geoip2.model object based on the type of lookup performed, or `None` in the event that the address lookup fails.  Depending on the type of lookup you're performing, the contents of the response can vary wildly, so due care should be exercised when consuming it in your application.  See the [MaxMind GeoIP2-Python documentation](https://github.com/maxmind/GeoIP2-python) for more information on response formats.

Development Options
-------------------
If your Flask site is currently under development, you can set `FLASK_MM_GEOIP2_DEVELOPMENT_MODE = True`.  This alters the behavior of get_geoip_data() to ignore the IP address passed in its arguments and always return the IP address set in `FLASK_MM_GEOIP2_DEVELOPMENT_IP` (which is 1.1.1.1 by default).  This way, you can expect a consistent result from the function while you're working on your site.

To-Do
-----
* Create some unit tests
* Improve error handling for web service lookups - the GeoIP2 Python API implements custom exceptions that probably make sense in the context of a standalone Python app, but will probably behave clumsily in the context of a Flask application.
