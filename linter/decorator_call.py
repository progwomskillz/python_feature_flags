import ast


class DecoratorCall:
    def __init__(self, decorator_name, line_number, call_args, call_kwargs):
        self.decorator_name = decorator_name
        self.line_number = line_number
        self.call_args = call_args
        self.call_kwargs = call_kwargs

    @staticmethod
    def from_ast_attribute(ast_attribute):
        decorator_method_name = ast_attribute.attr
        decorator_call = DecoratorCall(
            decorator_name=decorator_method_name,
            line_number=ast_attribute.lineno,
            call_args=None,
            call_kwargs=None,
        )
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
        decorator_call.call_args = call_args or None
        decorator_call.call_kwargs = call_kwargs or None
        return decorator_call
