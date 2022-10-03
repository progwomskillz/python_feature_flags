import ast
from linter.decorator_calls_searcher import DecoratorCallsSearcher
from linter.decorator_call import DecoratorCall
from linter.py_module import PyModule


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

        without_args_call = result[0]
        assert isinstance(without_args_call, DecoratorCall)
        assert without_args_call.decorator_name == 'decorate'
        assert without_args_call.line_number == 4
        assert without_args_call.call_args is None
        assert without_args_call.call_args is None

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

        with_args_call = result[0]
        assert isinstance(with_args_call, DecoratorCall)
        assert with_args_call.decorator_name == "decorate"
        assert with_args_call.line_number == 4
        assert with_args_call.call_args == ["some arg"]
        assert with_args_call.call_kwargs is None

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

        with_args_call = result[0]
        assert isinstance(with_args_call, DecoratorCall)
        assert with_args_call.decorator_name == "decorate"
        assert with_args_call.line_number == 4
        assert with_args_call.call_args is None
        assert with_args_call.call_kwargs == {"some_kwarg": "some kwarg value"}

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

        with_args_call = result[0]
        assert isinstance(with_args_call, DecoratorCall)
        assert with_args_call.decorator_name == "decorate"
        assert with_args_call.line_number == 4
        assert with_args_call.call_args == ["some arg value"]
        assert with_args_call.call_kwargs == {"some_kwarg": "some kwarg value"}
