import os


class PyPathsProvider:
    def __init__(self, patterns_to_exclude=None):
        self.patterns_to_exclude = patterns_to_exclude or []

    def get_paths(self, root_path):
        file_paths = []
        for prefix, _, filenames in os.walk(root_path):
            file_paths += self.__build_file_paths(prefix, filenames)
        return file_paths

    def __build_file_paths(self, prefix, filenames):
        file_paths = []
        for filename in filenames:
            if not filename.endswith(".py"):
                continue
            file_path = os.path.join(prefix, filename)
            if self.__is_exclude(file_path):
                continue
            file_paths.append(file_path)
        return file_paths

    def __is_exclude(self, path):
        for pattern_to_exclude in self.patterns_to_exclude:
            if pattern_to_exclude not in path:
                continue
            return True
