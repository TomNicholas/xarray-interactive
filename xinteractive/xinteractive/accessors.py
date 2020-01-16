from xarray import register_dataarray_accessor
import xarray.plot as xplt

from ipywidgets import interact, fixed


@register_dataarray_accessor('interactive')
class InteractiveDataArrayAccessor:
    def __init__(self, da):
        self.da = da

    def apply(self, func, func_kwargs, **selection_kwargs):
        """
        Apply any function, but with interactive indexing.
        """
        raise NotImplementedError

    def plot(self, plotfunc=xplt.plot, plot_kwargs={}, continuous_update=True,
             **indexing_kwargs):
        """
        Plot with interactive indexing.

        Allows an API like:
        `da.interactive.plot(xplot.pcolormesh, time=20, position=4.5)`
        which would plot with sliders for time and position.

        Parameters
        ----------
        plotfunc, optional
            Plotting function which accepts a DataArray and displays something
            in ipython. Default is to use xarray's inbuilt general plotting
            function, i.e. `xarray.plot.plot`.
        plot_kwargs
            Keyword arguments to pass directly to the plotting function.
        continuous_update : bool, optional
            If False, will only update plot when mouse is released, not while
            slider is dragged. Default is True.
        indexing_kwargs
            Keyword arguments matching those which would be valid for the
            `.sel` and `.isel` methods on this DataArray.

        Returns
        -------
        return value of plotfunc
        """

        indexing_widgets = wigetize_indexers(data=self.da, **indexing_kwargs)
        wrapped_plotfunc = functools.partial(plotfunc, data=self.da,
                                             **plot_kwargs)
        return interact(wrapped_plotfunc, **indexing_widgets,
                        continuous_update=continuous_update)


def wigetize_indexing(da, **indexing_kwargs):
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
