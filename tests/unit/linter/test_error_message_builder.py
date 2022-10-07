from mock import Mock
from linter import ErrorMessageBuilder


class TestErrorMessageBuilder:
    def setup(self):
        self.builder = ErrorMessageBuilder()

    def test_build(self):
        errors = [
            Mock(
                filename='test-filename-1',
                line_number=1,
                message='test-error-message-1'
            ),
            Mock(
                filename='test-filename-2',
                line_number=2,
                message='test-error-message-2'
            ),
        ]
        expected_result = (
            "\ntest-filename-1:1 - test-error-message-1"
            "\ntest-filename-2:2 - test-error-message-2"
        )

        result = self.builder.build(errors)

        assert result == expected_result
