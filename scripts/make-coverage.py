"""Generate interface coverage table for all indicators."""

from pathlib import Path

import mintalib.core as core
import mintalib.functions as functions
import mintalib.indicators as indicators
import mintalib.expressions as expressions
import mintalib.pandas as mpandas
import mintalib.polars as mpolars

OUTPUT = Path(__file__).parent.parent / "output" / "coverage.md"

# Use core as authoritative source of indicator names
all_bases = sorted(n.removeprefix("calc_") for n in dir(core) if n.startswith("calc_"))

func_names  = {n for n in dir(functions)  if not n.startswith("_") and callable(getattr(functions, n))}
ind_names   = {n.lower() for n in dir(indicators)  if not n.startswith("_") and callable(getattr(indicators, n))}
expr_names  = {n.lower() for n in dir(expressions) if not n.startswith("_") and callable(getattr(expressions, n))}
pd_df_names = {n.lower() for n in dir(mpandas.DataFrameCalc)  if not n.startswith("_")}
pd_s_names  = {n.lower() for n in dir(mpandas.SeriesCalc)     if not n.startswith("_")}
pl_df_names = {n.lower() for n in dir(mpolars.DataFrameCalc)  if not n.startswith("_")}
pl_s_names  = {n.lower() for n in dir(mpolars.SeriesCalc)     if not n.startswith("_")}
pl_e_names  = {n.lower() for n in dir(mpolars.ExpressionCalc) if not n.startswith("_")}

Y, N = "✓", ""

headers = ["name", "core", "function", "indicator", "expression",
           "pd.DataFrame", "pd.Series", "pl.DataFrame", "pl.Series", "pl.Expr"]

rows = []
for base in all_bases:
    rows.append([
        f"`{base}`",
        Y,
        Y if base in func_names  else N,
        Y if base in ind_names   else N,
        Y if base in expr_names  else N,
        Y if base in pd_df_names else N,
        Y if base in pd_s_names  else N,
        Y if base in pl_df_names else N,
        Y if base in pl_s_names  else N,
        Y if base in pl_e_names  else N,
    ])

lines = ["# Interface Coverage\n"]
lines.append("| " + " | ".join(headers) + " |")
lines.append("| " + " | ".join(["---"] * len(headers)) + " |")
for row in rows:
    lines.append("| " + " | ".join(row) + " |")
lines.append("")

OUTPUT.write_text("\n".join(lines))
print(f"Written to {OUTPUT}")


if __name__ == "__main__":
    pass
