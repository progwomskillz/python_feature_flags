from linter.validation_services import KwargsValidationService


class TestKwargsValidationService:
    def setup(self):
        self.service = KwargsValidationService()

    def test_validate(self):
        expected_result = ["Decorator call contains kwargs, but must not."]
        result = self.service.validate(kwargs={"key": "value"})
        assert result == expected_result
