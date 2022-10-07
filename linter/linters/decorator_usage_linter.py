from linter.linting_exception import LintingException


class DecoratorUsageLinter:
    def __init__(
            self,
            py_modules_provider,
            py_module_linter,
            error_message_builder,
    ):
        self.py_modules_provider = py_modules_provider
        self.py_module_linter = py_module_linter
        self.error_message_builder = error_message_builder

    def lint(self):
        errors = []
        for py_module in self.py_modules_provider.get_py_modules():
            errors += self.py_module_linter.lint(py_module)
        if not errors:
            return
        error_message = self.error_message_builder.build(errors)
        raise LintingException(error_message)
