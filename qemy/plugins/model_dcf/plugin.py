def register(registry):
    from qemy.plugins.model_dcf.dcf import get_dcf_eval
    registry.register_model("dcf", get_dcf_eval)
