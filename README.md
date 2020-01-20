Repo for working ideas on making [xarray](https://github.com/pydata/xarray) interactive through [ipython
widgets](https://towardsdatascience.com/interactive-controls-for-jupyter-notebooks-f5c94829aee6).

## Proposal: xarray.interactive module

I've only just discovered the power of using ipython widgets in jupyter,
and I think xarray could leverage this to make lots of common data
analysis tasks more interactive and intuitive.

For example, imagine being in a jupyter environment, entering
```python
da.interactive.plot(time='2013-01-01T06:00:00')
```
and getting this plot with time slider (example from [holoviews]()), but interactive, and with N different sliders for exploring an N-dimensional `xarray.DataArray`

![hvplot example](https://github.com/TomNicholas/xarray-interactive/raw/master/images/hvplot_example.png "Title")

### Aims

To eventually implement all of the API shown in the [examples](https://github.com/TomNicholas/xarray-interactive/raw/master/examples.ipynb)


### Useful links

- [Quick intro to the power of interactivity with ipython widgets in jupyter environments](https://towardsdatascience.com/interactive-controls-for-jupyter-notebooks-f5c94829aee6)
- [Introduction to ipywidgets `interact()` function, which we want to emulate.](https://ipywidgets.readthedocs.io/en/latest/examples/Using%20Interact.html)
- [Making interact ignore arguments](https://github.com/jupyter-widgets/ipywidgets/issues/2740)
