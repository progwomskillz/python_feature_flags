from mock import Mock
from linter.validation_services import DecoratorCallValidationService


class TestDecoratorCallValidationService:
    def setup(self):
        self.args_validation_service_mock = Mock()
        self.kwargs_validation_service_mock = Mock()
        self.service = DecoratorCallValidationService(
            self.args_validation_service_mock,
            self.kwargs_validation_service_mock,
        )

    def test_init(self):
        assert self.service.args_validation_service == self.args_validation_service_mock
        assert self.service.kwargs_validation_service == self.kwargs_validation_service_mock

    def test_validate(self):
        args_messages = ["args-message-1", "args-message-2"]
        kwargs_messages = ["kwargs-message-1", "kwargs-message-2"]
        decorator_call_mock = Mock(args=('test-args',), kwargs={'test': 'kwargs'})

        args_validate_mock = Mock(return_value=args_messages)
        self.args_validation_service_mock.validate = args_validate_mock
        kwargs_validate_mock = Mock(return_value=kwargs_messages)
        self.kwargs_validation_service_mock.validate = kwargs_validate_mock
        result = self.service.validate(decorator_call_mock)

        assert result == [*args_messages, *kwargs_messages]
        args_validate_mock.assert_called_once_with(decorator_call_mock.args)
        kwargs_validate_mock.assert_called_once_with(decorator_call_mock.kwargs)
