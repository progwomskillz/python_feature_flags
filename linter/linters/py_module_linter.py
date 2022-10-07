class PyModuleLinter:
    def __init__(
            self,
            decorator_calls_searcher,
            decorator_call_linter,
    ):
        self.decorator_calls_searcher = decorator_calls_searcher
        self.decorator_call_linter = decorator_call_linter

    def lint(self, py_module):
        errors = []
        for decorator_call in self.decorator_calls_searcher.search(py_module):
            errors += self.decorator_call_linter.lint(decorator_call)
        return errors
