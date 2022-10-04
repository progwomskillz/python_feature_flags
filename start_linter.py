from linter.linters import (
    PyModuleLinter,
    DecoratorUsageLinter,
)
from linter.validation_services import (
    ArgsValidationService,
    KwargsValidationService,
)
from linter.providers import (
    PyPathsProvider,
    PyModulesProvider,
)
from linter import (
    AstLoader,
    DecoratorCallsSearcher,
)

ast_loader = AstLoader()
py_paths_provider = PyPathsProvider(patterns_to_exclude=["venv", ".git"])
py_modules_provider = PyModulesProvider(".", py_paths_provider, ast_loader)
decorator_calls_searcher = DecoratorCallsSearcher()
args_validation_service = ArgsValidationService()
kwargs_validation_service = KwargsValidationService()
py_module_linter = PyModuleLinter(
    "feature_flag",
    decorator_calls_searcher,
    args_validation_service,
    kwargs_validation_service,
)
decorator_usage_linter = DecoratorUsageLinter(
    py_modules_provider,
    py_module_linter,
)

if __name__ == '__main__':
    decorator_usage_linter.lint()
