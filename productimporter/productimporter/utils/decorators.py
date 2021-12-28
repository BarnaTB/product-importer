from collections import ChainMap
from functools import wraps

from utils.exceptions import CustomAPIException


def required_fields(params):
    """
    DRF function view decorator for checking that all required request
    params/fields are not None.
    """

    def validator(f):
        @wraps(f)
        def func_wrap(view, request, *args, **kwargs):
            if request:
                data = ChainMap(request.GET, request.data, kwargs)
                for param in params:
                    value = data.get(param)
                    if not value and value is not False:
                        message = param + " is required"
                        raise CustomAPIException(message=message)
            return f(view, request, *args, **kwargs)

        return func_wrap

    return validator
