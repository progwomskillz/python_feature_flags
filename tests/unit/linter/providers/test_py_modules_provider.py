from mock import Mock, call
from linter.providers.py_modules_provider import PyModulesProvider


class TestPyModulesProvider:
    def setup(self):
        self.root_path = "./test/root/path/"
        self.py_paths_provider_mock = Mock()
        self.ast_loader_mock = Mock()
        self.provider = PyModulesProvider(
            self.root_path,
            self.py_paths_provider_mock,
            self.ast_loader_mock,
        )

    def test_init(self):
        assert self.provider.root_path == self.root_path
        assert self.provider.py_paths_provider == self.py_paths_provider_mock
        assert self.provider.ast_loader == self.ast_loader_mock

    def test_get_py_modules(self):
        paths = [self.root_path + "file1.py", self.root_path + "file2.py"]
        self.py_paths_provider_mock.get_paths.return_value = paths
        abstract_syntax_tree_mocks = [Mock(), Mock()]
        self.ast_loader_mock.from_file.side_effect = abstract_syntax_tree_mocks

        result = self.provider.get_py_modules()

        assert len(result) == len(paths)
        assert result[0].filename == paths[0]
        assert result[0].abstract_syntax_tree == abstract_syntax_tree_mocks[0]

        assert result[1].filename == paths[1]
        assert result[1].abstract_syntax_tree == abstract_syntax_tree_mocks[1]

        self.py_paths_provider_mock.get_paths.assert_called_once_with(self.root_path)
        self.ast_loader_mock.from_file.assert_has_calls([call(path) for path in paths])
