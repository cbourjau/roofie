from ROOT import TF1
from rootpy.plotting import Hist1D, Graph
from roofie import Figure, Styles

# Define the visuals of the figure:
fig = Figure()
fig.style = Styles.Public_full
# Drawing the legend currently still screws up the y scale! :P
# This is why we love root...
fig.legend.title = "A legend title"
fig.legend.position = 'tl'  # top left
fig.xtitle = "Important X"
fig.ytitle = "More important Y"

# You can also pick a color palette.  The choices are "root", "set2",
# "husl", and "colorblind"
fig.plot.palette = "colorblind"

# Define the "plottables" and add them to the figure
f = TF1("f", "1000*exp(-0.5*((x)/2)**2)", -5, 5)
g = Graph()
g.SetPoint(0, 0, 100)
g.SetPoint(1, 1, 200)
g.SetPoint(2, 2, 200)
fig.add_plottable(g, legend_title="A Graph")
fig.add_plottable(f, legend_title='A Gaussian')

# add_plottable makes a deep copy of the passed object so you can do whatever you want after its "commited" to the figure.
# ie. overwrite a histogram in a loop:
fig.add_plottable(None, legend_title="Many Landaus:")
for i in range(1, 5):
    h = Hist1D(30, -5, 5)
    h.FillRandom('landau', 10000 * i)
    fig.add_plottable(h, legend_title="Landau {}".format(i), markerstyle='diamond')


fig.save_to_file(path=".", name="busy_plot.pdf")
