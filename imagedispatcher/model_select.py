def select_service(payload):
    if payload.deployment == 36:
        return "deployed-model-a"
    else:
        return "deployed-model-b"
