import pytest

from linter.structure import decorator_usage_linter, py_paths_provider
from linter import LintingException


class TestDecoratorUsageLinter:
    # Depends on "decorator_usage_test_file.py"
    test_file_path = "tests/integration/linter/linters/decorator_usage_test_file.py"

    def setup(self):
        self.linter = decorator_usage_linter
        py_paths_provider.patterns_to_exclude.remove("tests")

    def teardown(self):
        py_paths_provider.patterns_to_exclude.append("tests")

    @pytest.mark.parametrize(
        'expected_error', [
            f"{test_file_path}:6 - The feature_invalid feature flag has an invalid value.",
            f"{test_file_path}:7 - Invalid number of call args, required 1, but given 0.",
            f"{test_file_path}:8 - Invalid number of call args, required 1, but given 2.",
            f"{test_file_path}:8 - extra-arg feature flag not found.",
            f"{test_file_path}:8 - Decorator call contains kwargs, but must not",

        ]
    )
    def test_lint(self, expected_error):
        with pytest.raises(LintingException) as ex:
            self.linter.lint()
        error_message = ex.value.args[0]
        assert expected_error in error_message
