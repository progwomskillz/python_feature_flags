class KwargsValidationService:
    def validate(self, kwargs):
        error_messages = []
        if kwargs:
            error_messages.append("Decorator call contains kwargs, but must not.")
        return error_messages
