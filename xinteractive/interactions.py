import ipywidgets as ipy

from xarray.core.utils import either_dict_or_kwargs

from .widget_factories import IndexerWidgetFactory


def isel(da, func, indexers=None, func_kwargs={}, continuous_update=False,
         **indexers_kwargs):
    """
    Interactively choose indexes of a DataArray on which to apply func.

    Use in the same way as ipyywidgets.interact, i.e. as a function

    `interactive.isel(f=lambda da: np.sin(da), time=20, position=4.5)`

    or as a decorator

    `@interactive.isel(time=20, position=4.5)
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
        If True, will update while slider is dragged, rather than only when
        mouse is released. Default is False.
    indexing_kwargs
        Keyword arguments matching those which would be valid for the `.isel`
        method on this DataArray.

    Returns
    -------
    return value of func
    """

    if func is None:
        raise ValueError("Must provide function to apply")
    # TODO inspect func to ensure it's a valid function on a DataArray?

    if indexers:
        raise NotImplementedError
    indexers = either_dict_or_kwargs(indexers, indexers_kwargs, "isel")

    invalid = indexers.keys() - set(da.dims)
    if invalid:
        raise ValueError("dimensions %r do not exist" % invalid)

    factory = IndexerWidgetFactory(da, 'isel',
                                   continuous_update=continuous_update)

    indexing_widgets = {}
    fixed_indexers = {}
    for dim in da.dims:
        if dim in indexers:
            indexer = (dim, indexers[dim])  # TODO neater way
            indexing_widgets[dim] = factory.wigetize(indexer)
        else:
            fixed_indexers[dim] = slice(None)

    # Use closure to bypass interrogation of all args by ipywidgets.interactive
    # (see https://github.com/jupyter-widgets/ipywidgets/issues/2740)
    def _isel_then_func_with_fixed_args(**indexing_widgets):

        # Some widgets must be converted back to xarray-compatible inputs
        # TODO instead make special slider subclasses?
        for dim, indexer in indexing_widgets.items():
            if isinstance(indexer, tuple):
                indexing_widgets[dim] = slice(*indexer)

        interactive_slice = da.isel(**fixed_indexers, **indexing_widgets)
        return func(interactive_slice, **func_kwargs)

    return ipy.interactive(_isel_then_func_with_fixed_args, **indexing_widgets)


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
