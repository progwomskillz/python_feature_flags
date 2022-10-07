from python_feature_flags import FeatureFlags

feature_flags = FeatureFlags(flags=["feature_invalid"])


@feature_flags.feature_flag("feature_invalid")
@feature_flags.feature_flag()
@feature_flags.feature_flag(
    'invalid-flag',
    'extra-arg',
    kwarg="kwarg-value"
)
def invalid_usage_case():
    ...


@FeatureFlags(flags=['feature_login']).feature_flag('feature_login')
def valid_usage_case():
    ...
