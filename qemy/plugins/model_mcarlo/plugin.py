
def register(registry):
    from qemy.plugins.model_mcarlo.mcarlo import MCarloPlugin
    registry.register_model(MCarloPlugin.name, MCarloPlugin)

