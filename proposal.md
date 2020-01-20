## Proposal: `xarray.interactive` module

I've been experimenting with [ipython widgets](https://github.com/jupyter-widgets/ipywidgets) in jupyter notebooks, and I've been [working on](https://github.com/TomNicholas/xarray-interactive) how we might use them to make xarray more interactive.

### Motivation:

For most users who are exploring their data, it will be common to find themselves rerunning the same cells repeatedly but with slightly different values.
In `xarray`'s case that will often be in an `.isel()` or `.sel()` call, or selecting variables from a dataset.
IPython widgets allow you to interact with your functions in a very intuitive way, which we could exploit.
There are lots of tutorials on how to interact with `pandas` data (e.g. [this great one](https://towardsdatascience.com/interactive-controls-for-jupyter-notebooks-f5c94829aee6)), but I haven't seen any for interacting with `xarray` objects.


### Relationship to other libraries:

Some downstream plotting libaries (such as @hvplot) [already use widgets](https://hvplot.holoviz.org/user_guide/Gridded_Data.html) when interactively plotting xarray-derived data structures, but they don't seem to go the full N dimensions.
This also isn't something that should be confined to plotting functions - you often choose slices or variables at the start of analysis, not just at the end.
I'll come back to this idea later.

The default ipython widgets are pretty good, but we could write an `xarray.interactive` module in such a way that downstream developers can easily replace them with [their own widgets](https://hvplot.holoviz.org/user_guide/Widgets.html).

### Usage examples:

```python
# imports
import ipywidgets as widgets
import xarray.plot as xplot
import xarray.interactive as interactive

# Load tutorial data
ds = xr.tutorial.open_dataset('air_temperature')['air']
```

Plotting against multiple dimensions interactively
```python
interactive.isel(da, xplot.plot, lat=10, lon=50)
```

Interactively select a range from a dimension
```python
def plot_mean_over_time(da):
    da.mean(dim=time)
interactive.isel(da, plot_mean_over_time, time=slice(100, 500))
```

Animate over one dimension
from ipywidgets import Play
interactive.isel(da, xplot.plot, time=Play())


### API ideas:

We can write a function like this

```python
interactive.isel(da, func=xplot.plot, time=10)
```

which could also be used as a decorator something like this
```python
@interactive.isel(da, time=10)
def plot(da)
    return xplot.plot(da)
```

It would be nicer to be able to do this
```python
@Interactive(da).isel(time=10)
def plot(da)
    return xplot.plot(da)
```
but [Guido forbade it](https://seriously.dontusethiscode.com/2013/04/21/lambda-decorators.html).

But we can attach these functions to an accessor to get
```python
da.interactive.isel(xplot.plot, time=10)
```

### Other ideas

Select variables from datasets
```python
@interactive.data_vars(da1=ds['n'], da2=ds['T'], ...)
def correlation(da1, da2, ...)
    ...

# Would produce a dropdown list of variables for each dataset
```

Choose dimensions to apply functions over
```python
@interactive.dims(dim='time')
def mean(da, dim)
    ...
    
# Would produce a dropdown list of dimensions in the dataarray
```

General `interactive.explore()` method to see variation over any number of dimensions, the default being all of them.


### Difficulties with method chaining

Method chaining would be great
```python
da.interactive.isel(time=10).plot()
```
but I've found it to be much more difficult.

I would like to do it by subclassing to create an `InteractiveDataArray`, which you could create with an `interactive` accessor method like
```python
ida = da.interactive.isel(time=10)
```
This class would store the upstream widgets and decorate it's inherited methods to either propagate the widgets (e.g. through `ida.reduce()`) or display them (e.g. after `ida.plot()`).
It would define the [`_ipython_display_()`](https://ipython.readthedocs.io/en/stable/config/integrating.html#rich-display) method so that calling `display(ida)` revealed the widgets.

But method chaining brings additional problems because you have to have a return value...


