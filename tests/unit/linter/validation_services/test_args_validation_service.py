from mock import patch

from linter.validation_services import ArgsValidationService


class TestArgsValidationService:
    def setup(self):
        self.service = ArgsValidationService()

    def test_validate_number_of_args_wrong_case(self):
        expected_result = "Invalid number of call args, required 1, but given 0."
        result = self.service.validate_number_of_args(None)
        assert result == expected_result

    def test_validate_number_of_args_valid_case(self):
        result = self.service.validate_number_of_args(args=("feature-flag",))
        assert result is None

    def test_validate_content_of_args_not_found_case(self):
        expected_result = "name-of-flag feature flag not found."
        result = self.service.validate_content_of_args(arg="name-of-flag")
        assert result == expected_result

    @patch('linter.validation_services.args_validation_service.os')
    def test_validate_content_of_args_wrong_flag_value_case(self, os_mock):
        expected_result = (
            "The name-of-flag feature flag has an invalid value. "
            "Possible values: ['1', 'true', '0', 'false']."
        )
        os_mock.environ = {'name-of-flag': 'wrong-value'}
        result = self.service.validate_content_of_args(arg='name-of-flag')
        assert result == expected_result

    @patch('linter.validation_services.args_validation_service.os')
    def test_validate_content_of_args_valid_case(self, os_mock):
        os_mock.environ = {'name-of-flag': 'true'}
        result = self.service.validate_content_of_args(arg="name-of-flag")
        assert result is None

    @patch('linter.validation_services.args_validation_service.os')
    def test_validate(self, os_mock):
        os_mock.environ = {'name-of-flag': 'wrong-value'}
        args = ('name-of-flag', 'wrong-flag')
        expected_result = [
            "Invalid number of call args, required 1, but given 2.",

            "The name-of-flag feature flag has an invalid value. "
            "Possible values: ['1', 'true', '0', 'false'].",

            "wrong-flag feature flag not found.",
        ]
        result = self.service.validate(args)
        assert result == expected_result

    def test_validate_no_args_case(self):
        expected_result = ["Invalid number of call args, required 1, but given 0."]
        result = self.service.validate(None)
        assert result == expected_result
