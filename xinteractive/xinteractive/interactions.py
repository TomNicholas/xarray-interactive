import ipywidgets as widgets

from xarray.core.utils import either_dict_or_kwargs


def indexing(da, func, func_kwargs={}, continuous_update=True,
             **indexers_kwargs):
    """
    Interactively choose indexes of a DataArray on which to apply func.

    Use in the same way as ipyywidgets.interact, i.e. as a function

    `interactive.indexing(f=lambda da: np.sin(da), time=20, position=4.5)`

    or as a decorator

    `@interactive.indexing(time=20, position=4.5)
    lambda da: np.sin(da)`

    Both syntaxes would apply `np.sin`, but create interactive sliders for time
    and position indexes.

    Parameters
    ----------
    func
        Function which accepts a DataArray, to be applied interactively.
    func_kwargs
        Keyword arguments to pass directly to the function.
    continuous_update : bool, optional
        If False, will only update when mouse is released, not while
        slider is dragged. Default is True.
    indexing_kwargs
        Keyword arguments matching those which would be valid for the
        `.sel` and `.isel` methods on this DataArray.

    Returns
    -------
    return value of func
    """

    if func is None:
        raise ValueError("Must provide function to apply")
    # TODO inspect func to ensure it's a valid function on a DataArray?

    indexing_widgets = wigetize_indexers(da, **indexers_kwargs)
    return widgets.interact(func, da=widgets.fixed(da), **indexing_widgets,
                            continuous_update=continuous_update)


def wigetize_indexers(da, *indexers, **indexers_kwargs):
    """
    Developer API for constructing widgets from a DataArray and its indexing
    arguments.

    Creates a slider for each dimension.

    Parameters
    ----------
    da
    indexing_kwargs

    Returns
    -------
    selection_widgets
    """

    # TODO if dim use isel, if coord use sel?

    # Apply same logic that's in `xarray.variable.isel()`
    # TODO relax indexers=None constraint by adding it as positional args?
    if indexers is not ():
        print(indexers)
        raise NotImplementedError("Currently only accepting kwarg indexers")
    indexers = either_dict_or_kwargs(None, indexers_kwargs, "isel")

    invalid = indexers.keys() - set(da.dims)
    if invalid:
        raise ValueError("dimensions %r do not exist" % invalid)

    indexing_widgets = {}
    for dim in da.dims:
        if dim in indexers:
            indexing_widgets[dim] = indexers[dim]
        else:
            indexing_widgets[dim] = widgets.fixed(slice(None))

    return indexing_widgets


def variables(*args, func=None, func_kwargs={}):
    """
    Interactively choose data variables on which to apply func.

    Each obj in args will be given a dropdown widget allowing you to
    interactively choose the variable from that object to pass in to `func`,
    e.g.

    `@interactive.variables(ds1=ds1.data_vars, ds2=ds2.data_vars)
    lambda ds1, ds2: xr.cov(ds1, ds2)`


    Parameters
    ----------
    *args : Dataset, DataArray
        Apply function to these objects
    func
        Function which accepts one or more DataArrays, to be applied
        interactively.
    func_kwargs
        Keyword arguments to pass directly to the function.

    Returns
    -------
    return value of func
    """

    if func is None:
        raise ValueError("Must provide function to apply to arguments")
    # TODO inspect func to ensure it's a valid function on DataArrays?
    # TODO check func accepts the correct number of arguments?
    # TODO check args are of the correct type

    variable_widgets = {wigetize_vars(data=obj) for obj in args}
    wrapped_func = functools.partial(func, *args, **func_kwargs)
    return widgets.interact(wrapped_func, **variable_widgets)
