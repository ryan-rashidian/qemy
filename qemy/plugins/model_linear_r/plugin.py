def register(registry):
    from qemy.plugins.model_linear_r.linear_r import linear_r
    registry.register_model("linear_r", linear_r)
