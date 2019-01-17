import os
import re
import geoip2.database
import geoip2.webservice
from flask import current_app, _app_ctx_stack

VALID_SERVICE_TYPES = [
    'local',
    'webservice',
]

class GeoIP2(object):
    def __init__(self, app=None):
        self.app = app
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        app.config.setdefault('MAXMIND_SERVICE_TYPE', 'local')
        app.config.setdefault('MAXMIND_WEBSERVICE_ID', None)
        app.config.setdefault('MAXMIND_WEBSERVICE_LICENSE', None)
        app.config.setdefault('MAXMIND_DB_PATH', None)

        # To save us some typing later...
        self.service_type = app.config['MAXMIND_SERVICE_TYPE']
        self.webservice_id = app.config['MAXMIND_WEBSERVICE_ID']
        self.webservice_license = app.config['MAXMIND_WEBSERVICE_LICENSE']
        self.db_path = app.config['MAXMIND_DB_PATH']

        if self.service_type not in VALID_SERVICE_TYPES:
            raise TypeError('\'{}\' is not a valid Flask-MM-GeoIP2 service type.'.format(self.service_type))
        
        self.app = app
    
    def get_geoip_data(self, ip_address):
        """
        Performs a lookup from a MaxMind GeoIP database (either local or remote, based
        on Flask app config settings).  Returns a geoip2 response object.
        """
        if self.service_type == "local":
            # Performing a lookup from a local DB
            if self.db_path:
                if os.path.isfile(self.db_path):
                    reader = geoip2.database.Reader(self.db_path)

                    # Determine from the db_path what function to call.  MaxMind has
                    # very generously correlated the function calls suppored by
                    # the reader object to the names of the databases, so it's not 
                    # hard to divine what call to make.
                    p = re.compile('^.*\/?-(.*)\.mmdb$')
                    m = p.match(self.db_path)
                    lookup_function = m.group(1).lower().replace('-','_')

                    try:
                        # Using black magic to make this function call...
                        # this is safe to do, right?
                        result = getattr(reader, lookup_function)(ip_address)
                    except AttributeError:
                        raise ValueError('Unable to determine MaxMind database type - make sure you didn\'t rename the database.')
                    else:
                        return result
                else:
                    raise FileNotFoundError('The MaxMind DB at {} could not be found.'.format(db_path))
            else:
                raise ValueError('The MAXMIND_DB_PATH configuration directive is not set.')

        else:
            # Performing an API call
            if webservice_id and webservice_license:
                client = geoip2.webservice.Client(self.webservice_id, self.webservice_license)

                # TODO: There's a lot that can go wrong here (see geoip2.errors), 
                # and there is probably a potential for something very stupid to 
                # abend the Flask app.

                # TODO: API calls are pinned to "city" since, unlike the local db
                # method, we have no good way of determining whether we should use
                # city or country to perform this lookup.  
                return client.city(ip_address)
            else:
                raise TypeError('Either MAXMIND_WEBSERVICE_ID or MAXMIND_WEBSERVICE_LICENSE is not set.')