def strtobool(v):
    v = v.lower()
    if v in ("y", "yes", "t", "true", "on", "1"):
        return True
    elif v in ("n", "no", "f", "false", "off", "0"):
        return False
    raise ValueError("invalid truth value %r" % v)
