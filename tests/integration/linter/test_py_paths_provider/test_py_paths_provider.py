from linter.providers.py_paths_provider import PyPathsProvider


class TestPyPathsProvider:
    def setup(self):
        self.provider = PyPathsProvider(['excluded_dir'])

    def test_get_paths(self):
        root_path = "./tests/integration/linter/test_py_paths_provider/"
        result = self.provider.get_paths(root_path)
        expected_result = [
            root_path + "test_py_paths_provider.py",
            root_path + "__init__.py",
            root_path + "dir/in_dir_file.py",
            root_path + "dir/__init__.py",
        ]
        assert result == expected_result
