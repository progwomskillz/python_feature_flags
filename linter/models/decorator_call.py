import ast


class DecoratorCall:
    def __init__(self):
        self.decorator_name = None
        self.filename = None
        self.line_number = None
        self.args = None
        self.kwargs = None

    @staticmethod
    def from_ast_attribute(ast_attribute):
        decorator_call = DecoratorCall()
        decorator_call.decorator_name = ast_attribute.attr
        decorator_call.line_number = ast_attribute.lineno
        decorator_call.args = []
        decorator_call.kwargs = {}
        return decorator_call

    @staticmethod
    def from_ast_call(ast_call):
        call_args = [
            item.value
            for item in ast_call.args
            if isinstance(item, ast.Constant)
        ]
        call_kwargs = {
            item.arg: item.value.value
            for item in ast_call.keywords
            if isinstance(item, ast.keyword)
            if isinstance(item.value, ast.Constant)
        }
        if not isinstance(ast_call.func, ast.Attribute):
            return None
        decorator_call = DecoratorCall.from_ast_attribute(ast_call.func)
        decorator_call.args = call_args
        decorator_call.kwargs = call_kwargs
        return decorator_call
