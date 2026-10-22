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

        self.tokens_output = self._add_output_tab("Tokens")
        self.ast_output = self._add_output_tab("AST")
        self.semantic_output = self._add_output_tab("Semantic Analysis")
        self.errors_output = self._add_output_tab("Errors")

        status_bar = ttk.Label(
            self.root,
            textvariable=self.status,
            anchor="w",
            padding=8,
        )
        status_bar.grid(row=3, column=0, sticky="ew")

    def _add_output_tab(self, title):
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

    @staticmethod
    def _set_text(widget, content):
        widget.configure(state="normal")
        widget.delete("1.0", "end")
        widget.insert("1.0", str(content))
        widget.configure(state="disabled")

    def _load_sample(self):
        self.editor.delete("1.0", "end")
        self.editor.insert("1.0", SAMPLE_PROGRAM)
        self.status.set("Sample program loaded")

    def _clear(self):
        self.editor.delete("1.0", "end")

        for widget in (
            self.tokens_output,
            self.ast_output,
            self.semantic_output,
            self.errors_output,
        ):
            self._set_text(widget, "")

        self.status.set("Cleared")

    @staticmethod
    def _get_tokens(source):
        """Get tokens from the project's lexer."""
        lexer_module = importlib.import_module("src.lexer")

        for function_name in ("tokenize", "lex_source", "lex"):
            function = getattr(lexer_module, function_name, None)

            if callable(function):
                result = function(source)
                return "\n".join(map(str, result))

        lexer_class = getattr(lexer_module, "Lexer", None)

        if lexer_class is not None:
            lexer = lexer_class(source)

            for method_name in ("tokenize", "lex", "get_tokens"):
                method = getattr(lexer, method_name, None)

                if callable(method):
                    return "\n".join(map(str, method()))

        return (
            "Could not identify the project's lexer API.\n"
            "Check the tokenization function in src/lexer.py."
        )

    @staticmethod
    def _format_ast(tree):
        """Return a readable AST using the project's AST printer."""
        try:
            printer_module = importlib.import_module("src.ast_printer")

            for function_name in (
                "format_ast",
                "ast_to_string",
                "print_ast",
            ):
                function = getattr(printer_module, function_name, None)

                if callable(function):
                    result = function(tree)

                    if result is not None:
                        return str(result)

        except (ImportError, AttributeError) as exc:
            return (
                "AST created successfully, but the AST printer could "
                f"not be loaded: {exc}\n\n{tree!r}"
            )

        return repr(tree)

    def compile_source(self):
        source = self.editor.get("1.0", "end-1c").strip()

        if not source:
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

        try:
            tree = parse_source(source)
            ast_text = self._format_ast(tree)
        except Exception as exc:
            errors.append(f"Parser error: {exc}")

            self._set_text(self.tokens_output, token_text)
            self._set_text(
                self.ast_output,
                "AST unavailable: parsing failed.",
            )
            self._set_text(
                self.semantic_output,
                "Semantic analysis not run.",
            )
            self._set_text(self.errors_output, "\n".join(errors))

            self.status.set("Compilation failed: syntax/parser error")
            self.tabs.select(3)
            return

        try:
            semantic_result = analyze(tree)

            if semantic_result:
                semantic_text = "\n".join(map(str, semantic_result))
                errors.extend(map(str, semantic_result))
            else:
                semantic_text = "No semantic errors found."

        except Exception as exc:
            semantic_text = f"Semantic analysis failed: {exc}"
            errors.append(semantic_text)

        self._set_text(self.tokens_output, token_text)
        self._set_text(self.ast_output, ast_text)
        self._set_text(self.semantic_output, semantic_text)
        self._set_text(
            self.errors_output,
            "\n".join(errors) if errors else "No errors found.",
        )

        if errors:
            self.status.set("Compilation finished with errors")
            self.tabs.select(3)
        else:
            self.status.set("Compilation successful")
            self.tabs.select(2)


def main():
    root = tk.Tk()
    CompilerGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
