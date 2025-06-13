def register(registry):
    from qemy.plugins.model_mcarlo.mcarlo import monte_carlo_sim
    registry.register_model("mcarlo", monte_carlo_sim)
