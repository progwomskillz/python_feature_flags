from linter.models import LintingError


class DecoratorCallLinter:
    def __init__(self, decorator_name, decorator_call_validation_service):
        self.decorator_name = decorator_name
        self.decorator_call_validation_service = decorator_call_validation_service

    def lint(self, decorator_call):
        if decorator_call.decorator_name != self.decorator_name:
            return []
        errors = [
            LintingError(
                decorator_call.filename,
                decorator_call.line_number,
                error_message,
            )
            for error_message
            in self.decorator_call_validation_service.validate(decorator_call)
        ]
        return errors
