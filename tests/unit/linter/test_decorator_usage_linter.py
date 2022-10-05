import pytest
from mock import Mock
from linter.linters import DecoratorUsageLinter
from linter.models import LintingError
from linter import LintingException


class TestDecoratorUsageLinter:
    def setup(self):
        self.py_modules_provider_mock = Mock()
        self.py_module_linter_mock = Mock()
        self.linter = DecoratorUsageLinter(
            self.py_modules_provider_mock,
            self.py_module_linter_mock,
        )

    def test_init(self):
        assert self.linter.py_module_linter == self.py_module_linter_mock
        assert self.linter.py_modules_provider == self.py_modules_provider_mock

    def test_lint_no_errors(self):
        py_module_mock = Mock()
        self.py_modules_provider_mock.get_py_modules = Mock(
            return_value=[py_module_mock]
        )

        module_errors = []
        self.py_module_linter_mock.lint.return_value = module_errors

        result = self.linter.lint()

        assert result is None
        self.py_modules_provider_mock.get_py_modules.assert_called_once()
        self.py_module_linter_mock.lint.assert_called_once_with(py_module_mock)


    def test_lint_with_errors(self):
        py_module_mock = Mock()
        self.py_modules_provider_mock.get_py_modules = Mock(
            return_value=[py_module_mock]
        )
        module_errors = [LintingError('test-filename', 4, 'test-message')]
        self.py_module_linter_mock.lint.return_value = module_errors

        with pytest.raises(LintingException) as ex:
            self.linter.lint()

        assert ex.value.args[0] == '\ntest-filename:4 - test-message'
        self.py_modules_provider_mock.get_py_modules.assert_called_once()
        self.py_module_linter_mock.lint.assert_called_once_with(py_module_mock)
