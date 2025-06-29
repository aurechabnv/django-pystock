from pystock.settings.base import *


if env("ENV_NAME") == 'Production':
    from pystock.settings.prod import *
elif env("ENV_NAME") == 'Staging':
    from pystock.settings.staging import *
else:
    from pystock.settings.dev import *
