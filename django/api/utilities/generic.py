def get_map(key_name, objects):
    result = {}
    for object in objects:
        key = getattr(object, key_name)
        result[key] = object
    return result
