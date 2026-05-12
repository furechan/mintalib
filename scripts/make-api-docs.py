"""Generate Markdown API documentation using pdoc introspection."""

import ast
import inspect
from pathlib import Path

import pdoc.doc
import pdoc.extract

MODULES = [
    "mintalib",
    "mintalib.core",
    "mintalib.functions",
    "mintalib.indicators",
    "mintalib.expressions",
]

OUTPUT_DIR = Path(__file__).parent.parent / "docs"


def clean_type(text: str) -> str:
    return text.replace("polars.expr.expr.Expr", "polars.Expr")


def format_signature(name, sig):
    return f"`{clean_type(name + str(sig))}`"


def render_module(module_name: str) -> str:
    mod = pdoc.doc.Module(
        pdoc.extract.load_module(pdoc.extract.parse_spec(module_name))
    )

    lines = []
    lines.append(f"# {module_name}\n")

    if mod.docstring:
        lines.append(mod.docstring.strip())
        lines.append("")

    members = [
        m for m in mod.flattened_own_members
        if not m.name.startswith("_") and m.kind in ("function", "class", "variable")
    ]

    # Fallback for modules with empty __all__ (e.g. mintalib.core):
    # read signatures from the adjacent .pyi stub (it has full type hints,
    # unlike inspect.signature on a compiled Cython function), and pair
    # them with docstrings from the live module.
    if not members:
        obj = mod.obj
        obj_file = getattr(obj, "__file__", None)
        # Compiled extensions are named e.g. "core.cpython-311-darwin.so" —
        # strip the ABI tags by taking the basename up to the first dot.
        if obj_file:
            obj_path = Path(obj_file)
            stem = obj_path.name.split(".", 1)[0]
            pyi_path = obj_path.parent / f"{stem}.pyi"
        else:
            pyi_path = None
        tree = ast.parse(pyi_path.read_text()) if pyi_path and pyi_path.exists() else None
        stub_funcs = {
            node.name: node for node in (tree.body if tree else [])
            if isinstance(node, ast.FunctionDef) and not node.name.startswith("_")
        }
        names = sorted(stub_funcs) if stub_funcs else sorted(
            n for n in dir(obj) if n.startswith("calc_")
        )
        for name in names:
            node = stub_funcs.get(name)
            if node is not None:
                args_str = ast.unparse(node.args)
                ret_str = f" -> {ast.unparse(node.returns)}" if node.returns else ""
                sig_str = f"({args_str}){ret_str}"
            else:
                fn = getattr(obj, name, None)
                try:
                    sig_str = str(inspect.signature(fn)) if fn else ""
                except (ValueError, TypeError):
                    sig_str = ""
            fn = getattr(obj, name, None)
            doc = inspect.getdoc(fn) or "" if fn else ""
            # Cython prepends a "name(sig)" line to docstrings — strip it.
            doc_lines = doc.splitlines()
            if doc_lines and doc_lines[0].lstrip().startswith(name + "("):
                doc_lines = doc_lines[1:]
                while doc_lines and not doc_lines[0].strip():
                    doc_lines = doc_lines[1:]
            doc = "\n".join(doc_lines)
            lines.append("---\n" if lines[-1] != "---\n" else "")
            lines.append(f"### `{clean_type(name + sig_str)}`\n" if sig_str else f"### `{name}`\n")
            if doc:
                lines.append(doc)
                lines.append("")
        return "\n".join(lines)

    lines.append("---\n")

    for m in members:
        if m.kind == "function":
            sig = str(m.signature) if hasattr(m, "signature") else ""
            lines.append(f"### {format_signature(m.name, sig)}\n")
        elif m.kind == "class":
            lines.append(f"## {m.name}\n")
        else:
            annotation = getattr(m, "annotation_str", "").lstrip(": ")
            default = getattr(m, "default_value_str", "")
            if annotation:
                lines.append(f"### `{clean_type(m.name + ': ' + annotation)}`\n")
            else:
                lines.append(f"### `{m.name}`\n")
            if not m.docstring and default:
                value = repr(m.obj) if hasattr(m, "obj") and m.obj is not None else default
                lines.append(value)
                lines.append("")

        if m.docstring:
            lines.append(m.docstring.strip())
            lines.append("")

    return "\n".join(lines)


def main():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    for module_name in MODULES:
        print(f"Generating {module_name} ...")
        content = render_module(module_name)
        filename = module_name + ".md"
        output_path = OUTPUT_DIR / filename
        output_path.write_text(content)
        print(f"  -> {output_path}")


if __name__ == "__main__":
    main()
