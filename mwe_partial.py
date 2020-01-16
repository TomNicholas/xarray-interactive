from ipywidgets import interact
from functools import partial, update_wrapper

# This is to avoid the error
# AttributeError: 'functools.partial' object has no attribute '__name__'
def wrapped_partial(func, *args, **kwargs):
    partial_func = partial(func, *args, **kwargs)
    update_wrapper(partial_func, func)
    return partial_func

def g(dat, x):
    print("dat={dat} from inside g")
    return dat

g_plus_dat = wrapped_partial(g, dat='a')

interact(g_plus_dat, x=10)
