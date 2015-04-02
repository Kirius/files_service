# coding=utf-8
import json
from django.http import HttpResponse


def json_response(view):
    """
    Decorator for views to return json.
    Decorated view must return a json serializable dictionary.
    """
    def _f(*args, **kwargs):
        res = view(*args, **kwargs)
        # if 'success' not in res:
        #     res['success'] = True

        return HttpResponse(json.dumps(res), content_type='application/json')

    return _f
