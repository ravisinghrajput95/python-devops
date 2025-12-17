def validate_config(config: dict) -> bool:
    # Required keys must exist
    required_keys = {"service_name", "env", "port"}
    if not required_keys.issubset(config.keys()):
        return False

    # service_name must be a non-empty string
    if not isinstance(config["service_name"], str) or config["service_name"].strip() == "":
        return False

    # env must be one of allowed values
    allowed_envs = {"dev", "staging", "prod"}
    if config["env"] not in allowed_envs:
        return False

    # port must be an integer 1–65535
    if not isinstance(config["port"], int) or not (1 <= config["port"] <= 65535):
        return False

    return True


config1 = {
    "service_name": "payment-service",
    "env": "prod",
    "port": 8080
}

config2 = {
    "service_name": "",
    "env": "dev",
    "port": 3000
}

config3 = {
    "service_name": "api",
    "env": "invalid",
    "port": 8080
}

print(validate_config(config1))  # True
print(validate_config(config2))  # False (empty service_name)
print(validate_config(config3))  # False (invalid env)
