
def register(registry):
    from qemy.plugins.model_linear_r.linear_r import LinearRPlugin
    registry.register_model(LinearRPlugin.name, LinearRPlugin)

