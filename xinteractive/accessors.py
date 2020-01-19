from xarray import register_dataarray_accessor, register_dataset_accessor
import xarray.plot as xplt

from . import interactions


@register_dataarray_accessor('interactive')
class InteractiveDataArrayAccessor:
    def __init__(self, da):
        self.da = da

    def apply(self, func, func_kwargs={}, continuous_update=True,
              **indexing_kwargs):
        """
        Apply any function to the DataArray, but with interactive indexing.

        Use like:

        `da.interactive.apply(np.sin, time=20, position=4.5)`

        which would apply `np.sin` to `da`, creating interactive sliders for
        time and position.

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

        return interactions.indexing(da=self.da, func=func,
                                     func_kwargs=func_kwargs,
                                     continuous_update=continuous_update,
                                     **indexing_kwargs)

    def plot(self, plotfunc=xplt.plot, plot_kwargs={}, continuous_update=True,
             **indexing_kwargs):
        """
        Plot the DataArray with interactive indexing.

        Use like:

        `da.interactive.plot(xplot.pcolormesh, time=20, position=4.5)`

        which would plot `da` using xarray's wrapping of `pcolormesh`, creating
        interactive sliders for time and position.

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

        return self.apply(func=plotfunc, func_kwargs=plot_kwargs,
                          continuous_update=continuous_update,
                          **indexing_kwargs)


@register_dataset_accessor('interactive')
class InteractiveDatasetAccessor:
    def __init__(self, ds):
        self.ds = ds

    def apply(self, func, func_kwargs={}, continuous_update=True,
              **indexing_kwargs):
        """
        Apply any function to the DataArray, but with interactive indexing.

        Use like:

        `da.interactive.apply(np.sin, time=20, position=4.5)`

        which would apply `np.sin` to `da`, creating interactive sliders for
        time and position.

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

        # TODO relies on interaction decorator chaining

        interact_indexes = interactions.indexing(
            ds=self.ds, func=func, func_kwargs=func_kwargs,
            continuous_update=continuous_update, **indexing_kwargs)

        return interactions.variables(ds, func=interact_indexes)

    def plot(self, plotfunc=xplt.plot, plot_kwargs={}, continuous_update=True,
             **indexing_kwargs):
        """
        Plot the DataArray with interactive indexing.

        Use like:

        `da.interactive.plot(xplot.pcolormesh, time=20, position=4.5)`

        which would plot `da` using xarray's wrapping of `pcolormesh`, creating
        interactive sliders for time and position.

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

        # TODO relies on interaction decorator chaining

        interact_indexes = self.apply(func=plotfunc, func_kwargs=plot_kwargs,
                                      continuous_update=continuous_update,
                                      **indexing_kwargs)

        return interactions.variables(ds, func=interact_indexes)