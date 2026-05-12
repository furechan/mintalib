"""Generate Markdown API documentation using pdoc introspection."""

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
    # introspect directly and filter for calc_* functions
    if not members:
        obj = mod.obj
        calc_names = sorted(n for n in dir(obj) if n.startswith("calc_"))
        for name in calc_names:
            fn = getattr(obj, name)
            try:
                sig = inspect.signature(fn)
            except (ValueError, TypeError):
                sig = None
            doc = inspect.getdoc(fn) or ""
            lines.append("---\n" if lines[-1] != "---\n" else "")
            lines.append(f"### `{clean_type(name + str(sig))}`\n" if sig else f"### `{name}`\n")
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
