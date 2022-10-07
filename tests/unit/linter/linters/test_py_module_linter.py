from mock import Mock
from linter.linters import PyModuleLinter


class TestPyModuleLinter:
    def setup(self):
        self.decorator_calls_searcher_mock = Mock()
        self.decorator_call_linter_mock = Mock()
        self.linter = PyModuleLinter(
            self.decorator_calls_searcher_mock,
            self.decorator_call_linter_mock,
        )

    def test_init(self):
        assert self.linter.decorator_calls_searcher == self.decorator_calls_searcher_mock
        assert self.linter.decorator_call_linter == self.decorator_call_linter_mock

    def test_lint(self):
        decorator_calls_mocks = [Mock()]
        errors = [Mock()]
        py_module_mock = Mock()

        search_mock = Mock(return_value=decorator_calls_mocks)
        self.decorator_calls_searcher_mock.search = search_mock
        lint_mock = Mock(return_value=errors)
        self.decorator_call_linter_mock.lint = lint_mock
        result = self.linter.lint(py_module_mock)

        assert result == errors
        search_mock.assert_called_once_with(py_module_mock)
        lint_mock.assert_called_once_with(decorator_calls_mocks[0])
