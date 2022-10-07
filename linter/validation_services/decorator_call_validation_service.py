class DecoratorCallValidationService:
    def __init__(self, args_validation_service, kwargs_validation_service):
        self.args_validation_service = args_validation_service
        self.kwargs_validation_service = kwargs_validation_service

    def validate(self, decorator_call):
        error_messages = [
            *self.args_validation_service.validate(decorator_call.args),
            *self.kwargs_validation_service.validate(decorator_call.kwargs)
        ]
        return error_messages
