from linter.linting_exception import LintingException


class DecoratorUsageLinter:
    def __init__(
            self,
            py_modules_provider,
            py_module_linter,
    ):
        self.py_modules_provider = py_modules_provider
        self.py_module_linter = py_module_linter

    def lint(self):
        errors = []
        for py_module in self.py_modules_provider.get_py_modules():
            errors += self.py_module_linter.lint(py_module)
        if not errors:
            return
        errors_message = self.__build_error_message(errors)
        raise LintingException(errors_message)

    def __build_error_message(self, errors):
        error_lines = [
            f"\n{error.filename}:{error.line_number} - {error.message}"
            for error in errors
        ]
        return "".join(error_lines)
