def get_class_attributes(cls):
    members = [getattr(cls, attr) \
        for attr in dir(cls) \
            if not callable(getattr(cls, attr)) and not attr.startswith('__')]
    return members
