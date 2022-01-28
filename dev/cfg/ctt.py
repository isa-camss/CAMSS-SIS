# PROJECT CONFIG
PROJECT_NAME = 'camss-sis'
VERSION = 'v1.0'

# API
API_PORT = 5000
API_DEBUG = False
API_NAME = 'apiCAMSS-SIS'
API_PREFIX = f'/{PROJECT_NAME}/{VERSION[:2]}'
API_TITLE = 'CAMSS-SIS.API - Development'
API_DESCRIPTION = 'It is an API...'
END_POINT_SWAGGER = f'{API_PREFIX}/swagger'
END_POINT_SWAGGER_JSON = f'{API_PREFIX}/swagger.json'
NAME_BLUEPRINT = 'swaggerCAMSS-SIS'

# EIRA THESAURI JOINUP

EIRA_THESAURI = 'https://joinup.ec.europa.eu/sites/default/files/distribution/access_url/2021-08/8adc381e-6997-4d66' \
                '-8ea3-b3d9edc6c42c/EIRA_SKOS.rdf '

