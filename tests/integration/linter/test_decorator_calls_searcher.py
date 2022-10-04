import ast
from linter.decorator_calls_searcher import DecoratorCallsSearcher
from linter.models.decorator_call import DecoratorCall
from linter.models.py_module import PyModule


class TestDecoratorCallsSearcher:
    def setup(self):
        self.searcher = DecoratorCallsSearcher()

    def test_search_without_args_call(self):
        py_module = PyModule(
            filename="test.py",
            abstract_syntax_tree=ast.parse(
                """
from decorator import decorator
class RootPlacedExecutor:
    @decorator.decorate
    def easy_decorated_method(self, arg_1, arg_2):
        ...
                """
            )
        )

        result = self.searcher.search(py_module)

        decorator_call = result[0]
        assert isinstance(decorator_call, DecoratorCall)
        assert decorator_call.decorator_name == 'decorate'
        assert decorator_call.filename == "test.py"
        assert decorator_call.line_number == 4
        assert decorator_call.args == []
        assert decorator_call.kwargs == {}

    def test_search_with_args_call(self):
        py_module = PyModule(
            filename="test.py",
            abstract_syntax_tree=ast.parse(
                """
from decorator import decorator
class RootPlacedExecutor:
    @decorator.decorate(\"some arg\")
    def easy_decorated_method(self, arg_1, arg_2):
        ...
                """
            )
        )

        result = self.searcher.search(py_module)

        decorator_call = result[0]
        assert isinstance(decorator_call, DecoratorCall)
        assert decorator_call.decorator_name == "decorate"
        assert decorator_call.filename == "test.py"
        assert decorator_call.line_number == 4
        assert decorator_call.args == ["some arg"]
        assert decorator_call.kwargs == {}

    def test_search_with_kwargs_call(self):
        py_module = PyModule(
            filename="test.py",
            abstract_syntax_tree=ast.parse(
                """
from decorator import decorator
class RootPlacedExecutor:
    @decorator.decorate(some_kwarg="some kwarg value")
    def easy_decorated_method(self, arg_1, arg_2):
        ...
                """
            )
        )
        result = self.searcher.search(py_module)

        decorator_call = result[0]
        assert isinstance(decorator_call, DecoratorCall)
        assert decorator_call.decorator_name == "decorate"
        assert decorator_call.filename == "test.py"
        assert decorator_call.line_number == 4
        assert decorator_call.args == []
        assert decorator_call.kwargs == {"some_kwarg": "some kwarg value"}

    def test_search_with_args_and_kwargs_call(self):
        py_module = PyModule(
            filename="test.py",
            abstract_syntax_tree=ast.parse(
                (
                    """
from decorator import decorator
class RootPlacedExecutor:
    @decorator.decorate("some arg value", some_kwarg="some kwarg value")
    def easy_decorated_method(self, arg_1, arg_2):
        ...
                    """
                )
            )
        )
        searcher = DecoratorCallsSearcher()
        result = searcher.search(py_module)

        decorator_call = result[0]
        assert isinstance(decorator_call, DecoratorCall)
        assert decorator_call.decorator_name == "decorate"
        assert decorator_call.filename == "test.py"
        assert decorator_call.line_number == 4
        assert decorator_call.args == ["some arg value"]
        assert decorator_call.kwargs == {"some_kwarg": "some kwarg value"}
