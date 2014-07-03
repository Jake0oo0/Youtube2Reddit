def get(value, default=None):
    config = {}
    execfile('config.conf', config)
    if value in config:
        return config[value]
    else:
        return default