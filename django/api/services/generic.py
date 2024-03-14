# gets a map of specified model values to model instances
def get_objects_map(qs, key_field):
    result = {}
    for object in qs:
        key = getattr(object, key_field, None)
        if key:
            result[key] = object
    return result
