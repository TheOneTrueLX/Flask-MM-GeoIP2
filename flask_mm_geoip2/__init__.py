import os
import re
import geoip2.database
import geoip2.webservice
from geoip2.errors import AddressNotFoundError
from flask import current_app

class GeoIP2(object):
    def __init__(self, app=None):
        self.app = app
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        app.config.setdefault('FLASK_MM_GEOIP2_WEBSERVICE_ID', None)
        app.config.setdefault('FLASK_MM_GEOIP2_WEBSERVICE_LICENSE', None)
        app.config.setdefault('FLASK_MM_GEOIP2_DB_PATH', None)
        app.config.setdefault('FLASK_MM_GEOIP2_DEVELOPMENT_MODE', False)
        app.config.setdefault('FLASK_MM_GEOIP2_DEVELOPMENT_IP', '1.1.1.1')

        # To save us some typing later...
        self.webservice_id = app.config['FLASK_MM_GEOIP2_WEBSERVICE_ID']
        self.webservice_license = app.config['FLASK_MM_GEOIP2_WEBSERVICE_LICENSE']
        self.db_path = app.config['FLASK_MM_GEOIP2_DB_PATH']
        self.development_mode = app.config['FLASK_MM_GEOIP2_DEVELOPMENT_MODE']
        self.development_ip = app.config['FLASK_MM_GEOIP2_DEVELOPMENT_IP']
        
        self.app = app
    
    def get_local_geoip_data(self, ip_address):
        """
        Performs a lookup from a local MaxMind GeoIP database.  Returns a geoip2 response object.
        """
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
                    if not self.development_mode:
                        result = getattr(reader, lookup_function)(ip_address)
                    else:
                        result = getattr(reader, lookup_function)(self.development_ip)
                except AttributeError:
                    raise ValueError('Unable to determine MaxMind database type - make sure you didn\'t rename the database.')
                except AddressNotFoundError:
                    return None

                return result
            else:
                raise FileNotFoundError('The MaxMind DB at {} could not be found.'.format(db_path))
        else:
            raise ValueError('The FLASK_MM_GEOIP2_DB_PATH configuration directive is not set.')


    def get_webservice_geoip_data(self, ip_address, query_type='city'):
        VALID_QUERY_TYPES = ['city','country','insights']
        if not query_type in VALID_QUERY_TYPES:
            raise ValueError('\'{}\' is not a valid query type'.format(query_type))
        
        # Performing an API call
        if webservice_id and webservice_license:
            client = geoip2.webservice.Client(self.webservice_id, self.webservice_license)

            # TODO: There's a lot that can go wrong here (see geoip2.errors), 
            # and there is probably a potential for something very stupid to 
            # abend the Flask app.
            try:
                if not self.development_mode:
                    result = getattr(client, query_type)(ip_address)
                else:
                    result = getattr(client, query_type)(self.development_ip)
            except AddressNotFoundError:
                return None
            
            return result
        else:
            raise TypeError('Either FLASK_MM_GEOIP2_WEBSERVICE_ID or FLASK_MM_GEOIP2_WEBSERVICE_LICENSE is not set.')