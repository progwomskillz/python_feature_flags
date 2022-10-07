class LintingError:
    def __init__(self, filename, line_number, message):
        self.filename = filename
        self.line_number = line_number
        self.message = message
