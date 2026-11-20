from core.binding.model import ViewNode
from core.binding.parser import ANDROID_NS

A = f"{{{ANDROID_NS}}}"
# BOLT OPTIMIZATION: Precompute android:id attribute key to avoid
# repeated string concatenation in bind_views during XML AST traversal.
A_ID = f"{{{ANDROID_NS}}}id"

# BOLT OPTIMIZATION: Memoize converted snake_case identifiers and optimize
# string partitioning logic to eliminate redundant split/generator allocations during view binding resolution.
_camel_cache = {}

def snake_to_camel(s):
    if "_" not in s:
        return s

    cached = _camel_cache.get(s)
    if cached is not None:
        return cached

    parts = s.split("_")
    first = parts[0]
    rest = [p[0].upper() + p[1:] for p in parts[1:] if p]
    if not first:
        res = "".join(rest)
    else:
        res = first + "".join(rest)

    _camel_cache[s] = res
    return res

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