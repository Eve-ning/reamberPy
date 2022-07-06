import cProfile

def profile(fun):
    def wrapper(*args, **kwargs):
        pr = cProfile.Profile()
        pr.enable()
        fun(*args, **kwargs)
        pr.disable()
        # after your program ends
        pr.print_stats(sort="tottime")
    return wrapper
