import ast
from .decorator_call import DecoratorCall


class DecoratorCallsSearcher(ast.NodeVisitor):
    def __init__(self):
        self._decorator_calls = []

    def search(self, py_module):
        self.visit(py_module.abstract_syntax_tree)
        result = self._decorator_calls[:]
        self._decorator_calls = []
        for decorator_call in result:
            decorator_call.filename = py_module.filename
        return result

    def visit_FunctionDef(self, node):
        for decorator in node.decorator_list:
            decorator_call = None
            if isinstance(decorator, ast.Attribute):
                decorator_call = DecoratorCall.from_ast_attribute(decorator)
            if isinstance(decorator, ast.Call):
                decorator_call = DecoratorCall.from_ast_call(decorator)
            if not decorator_call:
                continue
            self._decorator_calls.append(decorator_call)
