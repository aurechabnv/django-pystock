from pystock.settings.base import env


if env("ENV_NAME") == 'Production':
    from pystock.settings.prod import *
else:
    from pystock.settings.dev import *
