"""
Defines how widgets are created.

Purpose of classes is to make overriding easier for developers of downstream
plotting and GUI libaries.
"""

import ipywidgets as ipy

import pandas as pd
import numpy as np

from xarray import DataArray


class WidgetFactory:
    def __init__(self, da, continuous_update=False):
        self.da = da
        self.continuous_update = continuous_update


class IndexerWidgetFactory(WidgetFactory):
    """
    Creates an indexing widget (e.g. a slider) from an indexer.
    """

    # TODO animations using the Play widget?
    # TODO handle dates

    def __init__(self, da, indexing_method, continuous_update=False):
        super().__init__(da, continuous_update)
        self.indexing_method = indexing_method

    def wigetize(self, indexer):
        key, selection = indexer

        if isinstance(selection, ipy.Widget):
            # Allows for users to pass in their own custom widgets
            return selection
        else:
            if self.indexing_method == 'isel':
                return self.parse_isel(key, selection)
            elif self.indexing_method == 'sel':
                return self.parse_sel(key, selection)
            else:
                raise ValueError

    # TODO if https://github.com/jupyter-widgets/ipywidgets/issues/2251 were
    # implemented then no need for continuous_update kwarg repeated every time

    def parse_isel(self, dim, selection):
        if dim not in self.da.dims:
            raise ValueError(f"{dim} not present in dimensions {self.da.dims}")

        if isinstance(selection, int):
            # TODO if int is negative
            slider = ipy.IntSlider(
                value=selection,
                min=0,
                max=self.da.sizes[dim]-1,
                step=1,
                description=f"{dim}:",
                continuous_update=self.continuous_update
            )

        elif isinstance(selection, list):
            raise NotImplementedError

        elif isinstance(selection, slice):
            # TODO deal with Nones in slices
            slider = ipy.IntRangeSlider(
                value=[selection.start, selection.stop],
                min=0,
                max=self.da.sizes[dim]-1,
                step=selection.step,
                description=f"{dim}:",
                continuous_update=self.continuous_update
            )

        elif isinstance(selection, DataArray):
            raise NotImplementedError

        else:
            raise ValueError

        return slider

    def parse_sel(self, coord_name, selection):
        coord = self.da.coords[coord_name]
        dim, *extra_dims = coord.dims
        if extra_dims:
            raise NotImplementedError("Can't handle multidimensional coords")
        index_type = self.da.coords[coord].indexer

        if isinstance(selection, float):
            slider = ipy.FloatSlider(
                value=selection,
                min=float(coord.min()),
                max=float(coord.max()),
                step=1,
                description=f"{coord_name}:",
                continuous_update=self.continuous_update
            )

        elif selection is list:
            raise NotImplementedError

        elif isinstance(selection, str):
            # TODO what if it's a date?
            slider = ipy.SelectionSlider(
                options=list(coord.values),
                value=selection,
                description=f"{coord_name}:",
                continuous_update=self.continuous_update,
            )

        elif isinstance(selection, slice):
            # TODO better ways of checking types of indexes?
            if isinstance(selection.start, str):
                slider = ipy.SelectionRangeSlider(
                    options=list(coord.values),
                    index=(selection.start, selection.stop),
                    description=f"{coord_name}:",
                )

            elif isinstance(selection.start, int):
                slider = ipy.IntRangeSlider(
                    value=[selection.start, selection.stop],
                    min=0,
                    max=self.da.sizes[dim]-1,
                    step=selection.step,
                    description=f"{coord_name}:",
                    continuous_update=self.continuous_update
                )
            else:
                raise ValueError

        elif isinstance(selection, DataArray):
            raise NotImplementedError

        else:
            raise ValueError

        return slider


class VariableWidgetFactory(WidgetFactory):
    ...


class DimensionWidgetFactory(WidgetFactory):
    ...
