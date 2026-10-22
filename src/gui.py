
"""Tkinter GUI for the Simple Calculator Language compiler."""

import importlib
import tkinter as tk
from tkinter import messagebox, ttk

from src.parser import parse_source
from src.semantic import analyze


SAMPLE_PROGRAM = """x = 10;
y = x % 3;
print(y);
"""


class CompilerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Simple Calculator Language Compiler")
        self.root.geometry("1100x760")
        self.root.minsize(800, 550)

        self.status = tk.StringVar(value="Ready")
        self._build_ui()
        self._load_sample()

    def _build_ui(self):
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(1, weight=1)
        self.root.rowconfigure(2, weight=1)

        header = ttk.Frame(self.root, padding=12)
        header.grid(row=0, column=0, sticky="ew")
        header.columnconfigure(0, weight=1)

        ttk.Label(
            header,
            text="Simple Calculator Language",
            font=("Segoe UI", 18, "bold"),
        ).grid(row=0, column=0, sticky="w")

        ttk.Label(
            header,
            text="Compiler Front End | Lexer | Parser | AST | Semantics",
        ).grid(row=1, column=0, sticky="w", pady=(4, 0))

        editor_frame = ttk.LabelFrame(
            self.root, text="Source Code", padding=8
        )
        editor_frame.grid(
            row=1, column=0, sticky="nsew", padx=12, pady=6
        )
        editor_frame.columnconfigure(0, weight=1)
        editor_frame.rowconfigure(0, weight=1)

        self.editor = tk.Text(
            editor_frame,
            wrap="none",
            undo=True,
            font=("Consolas", 12),
            height=10,
        )
        self.editor.grid(row=0, column=0, sticky="nsew")

        y_scroll = ttk.Scrollbar(
            editor_frame,
            orient="vertical",
            command=self.editor.yview,
        )
        y_scroll.grid(row=0, column=1, sticky="ns")
        self.editor.configure(yscrollcommand=y_scroll.set)

        x_scroll = ttk.Scrollbar(
            editor_frame,
            orient="horizontal",
            command=self.editor.xview,
        )
        x_scroll.grid(row=1, column=0, sticky="ew")
        self.editor.configure(xscrollcommand=x_scroll.set)

        buttons = ttk.Frame(editor_frame)
        buttons.grid(
            row=2, column=0, columnspan=2, sticky="ew", pady=8
        )

        ttk.Button(
            buttons, text="Compile", command=self.compile_source
        ).pack(side="left", padx=(0, 8))

        ttk.Button(
            buttons, text="Load Sample", command=self._load_sample
        ).pack(side="left", padx=4)

        ttk.Button(
            buttons, text="Clear", command=self._clear
        ).pack(side="left", padx=4)

        results = ttk.LabelFrame(
            self.root, text="Compiler Results", padding=8
        )
        results.grid(
            row=2, column=0, sticky="nsew", padx=12, pady=6
        )
        results.columnconfigure(0, weight=1)
        results.rowconfigure(0, weight=1)

        self.tabs = ttk.Notebook(results)
        self.tabs.grid(row=0, column=0, sticky="nsew")

        # Keep the existing result tabs and their order.
        self.tokens_output = self._add_output_tab("Tokens")

        # The AST tab uses a graphical canvas instead of plain text.
        self.ast_canvas = self._add_ast_tab("AST")

        self.semantic_output = self._add_output_tab(
            "Semantic Analysis"
        )
        self.errors_output = self._add_output_tab("Errors")
        self.program_output = self._add_output_tab("Output")

        status_bar = ttk.Label(
            self.root,
            textvariable=self.status,
            anchor="w",
            padding=8,
        )
        status_bar.grid(row=3, column=0, sticky="ew")

    def _add_output_tab(self, title):
        """Create a regular text output tab."""
        frame = ttk.Frame(self.tabs, padding=5)
        frame.rowconfigure(0, weight=1)
        frame.columnconfigure(0, weight=1)

        output = tk.Text(
            frame,
            wrap="word",
            state="disabled",
            font=("Consolas", 10),
            height=8,
        )
        output.grid(row=0, column=0, sticky="nsew")

        scrollbar = ttk.Scrollbar(
            frame,
            orient="vertical",
            command=output.yview,
        )
        scrollbar.grid(row=0, column=1, sticky="ns")
        output.configure(yscrollcommand=scrollbar.set)

        self.tabs.add(frame, text=title)
        return output

    def _add_ast_tab(self, title):
        """Create a scrollable canvas for displaying the AST."""
        frame = ttk.Frame(self.tabs, padding=5)
        frame.rowconfigure(0, weight=1)
        frame.columnconfigure(0, weight=1)

        canvas = tk.Canvas(
            frame,
            background="white",
            highlightthickness=0,
        )
        canvas.grid(row=0, column=0, sticky="nsew")

        y_scroll = ttk.Scrollbar(
            frame,
            orient="vertical",
            command=canvas.yview,
        )
        y_scroll.grid(row=0, column=1, sticky="ns")

        x_scroll = ttk.Scrollbar(
            frame,
            orient="horizontal",
            command=canvas.xview,
        )
        x_scroll.grid(row=1, column=0, sticky="ew")

        canvas.configure(
            yscrollcommand=y_scroll.set,
            xscrollcommand=x_scroll.set,
        )

        self.tabs.add(frame, text=title)
        return canvas

    @staticmethod
    def _set_text(widget, content):
        """Replace the content of a read-only result widget."""
        widget.configure(state="normal")
        widget.delete("1.0", "end")
        widget.insert("1.0", str(content))
        widget.configure(state="disabled")

    def _draw_ast(self, tree, message=None):
        """Draw the AST as a top-down tree with connecting branches."""
        canvas = self.ast_canvas
        canvas.delete("all")

        if tree is None:
            canvas.create_text(
                25,
                25,
                text=message or "AST will appear here after parsing.",
                anchor="nw",
                font=("Segoe UI", 11),
                fill="#555555",
            )
            canvas.configure(scrollregion=(0, 0, 900, 500))
            return

        def describe(node):
            """Return a display label and the node's child nodes."""
            kind = type(node).__name__

            if kind == "Program":
                return "Program", list(node.statements)

            if kind == "Assignment":
                return f"Assignment: {node.target}", [node.expression]

            if kind == "PrintStatement":
                return "Print", [node.expression]

            if kind == "BinaryOp":
                return str(node.operator), [node.left, node.right]

            if kind == "UnaryOp":
                return str(node.operator), [node.operand]

            if kind == "Variable":
                return f"Variable: {node.name}", []

            if kind == "Number":
                return f"Number: {node.value}", []

            # Fallback for other AST node types.
            children = []

            for attribute in ("statements", "body"):
                value = getattr(node, attribute, None)
                if isinstance(value, (list, tuple)):
                    children = value
                    break

            if not children:
                for attribute in ("expression", "operand", "left", "right"):
                    value = getattr(node, attribute, None)
                    if value is not None and not isinstance(
                        value, (str, int, float, bool)
                    ):
                        children.append(value)

            return kind, children

        def build_tree(node):
            label, children = describe(node)
            return {
                "label": label,
                "children": [build_tree(child) for child in children],
            }

        root_node = build_tree(tree)

        # Calculate positions: leaves first, parents centered above children.
        leaf_counter = [0]
        horizontal_gap = 165
        vertical_gap = 105
        nodes = []

        def position_nodes(node, depth=0):
            children = node["children"]

            if not children:
                x = 100 + leaf_counter[0] * horizontal_gap
                leaf_counter[0] += 1
            else:
                child_positions = [
                    position_nodes(child, depth + 1)
                    for child in children
                ]
                x = sum(child_positions) / len(child_positions)

            node["x"] = x
            node["y"] = 55 + depth * vertical_gap
            nodes.append(node)
            return x

        position_nodes(root_node)

        # Draw the branches before the nodes.
        for node in nodes:
            for child in node["children"]:
                canvas.create_line(
                    node["x"],
                    node["y"] + 22,
                    child["x"],
                    child["y"] - 22,
                    fill="#8193A5",
                    width=2,
                )

        # Draw each node and its label.
        for node in nodes:
            x = node["x"]
            y = node["y"]

            text_id = canvas.create_text(
                x,
                y,
                text=node["label"],
                font=("Segoe UI", 10, "bold"),
                fill="#17324D",
                justify="center",
                width=135,
            )

            bounds = canvas.bbox(text_id)
            padding_x = 12
            padding_y = 9

            rectangle_id = canvas.create_rectangle(
                bounds[0] - padding_x,
                bounds[1] - padding_y,
                bounds[2] + padding_x,
                bounds[3] + padding_y,
                fill="#E8F2FF",
                outline="#3973AC",
                width=2,
            )

            canvas.tag_lower(rectangle_id, text_id)

        bounds = canvas.bbox("all")

        if bounds:
            margin = 45
            canvas.configure(
                scrollregion=(
                    min(0, bounds[0] - margin),
                    min(0, bounds[1] - margin),
                    bounds[2] + margin,
                    bounds[3] + margin,
                )
            )

    def _load_sample(self):
        self.editor.delete("1.0", "end")
        self.editor.insert("1.0", SAMPLE_PROGRAM)
        self.status.set("Sample program loaded")

    def _clear(self):
        self.editor.delete("1.0", "end")

        for widget in (
            self.tokens_output,
            self.semantic_output,
            self.errors_output,
            self.program_output,
        ):
            self._set_text(widget, "")

        self._draw_ast(None)
        self.status.set("Cleared")

    @staticmethod
    def _get_tokens(source):
        """Get tokens from the project's lexer."""
        lexer_module = importlib.import_module("src.lexer")

        for function_name in ("tokenize", "lex_source", "lex"):
            function = getattr(lexer_module, function_name, None)

            if callable(function):
                return "\n".join(map(str, function(source)))

        lexer_class = getattr(lexer_module, "Lexer", None)

        if lexer_class is not None:
            lexer = lexer_class(source)

            for method_name in ("tokenize", "lex", "get_tokens"):
                method = getattr(lexer, method_name, None)

                if callable(method):
                    return "\n".join(map(str, method()))

        return "Could not identify the lexer API."

    @staticmethod
    def _execute_ast(tree):
        """Evaluate the calculator AST and collect print() output."""
        variables = {}
        printed_values = []

        def evaluate(node):
            kind = type(node).__name__

            if kind == "Program":
                for statement in node.statements:
                    evaluate(statement)
                return None

            if kind == "Assignment":
                variables[node.target] = evaluate(node.expression)
                return None

            if kind == "PrintStatement":
                printed_values.append(str(evaluate(node.expression)))
                return None

            if kind == "Number":
                return node.value

            if kind == "Variable":
                if node.name not in variables:
                    raise ValueError(
                        f"Undefined variable: {node.name}"
                    )
                return variables[node.name]

            if kind == "BinaryOp":
                left = evaluate(node.left)
                right = evaluate(node.right)
                operator = node.operator

                if operator in ("/", "%") and right == 0:
                    raise ValueError("Division or modulo by zero.")

                operations = {
                    "+": lambda: left + right,
                    "-": lambda: left - right,
                    "*": lambda: left * right,
                    "/": lambda: left / right,
                    "%": lambda: left % right,
                }

                if operator not in operations:
                    raise ValueError(
                        f"Unsupported operator: {operator}"
                    )

                return operations[operator]()

            if kind == "UnaryOp":
                operator = node.operator
                operand = evaluate(node.operand)

                if operator == "-":
                    return -operand
                if operator == "+":
                    return +operand

                raise ValueError(
                    f"Unsupported unary operator: {operator}"
                )

            raise ValueError(f"Unsupported AST node: {kind}")

        evaluate(tree)
        return "\n".join(printed_values)

    def compile_source(self):
        source = self.editor.get("1.0", "end-1c").strip()

        # Clear results from the previous compilation.
        for widget in (
            self.tokens_output,
            self.semantic_output,
            self.errors_output,
            self.program_output,
        ):
            self._set_text(widget, "")

        self._draw_ast(None)

        if not source:
            self.status.set("Please enter a program.")
            messagebox.showwarning(
                "Empty Source",
                "Please enter a program first.",
            )
            return

        errors = []

        try:
            token_text = self._get_tokens(source)
        except Exception as exc:
            token_text = f"Lexer error: {exc}"
            errors.append(token_text)

        try:
            tree = parse_source(source)
            self._draw_ast(tree)
        except Exception as exc:
            errors.append(f"Parser error: {exc}")

            self._set_text(self.tokens_output, token_text)
            self._draw_ast(
                None,
                "AST unavailable: parsing failed.",
            )
            self._set_text(
                self.semantic_output,
                "Semantic analysis not run.",
            )
            self._set_text(self.errors_output, "\n".join(errors))

            self.status.set("Compilation failed: parser error")
            self.tabs.select(3)
            return

        try:
            semantic_result = analyze(tree)

            if semantic_result:
                if isinstance(semantic_result, (list, tuple)):
                    diagnostics = list(map(str, semantic_result))
                else:
                    diagnostics = [str(semantic_result)]

                semantic_text = "\n".join(diagnostics)
                errors.extend(diagnostics)
            else:
                semantic_text = "No semantic errors found."

        except Exception as exc:
            semantic_text = f"Semantic analysis failed: {exc}"
            errors.append(semantic_text)

        self._set_text(self.tokens_output, token_text)
        self._set_text(self.semantic_output, semantic_text)

        if errors:
            self._set_text(self.program_output, "")
            self._set_text(self.errors_output, "\n".join(errors))
            self.status.set("Compilation finished with errors")
            self.tabs.select(3)
            return

        # Run the program only if parsing and semantic analysis succeed.
        try:
            result = self._execute_ast(tree)

            self._set_text(
                self.program_output,
                result if result else "(No print output)",
            )
            self._set_text(self.errors_output, "No errors found.")
            self.status.set("Compilation successful")
            self.tabs.select(4)

        except Exception as exc:
            self._set_text(self.program_output, "")
            self._set_text(
                self.errors_output,
                f"Execution error: {exc}",
            )
            self.status.set("Execution failed")
            self.tabs.select(3)


def main():
    root = tk.Tk()
    CompilerGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
