class ErrorMessageBuilder:
    def build(self, errors):
        error_lines = [
            f"\n{error.filename}:{error.line_number} - {error.message}"
            for error in errors
        ]
        return "".join(error_lines)
