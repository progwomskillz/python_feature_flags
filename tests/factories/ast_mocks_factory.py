import ast
from mock import Mock


class MockAstAttribute(ast.Attribute):
    def __new__(cls, *args, **kwargs):
        return Mock(spec=cls)


class MockAstCall(ast.Call):
    def __new__(cls, *args, **kwargs):
        return Mock(spec=cls)


class MockAstConstant(ast.Constant):
    def __new__(cls, *args, **kwargs):
        return Mock(spec=cls)


class MockAstKeyword(ast.keyword):
    def __new__(cls, *args, **kwargs):
        return Mock(spec=cls)


class AstMocksFactory:
    def get_attribute_mock(self, attr=None, lineno=None):
        mock = MockAstAttribute()
        mock.attr = attr
        mock.lineno = lineno
        return mock

    def get_call_mock(self, args=None, keywords=None, func=None):
        mock = MockAstCall()
        mock.args = args
        mock.keywords = keywords
        mock.func = func
        return mock

    def get_constant_mock(self, value=None):
        mock = MockAstConstant()
        mock.value = value
        return mock

    def get_keyword_mock(self, arg=None, value=None):
        mock = MockAstKeyword()
        mock.arg = arg
        mock.value = value
        return mock
