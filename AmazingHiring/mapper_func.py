def mapper(values, param: bool):
    if values is None:
        if param is True:
            return None
        return ['any']
    elif len(values) > 1:
        return values
    elif values == ['no']:
        if param is True:
            return values
        return None
    return values

