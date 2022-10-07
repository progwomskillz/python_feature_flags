from linter.models.py_module import PyModule


class PyModulesProvider:
    def __init__(self, root_path, py_paths_provider, ast_loader):
        self.root_path = root_path
        self.py_paths_provider = py_paths_provider
        self.ast_loader = ast_loader

    def get_py_modules(self):
        py_modules = []
        for file_path in self.py_paths_provider.get_paths(self.root_path):
            abstract_syntax_tree = self.ast_loader.from_file(file_path)
            py_module = PyModule(file_path, abstract_syntax_tree)
            py_modules.append(py_module)
        return py_modules
