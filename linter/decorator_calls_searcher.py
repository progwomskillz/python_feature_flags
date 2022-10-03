import ast
from .decorator_call import DecoratorCall


class DecoratorCallsSearcher(ast.NodeVisitor):
    def __init__(self):
        self._decorator_calls = []

    def search(self, code):
        abstract_syntax_tree = ast.parse(code)
        self.visit(abstract_syntax_tree)
        result = self._decorator_calls[:]
        self._decorator_calls = []
        return result

    def visit_FunctionDef(self, node):
        for decorator in node.decorator_list:
            decorator_call = None
            if isinstance(decorator, ast.Attribute):
                decorator_call = DecoratorCall.from_ast_attribute(decorator)
            if isinstance(decorator, ast.Call):
                decorator_call = DecoratorCall.from_ast_call(decorator)
            if decorator_call is not None:
                self._decorator_calls.append(decorator_call)
