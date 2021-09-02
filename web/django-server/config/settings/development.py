from .base import *
import sys
SECRET_DEV_FILE = os.path.join(SECRET_PATH, 'settings_development.json')

dev_secrets = json.loads(''.join(open(SECRET_DEV_FILE).read())).get('django')
for key, value in dev_secrets.items():
    setattr(sys.modules[__name__], key, value)

DEBUG = True

INSTALLED_APPS += [
    'debug_toolbar',
]

MIDDLEWARE += [
    'debug_toolbar.middleware.DebugToolbarMiddleware',
]

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.mysql',
#         'NAME': os.path.join(BASE_DIR, 'db.mysql'),
#         'USER': dev_secrets['DATABASES']['USER'],
#         'PASSWORD': dev_secrets['DATABASES']['PASSWORD']
#     }
# }