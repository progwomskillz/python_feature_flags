import functools
from os import environ

from .exceptions import FeatureFlagNotFound, InvalidValueOfFeatureFlag


class FeatureFlags():
    def __init__(self, flags):
        self.flags = {}
        self.__configure(flags)

    def feature_flag(self, flag):
        def decorator_feature_flag(func):
            @functools.wraps(func)
            def wrapper_feature_flag(*args, **kwargs):
                if flag not in self.flags:
                    raise FeatureFlagNotFound(f'{flag} feature flag not found.')
                value = None
                if self.flags[flag]:
                    value = func(*args, **kwargs)
                return value
            return wrapper_feature_flag
        return decorator_feature_flag

    def __configure(self, flags):
        for flag in flags:
            self.__configure_flag(flag)

    def __configure_flag(self, flag):
        try:
            lower_value = environ[flag].lower()
        except KeyError:
            raise FeatureFlagNotFound(f'{flag} feature flag not found.')
        possible_values = {
            '1': True,
            'true': True,
            '0': False,
            'false': False
        }
        if lower_value not in possible_values:
            raise InvalidValueOfFeatureFlag(f'The {flag} feature flag has an invalid value. Possible values: {list(possible_values.keys())}.')
        self.flags[flag] = possible_values[lower_value]
