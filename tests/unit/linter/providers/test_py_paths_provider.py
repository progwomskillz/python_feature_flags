from mock import patch
from linter.providers import PyPathsProvider


class TestPyPathsProvider:
    @patch('linter.providers.py_paths_provider.os')
    def test_get_paths_invalid_file_extension(self, os_mock):
        provider = PyPathsProvider()
        prefix = 'test-prefix'
        directories = []
        filenames = ['test-filename.not_py']

        os_mock.walk.return_value = [(prefix, directories, filenames)]
        result = provider.get_paths(root_path=".")

        assert result == []

    @patch('linter.providers.py_paths_provider.os')
    def test_get_paths_exclude_case(self, os_mock):
        provider = PyPathsProvider(patterns_to_exclude=['exclude'])
        prefix_exclude = 'test-exclude-prefix'
        prefix = 'test-prefix'
        directories = []
        filenames_exclude = ['test-filename-exclude.py']
        filenames = ['test-filename.py']

        os_mock.walk.return_value = [
            (prefix_exclude, directories, filenames),
            (prefix, directories, filenames_exclude),
            (prefix_exclude, directories, filenames_exclude),
        ]
        os_mock.path.join = lambda *args: "/".join(args)
        result = provider.get_paths(".")

        assert result == []

    @patch('linter.providers.py_paths_provider.os')
    def test_get_paths(self, os_mock):
        provider = PyPathsProvider(patterns_to_exclude=['none'])
        prefix = 'test-prefix'
        directories = []
        filenames = ['valid_python_filename.py']

        os_mock.walk.return_value = [(prefix, directories, filenames)]
        os_mock.path.join = lambda *args: "/".join(args)
        result = provider.get_paths(".")

        assert result == ['test-prefix/valid_python_filename.py']
