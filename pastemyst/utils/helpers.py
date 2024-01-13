from typing import Callable, Any


def camel_to_snake(s: str) -> str:
    """
    Converts a camel case string to snake case.

    Args:
        s (str): The camel case string to convert.

    Returns:
        str: The converted snake case string.

    Example:
        >>> camel_to_snake("camelCase")
        'camel_case'

    """
    return "".join(["_" + c.lower() if c.isupper() else c for c in s]).lstrip("_")


def mangle_attr(source: Any, attr: str) -> str:
    """
    source: https://stackoverflow.com/a/7789483
    :param source: The source object whose attribute is to be mangled. Can be any object.
    :param attr: The attribute to be mangled. Should be a string.
    :return: A mangled version of the attribute, if it meets the mangle condition. Otherwise, the attribute itself is returned.
    """
    if not attr.startswith("__") or attr.endswith("__") or "." in attr:
        return attr
    if not hasattr(source, "__bases__"):
        source = source.__class__
    return "_%s%s" % (source.__name__.lstrip("_"), attr)


async def run_later(delay: int, task: Callable) -> Any:
    #await asynclib.sleep(delay)
    # noinspection PyUnresolvedReferences
    return await task
