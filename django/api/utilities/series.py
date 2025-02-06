# expects a Pandas series and returns a map f: value -> [indices]
def get_map_of_values_to_indices(series, index_offset=0):
    result = {}
    for index, value in series.items():
        if result.get(value) is None:
            result[value] = []
        result[value].append(index + index_offset)
    return result
