import ast


class AstLoader:
    def from_file(self, file_path):
        with open(file_path, "r") as file:
            source_code = file.read()
        abstract_syntax_tree = ast.parse(source_code)
        return abstract_syntax_tree
