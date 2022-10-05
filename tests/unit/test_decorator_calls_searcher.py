import ast

from mock import Mock, patch
from linter import DecoratorCallsSearcher
from linter.models import PyModule


class MockAstAttribute(ast.Attribute):
    def __new__(cls, *args, **kwargs):
        return Mock(spec=cls)


class MockAstCall(ast.Call):
    def __new__(cls, *args, **kwargs):
        return Mock(spec=cls)


class TestDecoratorCallsSearcher:
    def setup(self):
        self.searcher = DecoratorCallsSearcher()

    @patch('linter.DecoratorCallsSearcher.visit')
    def test_search(self, visit_method_mock):
        filename = "test-filename"
        abstract_syntax_tree_mock = Mock()
        py_module_mock = PyModule(filename, abstract_syntax_tree_mock)
        raw_decorator_calls = [Mock()]

        self.searcher._decorator_calls = raw_decorator_calls
        result = self.searcher.search(py_module_mock)

        assert self.searcher._decorator_calls == []
        assert result == raw_decorator_calls
        assert result[0].filename == filename
        visit_method_mock.assert_called_once_with(abstract_syntax_tree_mock)

    def test_visit_FunctionDef_invalid_decorator_type(self):
        node_mock = Mock()
        node_mock.decorator_list = [Mock()]

        result = self.searcher.visit_FunctionDef(node_mock)

        assert result is None
        assert self.searcher._decorator_calls == []

    @patch("linter.decorator_calls_searcher.DecoratorCall")
    def test_visit_FunctionDef_ast_attribute_case(self, decorator_call_mock):
        decorator_ast_attribute_mock = MockAstAttribute()
        node_mock = Mock()
        node_mock.decorator_list = [decorator_ast_attribute_mock]
        decorator_call_value = Mock()
        decorator_call_mock.from_ast_attribute.return_value = decorator_call_value

        result = self.searcher.visit_FunctionDef(node_mock)

        assert result is None
        assert self.searcher._decorator_calls == [decorator_call_value]
        decorator_call_mock.from_ast_attribute\
            .assert_called_once_with(decorator_ast_attribute_mock)

    @patch("linter.decorator_calls_searcher.DecoratorCall")
    def test_visit_FunctionDef_ast_call_case(self, decorator_call_mock):
        decorator_ast_call_mock = MockAstCall()
        node_mock = Mock()
        node_mock.decorator_list = [decorator_ast_call_mock]
        decorator_call_value = Mock()
        decorator_call_mock.from_ast_call.return_value = decorator_call_value

        result = self.searcher.visit_FunctionDef(node_mock)

        assert result is None
        assert self.searcher._decorator_calls == [decorator_call_value]
        decorator_call_mock.from_ast_call\
            .assert_called_once_with(decorator_ast_call_mock)
