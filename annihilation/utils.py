def walker(paths, data):
    if not paths:
        yield data
    else:
        k = paths.pop(0)
        if k == '*':
            for item in data:
                for y in walker(paths[:], item):
                    yield y
        else:
            for y in walker(paths, data[k]):
                yield y
