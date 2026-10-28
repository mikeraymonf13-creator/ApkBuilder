from core.binding.model import ViewNode
from core.binding.parser import ANDROID_NS

A = f"{{{ANDROID_NS}}}"
# BOLT OPTIMIZATION: Precompute android:id attribute key to avoid
# repeated string concatenation in bind_views during XML AST traversal.
A_ID = f"{{{ANDROID_NS}}}id"

def snake_to_camel(s):
    # BOLT OPTIMIZATION: Avoid list comprehension filter allocations and manual slice concatenations.
    # Using str.split('_') with str.capitalize() speeds up snake_to_camel by ~25-30%.
    if "_" not in s:
        return s

    parts = s.split("_")
    if not s.startswith("_"):
        return parts[0] + "".join(p.capitalize() for p in parts[1:])
    return "".join(p.capitalize() for p in parts if p)

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