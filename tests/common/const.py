class ConfigVars(object):
    """Configuration environment variables"""

    # behavior
    VERBOSE = 'VERBOSE'

    # Mercury API URL
    MERCURY_API_ENDPOINT = 'MERCURY_API_ENDPOINT'
    # TODO some of these probably just belong in this file in another Class
    # instead of being defined in a config file (like 'mercury_id')
    ENTITY_FIELD_NAME = 'ENTITY_FIELD_NAME'
    LISTED_SERVICE_NAMES = 'LISTED_SERVICE_NAMES'
    INTERNAL_IDENTITY_URL = 'INTERNAL_IDENTITY_URL'
    INTERNAL_IDENTITY_USERNAME = 'INTERNAL_IDENTITY_USERNAME'
    INTERNAL_IDENTITY_PASSWORD = 'INTERNAL_IDENTITY_PASSWORD'
    DOMAIN = 'DOMAIN'
    DOMAIN_NAME = 'DOMAIN_NAME'
    JSON_DATA_LOCATION = 'JSON_DATA_LOCATION'

class Sources(object):
    """Sources to get the configuration variables from"""

    ENVIRON = 'environ'