### Difficulties with method chaining

Arbitraily long method chaining would be great, i.e.
```python
da.interactive.isel(time=10).mean('time').plot()
```
but I think it will be considerably more complicated.

The problem is that the way the `ipywidgets.interactive()` function works means that each time a widget value is altered (e.g. a slider dragged to a new position), then the function wrapped by `interactive` must be recomputed.
For single functions that's fine, but for method chaining it means the final `.plot()` method has to know about all the previous methods back up to the `.interactive` input.

I've found a way to get around this, but I'd like some feedback on the approach because it might be needlessly complicated.

I would like to do it by subclassing to create an `InteractiveDataArray`, which you could create with an `interactive` accessor method like
```python
ida = da.interactive.isel(time=10)
```
This class would store the widgets and decorate it's inherited methods to either propagate them (e.g. through `ida.reduce()`) or display them (e.g. after `ida.plot()`).
It would define the [`_ipython_display_()`](https://ipython.readthedocs.io/en/stable/config/integrating.html#rich-display) method so that calling `display(ida)` revealed the widgets.

To allow for the final method to recompute all the previous steps, each inherited computation method would be wrapped by a decorator which records the function used and it's arguments.
That way the final method (which really you know will either be `.plot()`, or `__print__()`) can revaluate it's whole history when the slider tells it to recompute.

I've got a very rough example of this working, but as I said there might be a much easier way...

![method_chaining](https://user-images.githubusercontent.com/35968931/72756538-6d812e00-3bc5-11ea-8330-929673af5f47.gif)

