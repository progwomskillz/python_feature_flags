from linter.models import LintingError


class PyModuleLinter:
    def __init__(
            self,
            decorator_name,
            decorator_calls_searcher,
            args_validation_service,
            kwargs_validation_service,
    ):
        self.decorator_name = decorator_name
        self.decorator_calls_searcher = decorator_calls_searcher
        self.args_validation_service = args_validation_service
        self.kwargs_validation_service = kwargs_validation_service

    def lint(self, py_module):
        errors = []
        for decorator_call in self.decorator_calls_searcher.search(py_module):
            if decorator_call.decorator_name != self.decorator_name:
                continue
            error_messages = [
                *self.args_validation_service.validate(decorator_call.args),
                *self.kwargs_validation_service.validate(decorator_call.kwargs)
            ]
            errors += self.__build_errors(
                error_messages,
                py_module.filename,
                decorator_call.line_number,
            )
        return errors

    def __build_errors(self, error_messages, filename, line_number):
        return [
            LintingError(filename, line_number, error_message)
            for error_message in error_messages
        ]
