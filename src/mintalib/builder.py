import inspect
import warnings


def annotate_parameter(param):
    if param.annotation in ("int", "long"):
        return param.replace(annotation=int)

    if param.annotation in ("bint", "bool"):
        return param.replace(annotation=bool)

    if param.annotation == "str":
        return param.replace(annotation=str)

    if param.annotation is inspect._empty:
        if type(param.default) in (int, float, bool):
            return param.replace(annotation=type(param.default))

        if param.name in ("expr", "ma_type"):
            return param.replace(annotation=str)

        if param.name == "period":
            return param.replace(annotation=int)

        if param.name not in ("series", "prices"):
            warnings.warn(f"Missing annotation for {param.name}", stacklevel=2)

    return param
