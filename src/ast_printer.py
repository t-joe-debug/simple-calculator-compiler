try:
    from .ast_nodes import (
        Program,
        Number,
        Variable,
        BinaryOp,
        Assignment,
        PrintStatement,
    )
except ImportError:
    from ast_nodes import (
        Program,
        Number,
        Variable,
        BinaryOp,
        Assignment,
        PrintStatement,
    )

def node_label(node):
    if isinstance(node, Program):
        return "Program"
    elif isinstance(node, Number):
        return f"Number({node.value})"
    elif isinstance(node, Variable):
        return f"Variable({node.name})"
    elif isinstance(node, BinaryOp):
        return f"BinaryOp({node.operator})"
    elif isinstance(node, Assignment):
        return f"Assignment({node.name})"
    elif isinstance(node, PrintStatement):
        return "PrintStatement"
    else:
        raise TypeError(f"Unknown node: {type(node).__name__}")


def get_children(node):
    if isinstance(node, Program):
        return node.statements
    elif isinstance(node, BinaryOp):
        return [node.left, node.right]
    elif isinstance(node, Assignment):
        return [node.value]
    elif isinstance(node, PrintStatement):
        return [node.value]
    else:
        return []


def format_ast(node, prefix="", is_last=True, is_root=True):
    if is_root:
        lines = [node_label(node)]
    else:
        connector = "└── " if is_last else "├── "
        lines = [prefix + connector + node_label(node)]

    children = get_children(node)

    for i, child in enumerate(children):
        last = i == len(children) - 1

        if is_root:
            child_prefix = ""
        else:
            child_prefix = prefix + (
                "    " if is_last else "│   "
            )

        lines.append(
            format_ast(child, child_prefix, last, False)
        )

    return "\n".join(lines)


def print_ast(node):
    print(format_ast(node))


if __name__ == "__main__":
    example = Program([
        Assignment(
            "x",
            BinaryOp(
                Number(10),
                "+",
                BinaryOp(Number(5), "*", Number(2))
            )
        ),
        PrintStatement(Variable("x"))
    ])

    print_ast(example)
