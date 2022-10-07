from linter.linters import (
    PyModuleLinter,
    DecoratorUsageLinter,
    DecoratorCallLinter,
)
from linter.validation_services import (
    ArgsValidationService,
    KwargsValidationService,
    DecoratorCallValidationService,
)
from linter.providers import (
    PyPathsProvider,
    PyModulesProvider,
)
from linter import (
    AstLoader,
    DecoratorCallsSearcher,
    ErrorMessageBuilder
)

ast_loader = AstLoader()
decorator_calls_searcher = DecoratorCallsSearcher()
error_message_builder = ErrorMessageBuilder()

# providers
py_paths_provider = PyPathsProvider(
    patterns_to_exclude=["venv", ".git", 'usr/local/lib', 'tests']
)
py_modules_provider = PyModulesProvider(".", py_paths_provider, ast_loader)

# validation_services
args_validation_service = ArgsValidationService()
kwargs_validation_service = KwargsValidationService()
decorator_call_validation_service = DecoratorCallValidationService(
    args_validation_service,
    kwargs_validation_service,
)

# linters
decorator_call_linter = DecoratorCallLinter(
    'feature_flag',
    decorator_call_validation_service,
)
py_module_linter = PyModuleLinter(
    decorator_calls_searcher,
    decorator_call_linter,
)
decorator_usage_linter = DecoratorUsageLinter(
    py_modules_provider,
    py_module_linter,
    error_message_builder
)
