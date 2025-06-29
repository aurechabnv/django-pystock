from pystock.settings import env


def export_vars(request):
    data = dict()
    data['ENV_NAME'] = env('ENV_NAME')
    return data
