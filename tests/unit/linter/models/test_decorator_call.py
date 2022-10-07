from mock import Mock

from linter.models import DecoratorCall
from tests.factories import AstMocksFactory


class TestDecoratorCall:
    ast_mocks_factory = AstMocksFactory()

    def test_init(self):
        model = DecoratorCall()
        for value in model.__dict__.values():
            assert value is None

    def test_from_ast_attribute(self):
        ast_attribute_mock = Mock(attr='decorator-name', lineno=15)

        model = DecoratorCall.from_ast_attribute(ast_attribute_mock)

        assert isinstance(model, DecoratorCall)
        assert model.decorator_name == ast_attribute_mock.attr
        assert model.line_number == ast_attribute_mock.lineno
        assert model.args == []
        assert model.kwargs == {}
        assert model.filename is None

    def test_from_ast_call(self):
        ast_call_args = [
            self.ast_mocks_factory.get_constant_mock(value="arg-1"),
            Mock("invalid type case")
        ]
        ast_call_kwargs = [
            self.ast_mocks_factory.get_keyword_mock(
                arg='keyword',
                value=self.ast_mocks_factory.get_constant_mock(value='kwarg-value')
            )
        ]
        ast_call_func = self.ast_mocks_factory.get_attribute_mock(
            attr='decorator-name',
            lineno=1,
        )
        ast_call_mock = self.ast_mocks_factory.get_call_mock(
            ast_call_args,
            ast_call_kwargs,
            ast_call_func,
        )

        result = DecoratorCall.from_ast_call(ast_call_mock)

        assert result
        assert result.decorator_name == ast_call_func.attr
        assert result.line_number == ast_call_func.lineno
        assert result.args == ['arg-1']
        assert result.kwargs == {'keyword': 'kwarg-value'}

    def test_none_case(self):
        ast_call_args = [
            self.ast_mocks_factory.get_constant_mock(value="arg-1"),
            Mock("invalid type case")
        ]
        ast_call_kwargs = [
            self.ast_mocks_factory.get_keyword_mock(
                arg='keyword',
                value=self.ast_mocks_factory.get_constant_mock(value='kwarg-value')
            )
        ]
        ast_call_func = Mock("invalid type func")
        ast_call_mock = self.ast_mocks_factory.get_call_mock(
            ast_call_args,
            ast_call_kwargs,
            ast_call_func,
        )

        result = DecoratorCall.from_ast_call(ast_call_mock)

        assert result is None
