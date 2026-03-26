"""Generate Markdown API documentation using pdoc introspection."""

import inspect
from pathlib import Path

import pdoc.doc
import pdoc.extract

MODULES = [
    "mintalib",
    "mintalib.functions",
    "mintalib.indicators",
    "mintalib.expressions",
]

OUTPUT_DIR = Path(__file__).parent.parent / "docs"


def format_signature(name, sig):
    return f"{name}{sig}"


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

    if not members:
        return "\n".join(lines)

    lines.append("---\n")

    for m in members:
        if m.kind == "function":
            sig = str(m.signature) if hasattr(m, "signature") else ""
            lines.append(f"### {format_signature(m.name, sig)}\n")
        elif m.kind == "class":
            lines.append(f"## {m.name}\n")
        else:
            lines.append(f"### {m.name}\n")

        if m.docstring:
            lines.append(m.docstring.strip())
            lines.append("")

    return "\n".join(lines)


def main():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    for module_name in MODULES:
        print(f"Generating {module_name} ...")
        content = render_module(module_name)
        filename = module_name.replace(".", ".") + ".md"
        output_path = OUTPUT_DIR / filename
        output_path.write_text(content)
        print(f"  -> {output_path}")


if __name__ == "__main__":
    main()
