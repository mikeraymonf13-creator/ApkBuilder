from core.binding.model import ViewNode
from core.binding.parser import ANDROID_NS

A = f"{{{ANDROID_NS}}}"
# BOLT OPTIMIZATION: Precompute android:id attribute key to avoid
# repeated string concatenation in bind_views during XML AST traversal.
A_ID = f"{{{ANDROID_NS}}}id"

def snake_to_camel(s):
    if not s or "_" not in s:
        return s

    parts = [p for p in s.split("_") if p]
    if not parts:
        return ""

    if s.startswith("_"):
        return "".join(p.capitalize() for p in parts)
    return parts[0] + "".join(p.capitalize() for p in parts[1:])

def normalize_id(value):
    if not value:
        return None
    # BOLT OPTIMIZATION: Use rsplit with maxsplit=1 to avoid full splitting array allocations.
    return value.rsplit("/", 1)[-1]

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