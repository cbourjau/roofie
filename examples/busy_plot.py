from ROOT import TF1
from rootpy.plotting import Hist1D
from roofie import Figure, Styles

h = Hist1D(30, -5, 5)
h.FillRandom('landau', 1000)

f = TF1("f", "100*exp(-0.5*((x)/2)**2)", -5, 5)

fig = Figure()
fig.style = Styles.Public_full
# Drawing the legend currently still screws up the y scale! :P
# This is why we love root...
fig.legend.title = "Functions"
fig.legend.position = 'tr'  # top right
fig.xtitle = "Mega X"
fig.ytitle = "Tera Y"

fig.add_plottable(h, legend_title="Landau")
fig.add_plottable(f, legend_title='Gaussian')
fig.save_to_file(path=".", name="busy_plot.pdf")
