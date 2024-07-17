def get_map(key_name, objects):
    result = {}
    for object in objects:
        key = getattr(object, key_name)
        result[key] = object
    return result


def get_unified_map(key_name, value_name, maps):
    result = {}
    for map in maps:
        key = map.get(key_name)
        value = map.get(value_name)
        result[key] = value
    return result
