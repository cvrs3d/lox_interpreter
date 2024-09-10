import os


def define_ast(output_dir: str, base_name: str, types: list[str]) -> None:
    path = os.path.join(output_dir, base_name + ".py")
    with open(path, 'w') as f:
        f.write(f"class {base_name}:\n")
        f.write("    pass\n\n")

        # Define the base visitor interface.
        define_visitor(f, base_name, types)

        # Define each of the AST classes.
        for type_def in types:
            class_name, fields = map(str.strip, type_def.split(":"))
            define_type(f, base_name, class_name, fields)


def define_visitor(f, base_name: str, types: list[str]) -> None:
    f.write(f"class Visitor:\n")
    for type_def in types:
        class_name = type_def.split(":")[0].strip()
        f.write(f"    def visit_{class_name.lower()}(self, {base_name.lower()}: '{class_name}') -> Any:\n")
        f.write(f"        pass\n\n")


def define_type(f, base_name: str, class_name: str, field_list: str) -> None:
    f.write(f"class {class_name}({base_name}):\n")
    f.write(f"    def __init__(self, {field_list}) -> None:\n")
    fields = field_list.split(", ")
    for field in fields:
        name, _ = field.split()
        f.write(f"        self.{name} = {name}\n")
    f.write("\n")

    # Define the accept method in the subclass.
    f.write(f"    def accept(self, visitor: 'Visitor') -> Any:\n")
    f.write(f"        return visitor.visit_{class_name.lower()}(self)\n\n")


if __name__ == "__main__":
    define_ast("../app/", "Stmt", [
        "Expression : Expr expression",
        "Print      : Expr expression"
    ])
