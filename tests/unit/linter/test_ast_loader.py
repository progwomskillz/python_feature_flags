from mock import Mock, mock_open, patch

from linter import AstLoader


class TestAstLoader:
    def setup(self):
        self.ast_loader = AstLoader()

    @patch('linter.ast_loader.ast')
    @patch('builtins.open', new_callable=mock_open, read_data='print()')
    def test_from_file(self, open_mock, ast_module_mock):
        ast_mock = Mock()
        ast_module_mock.parse.return_value = ast_mock
        file_path = 'test-file-path'

        result = self.ast_loader.from_file(file_path)

        assert result == ast_mock
        ast_module_mock.parse.assert_called_once_with('print()')
        open_mock.assert_called_once_with(file_path, 'r')
