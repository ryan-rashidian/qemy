
def register(registry):
    from qemy.plugins.model_dcf.dcf import DCFPlugin
    registry.register_model(DCFPlugin.name, DCFPlugin)
