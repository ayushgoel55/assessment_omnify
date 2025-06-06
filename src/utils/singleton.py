def singleton(cls):
    instances={}
    def get_instance(*args,**kwargs):
        if  cls in instances:
            return instances[cls]
        instances[cls]=cls(*args,**kwargs)
        return instances[cls]
    return get_instance
