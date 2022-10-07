import os


class ArgsValidationService:
    def validate(self, args):
        errors = []
        if number_of_args_error := self.validate_number_of_args(args):
            errors.append(number_of_args_error)
        if not args:
            return errors
        for arg in args:
            if content_of_args_error := self.validate_content_of_args(arg):
                errors.append(content_of_args_error)
        return errors

    def validate_number_of_args(self, args):
        required_args_number = 1
        args_len = len(args) if args else 0
        if args_len == required_args_number:
            return
        return (
            f"Invalid number of call args, "
            f"required {required_args_number}, "
            f"but given {args_len}."
        )

    def validate_content_of_args(self, arg):
        try:
            lower_value = os.environ[arg].lower()
        except KeyError:
            return f'{arg} feature flag not found.'

        possible_values = {
            '1': True,
            'true': True,
            '0': False,
            'false': False
        }
        if lower_value in possible_values:
            return

        return (
            f'The {arg} feature flag has an invalid value. '
            f'Possible values: {list(possible_values.keys())}.'
        )
