import pytest
from mock import Mock
from linter.linters import DecoratorUsageLinter
from linter import LintingException


class TestDecoratorUsageLinter:
    def setup(self):
        self.py_modules_provider_mock = Mock()
        self.py_module_linter_mock = Mock()
        self.error_message_builder_mock = Mock()
        self.linter = DecoratorUsageLinter(
            self.py_modules_provider_mock,
            self.py_module_linter_mock,
            self.error_message_builder_mock,
        )

    def test_init(self):
        assert self.linter.py_module_linter == self.py_module_linter_mock
        assert self.linter.py_modules_provider == self.py_modules_provider_mock
        assert self.linter.error_message_builder == self.error_message_builder_mock

    def test_lint_no_errors(self):
        py_module_mocks = [Mock()]
        module_errors = []

        get_py_modules_mock = Mock(return_value=py_module_mocks)
        self.py_modules_provider_mock.get_py_modules = get_py_modules_mock
        lint_module_mock = Mock(return_value=module_errors)
        self.py_module_linter_mock.lint = lint_module_mock
        result = self.linter.lint()

        assert result is None
        get_py_modules_mock.assert_called_once()
        lint_module_mock.assert_called_once_with(py_module_mocks[0])

    def test_lint_with_errors(self):
        py_module_mocks = [Mock()]
        module_errors = [Mock()]
        error_message = "test-filename:test-line - error"

        get_py_modules_mock = Mock(return_value=py_module_mocks)
        self.py_modules_provider_mock.get_py_modules = get_py_modules_mock
        lint_module_mock = Mock(return_value=module_errors)
        self.py_module_linter_mock.lint = lint_module_mock
        build_error_message_mock = Mock(return_value=error_message)
        self.error_message_builder_mock.build = build_error_message_mock
        with pytest.raises(LintingException) as ex:
            self.linter.lint()

        get_py_modules_mock.assert_called_once()
        lint_module_mock.assert_called_once_with(py_module_mocks[0])
        build_error_message_mock.assert_called_once_with(module_errors)
        assert ex.value.args[0] == error_message
