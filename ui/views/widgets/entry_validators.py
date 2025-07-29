def only_int(value):
    return value.isdigt() or value == ""

def only_float(value):
    if value == "":
        return True
    try:
        float(value)
        return True
    except ValueError:
        return False

