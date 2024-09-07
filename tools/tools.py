import os
import sys


# Определите структуры для ваших подклассов выражений
def define_ast(output, base_name, types):
    path = os.path.join(output + f"{base_name}.py")

    with open(path, 'w') as file:
        file.write(f"from typing import Any\n\n")
        file.write(f"class {base_name}:\n")
        file.write(f"    def accept(self, visitor: 'Visitor') -> Any:\n")
        file.write(f"        raise NotImplementedError()\n\n")

        for type_name in types:
            file.write(f"class {type_name}({base_name}):\n")
            file.write(f"    def __init__(self, ")
            # Define constructor parameters here
            file.write(f"*args) -> None:\n")
            file.write(f"        super().__init__()\n")
            # Add constructor body here
            file.write(f"\n")

            # Optionally: Add methods for each type here
            file.write(f"    def accept(self, visitor: 'Visitor') -> Any:\n")
            file.write(f"        return visitor.visit_{type_name.lower()}(self)\n\n")


if __name__ == "__main__":
    output_dir = "../app/"

    # Define the types of expressions you want to generate
    define_ast(output_dir, "Expr", [
        "Binary",
        "Grouping",
        "Literal",
        "Unary",
        "Variable",
    ])
