from core.binding.model import ViewNode
from core.binding.parser import ANDROID_NS

A = f"{{{ANDROID_NS}}}"
# BOLT OPTIMIZATION: Precompute android:id attribute key to avoid
# repeated string concatenation in bind_views during XML AST traversal.
A_ID = f"{{{ANDROID_NS}}}id"

import functools

# BOLT OPTIMIZATION: Cache converted snake_case to camelCase identifiers
# using lru_cache to eliminate repeated string splitting, list creation, and joining
# during XML layout view binding generation.
@functools.lru_cache(maxsize=1024)
def snake_to_camel(s):
    if "_" not in s:
        return s

    partes = s.split("_")
    if not s.startswith("_"):
        first = partes[0]
        rest = [p[0].upper() + p[1:] for p in partes[1:] if p]
        return first + ''.join(rest) if first else ''.join(rest)
    else:
        rest = [p[0].upper() + p[1:] for p in partes if p]
        return ''.join(rest)

def normalize_id(value):
    if not value:
        return None
    return value.split("/")[-1]

def bind_views(elem, child=False):
    view_id = normalize_id(elem.get(A_ID))
    binding_id = None
    if not view_id and not child:
        view_id = "rootView"
    if view_id:
        binding_id = snake_to_camel(view_id)
    children = [
        bind_views(child, child=True)
        for child in elem
        if isinstance(child.tag, str)
    ]
    return ViewNode(elem.tag, view_id, binding_id, children)