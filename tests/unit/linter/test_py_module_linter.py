from mock import Mock
from linter.linters import PyModuleLinter
from linter.models import DecoratorCall


class TestPyModuleLinter:
    def setup(self):
        self.decorator_name = 'test-decorator-name'
        self.decorator_calls_searcher_mock = Mock()
        self.args_validation_service_mock = Mock()
        self.kwargs_validation_service_mock = Mock()
        self.linter = PyModuleLinter(
            self.decorator_name,
            self.decorator_calls_searcher_mock,
            self.args_validation_service_mock,
            self.kwargs_validation_service_mock,
        )

    def test_init(self):
        assert self.linter.decorator_name == self.decorator_name
        assert self.linter.decorator_calls_searcher == self.decorator_calls_searcher_mock
        assert self.linter.args_validation_service == self.args_validation_service_mock
        assert self.linter.kwargs_validation_service == self.kwargs_validation_service_mock

    def test_lint_invalid_decorator_name_case(self):
        decorator_call = Mock(decorator_name=self.decorator_name + 'invalid')
        self.decorator_calls_searcher_mock.search.return_value = [decorator_call]
        py_module_mock = Mock()

        result = self.linter.lint(py_module_mock)

        assert result == []
        self.decorator_calls_searcher_mock.search.assert_called_once_with(py_module_mock)

    def test_lint_errors_case(self):
        decorator_call = DecoratorCall()
        decorator_call.decorator_name = self.decorator_name
        decorator_call.line_number = 1
        decorator_call.args = ["test-arg"]
        decorator_call.kwargs = {"test": "kwarg"}
        self.decorator_calls_searcher_mock.search.return_value = [decorator_call]
        self.args_validation_service_mock.validate.return_value = ["args_error_message"]
        self.kwargs_validation_service_mock.validate.return_value = ["kwargs_error_message"]
        py_module_mock = Mock(filename='test-filename')

        result = self.linter.lint(py_module_mock)

        assert len(result) == 2
        assert result[0].filename == py_module_mock.filename
        assert result[0].line_number == decorator_call.line_number
        assert result[0].message == 'args_error_message'
        assert result[1].filename == py_module_mock.filename
        assert result[1].line_number == decorator_call.line_number
        assert result[1].message == "kwargs_error_message"
        self.decorator_calls_searcher_mock.search.assert_called_once_with(py_module_mock)
        self.args_validation_service_mock.validate.assert_called_once_with(decorator_call.args)
        self.kwargs_validation_service_mock.validate.assert_called_once_with(decorator_call.kwargs)
