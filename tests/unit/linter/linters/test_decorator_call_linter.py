from mock import Mock
from linter.linters import DecoratorCallLinter
from linter.models import LintingError


class TestDecoratorCallLinter:
    def setup(self):
        self.decorator_name = 'test-decorator-name'
        self.decorator_call_validation_service_mock = Mock()
        self.linter = DecoratorCallLinter(
            self.decorator_name,
            self.decorator_call_validation_service_mock,
        )

    def test_init(self):
        assert self.linter.decorator_name == self.decorator_name
        assert self.linter.decorator_call_validation_service == \
               self.decorator_call_validation_service_mock

    def test_lint_wrong_decorator_name(self):
        decorator_call_mock = Mock(decorator_name=self.decorator_name + "wrong")

        result = self.linter.lint(decorator_call_mock)

        assert result == []

    def test_lint(self):
        decorator_call_mock = Mock(
            decorator_name=self.decorator_name,
            filename='test-filename',
            line_number='test-line-number',
        )
        error_messages = ["error-message-1"]

        validate_mock = Mock(return_value=error_messages)
        self.decorator_call_validation_service_mock.validate = validate_mock
        result = self.linter.lint(decorator_call_mock)

        assert isinstance(result, list)
        assert len(result) == len(error_messages)
        linting_error = result[0]
        assert isinstance(linting_error, LintingError)
        assert linting_error.message == error_messages[0]
        assert linting_error.filename == decorator_call_mock.filename
        assert linting_error.line_number == decorator_call_mock.line_number
