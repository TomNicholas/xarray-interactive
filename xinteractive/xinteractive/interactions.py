from ipywidgets import interact, fixed


def indexing(da, func, func_kwargs={}, continuous_update=True,
             **indexing_kwargs):
    """
    Apply any function to the DataArray, but with interactive indexing.

    Use in the same way as ipyywidgets.interact, i.e. as a function

    `interactive.indexing(f=lambda da: np.sin(da), time=20, position=4.5)

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

    indexing_widgets = wigetize_indexers(data=self.da, **indexing_kwargs)
    wrapped_plotfunc = functools.partial(func, data=self.da, **func_kwargs)
    return interact(wrapped_func, **indexing_widgets,
                    continuous_update=continuous_update)


def wigetize_indexers(da, **indexing_kwargs):
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
    dims = list(da.dims.keys())
    coords = list(da.coords.keys())
    dim_coords = [dim for dim in dims if dim in coords]

    selection_widgets = {}
    for dim in dims:
        dim_widget = _create_dim_widget(dim, **indexing_kwargs)
        selection_widgets[dim] = dim_widget

    return selection_widgets
