import pytest
from mock import patch

from python_feature_flags import FeatureFlags
from python_feature_flags.exceptions import (
    FeatureFlagNotFound,
    InvalidValueOfFeatureFlag
)


class TestFeatureFlags():
    @patch('python_feature_flags.feature_flags.os')
    def test_init(self, os_mock):
        flags = ['feature_a', 'feature_b', 'feature_c', 'feature_d']
        os_mock.environ = {
            flags[0]: 'True',
            flags[1]: '1',
            flags[2]: 'false',
            flags[3]: '0'
        }

        feature_flags = FeatureFlags(flags)

        assert feature_flags.flags == {
            flags[0]: True,
            flags[1]: True,
            flags[2]: False,
            flags[3]: False
        }

    @patch('python_feature_flags.feature_flags.os')
    def test_init_flag_not_found(self, os_mock):
        flags = ['feature_a']
        os_mock.environ = {}

        with pytest.raises(FeatureFlagNotFound):
            FeatureFlags(flags)

    @patch('python_feature_flags.feature_flags.os')
    def test_init_invalid_flag_value(self, os_mock):
        flags = ['feature_a']
        os_mock.environ = {flags[0]: 'qwerty'}

        with pytest.raises(InvalidValueOfFeatureFlag):
            FeatureFlags(flags)

    @patch('python_feature_flags.feature_flags.os')
    def test_feature_flag_enabled(self, os_mock):
        flags = ['feature_a']
        os_mock.environ = {flags[0]: 'true'}

        expected_result = 'Return from test_func()'

        feature_flags = FeatureFlags(flags)

        @feature_flags.feature_flag(flags[0])
        def test_func():
            return expected_result

        result = test_func()

        assert result == expected_result

    @patch('python_feature_flags.feature_flags.os')
    def test_feature_flag_disabled(self, os_mock):
        flags = ['feature_a']
        os_mock.environ = {flags[0]: 'false'}

        expected_result = 'Return from test_func()'

        feature_flags = FeatureFlags(flags)

        @feature_flags.feature_flag(flags[0])
        def test_func():
            return expected_result

        result = test_func()

        assert result is None

    @patch('python_feature_flags.feature_flags.os')
    def test_feature_flag_flag_not_found(self, os_mock):
        flags = ['feature_a']
        os_mock.environ = {flags[0]: 'false'}

        expected_result = 'Return from test_func()'

        feature_flags = FeatureFlags(flags)

        @feature_flags.feature_flag(flags[0] + 'WRONG')
        def test_func():
            return expected_result

        with pytest.raises(FeatureFlagNotFound):
            test_func()
