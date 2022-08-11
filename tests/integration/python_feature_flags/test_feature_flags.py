import pytest

from python_feature_flags import FeatureFlags
from python_feature_flags.exceptions import (
    FeatureFlagNotFound,
    InvalidValueOfFeatureFlag
)


class TestFeatureFlags():
    def test_init(self):
        flags = [
            'feature_login',
            'feature_login_num',
            'feature_logout',
            'feature_logout_num'
        ]

        feature_flags = FeatureFlags(flags)

        assert feature_flags.flags == {
            flags[0]: True,
            flags[1]: True,
            flags[2]: False,
            flags[3]: False
        }

    def test_init_flag_not_found(self):
        flags = ['feature_unknown']

        with pytest.raises(FeatureFlagNotFound):
            FeatureFlags(flags)

    def test_init_invalid_flag_value(self):
        flags = ['feature_invalid']

        with pytest.raises(InvalidValueOfFeatureFlag):
            FeatureFlags(flags)

    def test_feature_flag_enabled(self):
        flags = ['feature_login']

        expected_result = 'Return from test_func()'

        feature_flags = FeatureFlags(flags)

        @feature_flags.feature_flag(flags[0])
        def test_func():
            return expected_result

        result = test_func()

        assert result == expected_result

    def test_feature_flag_disabled(self):
        flags = ['feature_logout']

        expected_result = 'Return from test_func()'

        feature_flags = FeatureFlags(flags)

        @feature_flags.feature_flag(flags[0])
        def test_func():
            return expected_result

        result = test_func()

        assert result is None

    def test_feature_flag_flag_not_found(self):
        flags = ['feature_login']

        expected_result = 'Return from test_func()'

        feature_flags = FeatureFlags(flags)

        @feature_flags.feature_flag(flags[0] + 'WRONG')
        def test_func():
            return expected_result

        with pytest.raises(FeatureFlagNotFound):
            test_func()
