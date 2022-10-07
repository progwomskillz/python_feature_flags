from mock import Mock, patch

from linter import DecoratorCallsSearcher
from linter.models import PyModule
from tests.factories import AstMocksFactory


class TestDecoratorCallsSearcher:
    ast_mocks_factory = AstMocksFactory()

    def setup(self):
        self.searcher = DecoratorCallsSearcher()

    def __build_node_mock(self, decorators):
        node_mock = Mock()
        node_mock.decorator_list = decorators
        return node_mock

    @patch('linter.DecoratorCallsSearcher.visit')
    def test_search(self, visit_method_mock):
        py_module = PyModule('test-filename', abstract_syntax_tree=Mock())
        raw_decorator_calls = [Mock()]

        self.searcher._decorator_calls = raw_decorator_calls
        result = self.searcher.search(py_module)

        assert self.searcher._decorator_calls == []
        assert result == raw_decorator_calls
        assert result[0].filename == py_module.filename

    def test_visit_FunctionDef_invalid_decorator_type(self):
        node_mock = self.__build_node_mock(decorators=[Mock()])

        result = self.searcher.visit_FunctionDef(node_mock)

        assert result is None
        assert self.searcher._decorator_calls == []

    @patch("linter.decorator_calls_searcher.DecoratorCall.from_ast_attribute")
    def test_visit_FunctionDef_ast_attribute_case(self, from_ast_attribute_mock):
        ast_attribute_mock = self.ast_mocks_factory.get_attribute_mock()
        node_mock = self.__build_node_mock(decorators=[ast_attribute_mock])
        decorator_call_mock = Mock()
        from_ast_attribute_mock.return_value = decorator_call_mock

        result = self.searcher.visit_FunctionDef(node_mock)

        assert result is None
        assert self.searcher._decorator_calls == [decorator_call_mock]

    @patch("linter.decorator_calls_searcher.DecoratorCall.from_ast_call")
    def test_visit_FunctionDef_ast_call_case(self, from_ast_call_mock):
        ast_call_mock = self.ast_mocks_factory.get_call_mock()
        node_mock = self.__build_node_mock(decorators=[ast_call_mock])
        decorator_call_value = Mock()
        from_ast_call_mock.return_value = decorator_call_value

        result = self.searcher.visit_FunctionDef(node_mock)

        assert result is None
        assert self.searcher._decorator_calls == [decorator_call_value]
