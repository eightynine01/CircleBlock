
def unused(_name) -> bool:
    sl = ['.', '_']
    return any([
        *[_name.startswith(i) for i in sl],
        not _name.endswith('.py')
    ])
