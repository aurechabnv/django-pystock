#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys


def main():
    """Run administrative tasks."""
    # https://github.com/gabigab117/onsenbray/blob/main/manage.py
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pystock.settings.dev') # En gros ici je gère avec des variables d'environnement (voir le lien ci-dessus)
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
