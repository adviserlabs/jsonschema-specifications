"""
A `referencing.Registry` containing schemas from the JSON Schema specification.
"""

import json

try:
    from importlib.resources import files
except ImportError:
    from importlib_resources import files  # type: ignore

from referencing import Registry, Resource


def _schemas():
    """
    All schemas we ship.
    """

    # importlib.resources.abc.Traversal doesn't have nice ways to do this that
    # I'm aware of...
    #
    # It can't recurse arbitrarily, e.g. no ``.glob()``.
    #
    # So this takes some liberties given the real layout of what we ship
    # (only 2 levels of nesting, no directories within the second level).

    for version in files(__package__).joinpath("schemas").iterdir():
        for child in version.iterdir():
            children = [child] if child.is_file() else child.iterdir()
            for path in children:
                contents = json.loads(path.read_text())
                yield Resource.from_contents(contents)


REGISTRY: Registry = (_schemas() @ Registry()).crawl()
