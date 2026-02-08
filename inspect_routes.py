# inspect_routes.py
from importlib import import_module
mod = import_module('app')   # change if your module name differs
app = mod.create_app() if hasattr(mod, 'create_app') else getattr(mod, 'app')
print("Routes:")
for rule in sorted(app.url_map.iter_rules(), key=lambda r: str(r)):
    print(str(rule), "methods=", sorted(rule.methods), "args=", list(rule.arguments))
