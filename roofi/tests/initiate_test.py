import os
import unittest
import shutil

from rootpy import asrootpy
from rootpy.plotting import Hist1D, Graph, Canvas
from rootpy.interactive import wait
from rootpy.io import File

from ROOT import TCanvas, TLegend, TFile, TDirectoryFile, TPad

from roofi.figure import Figure, Styles

import ROOT

test_dir = os.path.dirname(os.path.abspath(__file__))


class Test_Figure(unittest.TestCase):
    def test_initiate_figure(self):
        f = Figure()
        self.assertIsInstance(f, Figure)

    def test_add_plottable(self):
        f = Figure()
        h = Hist1D(10, 0, 10)
        f.add_plottable(h)
        # check if a deep copy was performed
        self.assertNotEqual(h, f._plottables[0])

        # add histogram with legend
        legend_labels = [pdic['legend_title'] for pdic in f._plottables if pdic['legend_title'] != '']
        self.assertEqual(len(legend_labels), 0)
        f.add_plottable(h, legend_title="cool hist")
        legend_labels = [pdic['legend_title'] for pdic in f._plottables if pdic['legend_title'] != '']
        self.assertEqual(len(legend_labels), 1)

        # no old plottables if I make a new one:
        f = Figure()
        self.assertEqual(len(f._plottables), 0)

    def test_reset_figure(self):
        f = Figure()
        h = Hist1D(10, 0, 10)
        f.add_plottable(h)
        f.delete_plottables()
        self.assertEqual(len(f._plottables), 0)


class Test_draw_to_canvas(unittest.TestCase):
    def test_draw_without_plottables(self):
        f = Figure()
        self.assertRaises(IndexError, f.draw_to_canvas)

    def test_add_graph_without_points(self):
        # Adding an empty plottable might not make a lot of sense, but it does not raise an error
        gr = Graph()
        f = Figure()
        f.add_plottable(gr)

    def test_draw_to_canvas_no_legend(self):
        f = Figure()
        h = Hist1D(10, 0, 10)
        h.Fill(5)
        f.add_plottable(h)
        c = f.draw_to_canvas()
        self.assertIsInstance(c, TCanvas)
        self.assertIsInstance(c.FindObject("plot"), TPad)

    def test_draw_to_canvas_legend(self):
        f = Figure()
        h = Hist1D(10, 0, 10)
        h.Fill(5)
        f.add_plottable(h, legend_title="some title")
        c = f.draw_to_canvas()
        self.assertIsInstance(c.FindObject("plot"), TPad)

    def test_draw_to_canvas_several_hists(self):
        f = Figure()
        h1 = Hist1D(10, 0, 10)
        h1.Fill(5)
        h2 = Hist1D(10, 0, 10)
        h2.Fill(2)
        f.add_plottable(h1, legend_title="hist 1")
        f.add_plottable(h2, legend_title="hist 1")
        c = f.draw_to_canvas()
        self.assertIsInstance(c.FindObject("plot"), TPad)

    def test_draw_to_canvas_hists_and_graphs(self):
        f = Figure()
        h1 = Hist1D(10, 0, 10)
        h1.Fill(5)
        h2 = Hist1D(10, 0, 10)
        h2.Fill(2)
        gr = Graph()
        gr.SetPoint(0, 0, 0)
        gr.SetPoint(1, 1, 1)
        gr.SetPoint(2, 7, 2)
        f.add_plottable(h1, "hist")
        f.add_plottable(gr, "graph")
        c = f.draw_to_canvas()
        self.assertIsInstance(c.FindObject("plot"), TPad)

    def test_draw_histograms_with_incompatible_binning(self):
        ROOT.gROOT.SetBatch(False)
        f = Figure()
        h1 = Hist1D(3, 0, 10)
        h1.Fill(1, 3)
        f.add_plottable(h1)
        h2 = Hist1D(7, 0, 10)
        h2.Fill(2, 7)
        f.add_plottable(h2)
        h3 = Hist1D(13, 0, 10)
        h3.Fill(5, 12)
        f.add_plottable(h3)
        c = f.draw_to_canvas()


class Test_plot_options(unittest.TestCase):
    def test_log_scales(self):
        f = Figure()
        h1 = Hist1D(10, 0, 10)
        h1.Fill(5)
        f.add_plottable(h1)
        f.plot.logx = True
        f.plot.logy = True
        c = f.draw_to_canvas()
        self.assertEqual(c.FindObject("plot").GetLogy(), 1)

    def test_axis_labels_dont_overlap(self):
        # ROOT.gROOT.SetBatch(False)
        f = Figure()
        f.xtitle = 'N_{ch}#times#eta / #phi'
        f.ytitle = '1/N_{ch}^{supscr}#pi^{#pm}/#Xi'
        h1 = Hist1D(10, 0, 10,)
        h1.Fill(5)
        f.add_plottable(h1)
        c = f.draw_to_canvas()
        # wait()

    def test_draw_half_width(self):
        ROOT.gROOT.SetBatch(False)
        f = Figure()
        f.style = Styles.Presentation_half
        f.xtitle = 'N_{ch}#times#eta / #phi'
        f.ytitle = '1/N_{ch}^{supscr}#pi^{#pm}/#Xi'
        h1 = Hist1D(10, 0, 10,)
        h1.Fill(5)
        f.add_plottable(h1)
        f.draw_to_canvas()

    def test_SetRangeUser(self):
        ROOT.gROOT.SetBatch(False)
        f = Figure()
        h1 = Hist1D(10, 0, 10)
        h1.Fill(1)
        f.add_plottable(h1)
        # f.plot.xmin = -5
        # f.plot.xmax = 15
        f.plot.ymin = -5
        f.plot.ymax = 5
        c = f.draw_to_canvas()
        plot_pad = c.FindObject("plot")
        # self.assertEqual(plot_pad.GetListOfPrimitives()[-1].GetXaxis().GetXmin(), -5)
        # self.assertEqual(plot_pad.GetListOfPrimitives()[-1].GetXaxis().GetXmax(), 5)
        self.assertEqual(plot_pad.GetListOfPrimitives()[-1].GetMinimum(), -5)
        self.assertEqual(plot_pad.GetListOfPrimitives()[-1].GetMaximum(), 5)



class Test_legend_options(unittest.TestCase):
    def setUp(self):
        self.f = Figure()
        h1 = Hist1D(10, 0, 10)
        h1.Fill(5)
        h2 = Hist1D(10, 0, 10)
        h2.Fill(2)
        self.f.add_plottable(h1, legend_title="hist 1")
        self.f.add_plottable(h2, legend_title="hist 1")

    def test_legend_postion(self):
        self.f.legend.position = 'tl'
        c = self.f.draw_to_canvas()
        leg = next(obj for obj in c.FindObject("plot").GetListOfPrimitives() if isinstance(obj, TLegend))
        self.assertGreater(leg.y1, .5)

        self.f.legend.position = 'bl'
        c = self.f.draw_to_canvas()
        leg = next(obj for obj in c.FindObject("plot").GetListOfPrimitives() if isinstance(obj, TLegend))
        self.assertLess(leg.y1, .5)

        self.f.legend.position = 'tr'
        c = self.f.draw_to_canvas()
        leg = next(obj for obj in c.FindObject("plot").GetListOfPrimitives() if isinstance(obj, TLegend))
        self.assertGreater(leg.x1, .5)
        self.assertGreater(leg.y1, .5)

        self.f.legend.position = 'br'
        c = self.f.draw_to_canvas()
        leg = next(obj for obj in c.FindObject("plot").GetListOfPrimitives() if isinstance(obj, TLegend))
        self.assertGreater(leg.x1, .5)
        self.assertLess(leg.y1, .5)
        self.assertIsInstance(c.FindObject("plot"), TPad)

        self.f.legend.position = 'seperate'
        c = self.f.draw_to_canvas()
        pad = c.FindObject("legend")
        self.assertIsInstance(pad, ROOT.TPad)


class Test_write_to_root_file(unittest.TestCase):
    def setUp(self):
        self.fig = Figure()
        h1 = Hist1D(10, 0, 10)
        h1.Fill(5)
        self.fig.add_plottable(h1, legend_title="hist 1")

    @unittest.skip(True)
    def test_write_to_TFile(self):
        f = TFile(test_dir + "/test.root", "recreate")
        f = self.fig.save_to_root_file(f, 'myname')
        # Close might raise an error here!
        f.Close()

    def test_write_to_root_file(self):
        f = File(test_dir + "/test.root", "recreate")
        f = self.fig.save_to_root_file(f, 'myname')
        f.close()
        f = TFile(test_dir + "/test.root", "read")
        self.assertIsInstance(f.Get("myname"), TCanvas)

    def test_write_to_root_file_with_path(self):
        f = File(test_dir + "/test.root", "recreate")
        f = self.fig.save_to_root_file(f, 'myname', path='folder/')
        f.Close()
        f = TFile(test_dir + "/test.root", "read")
        self.assertIsInstance(f.Get("folder"), TDirectoryFile)
        self.assertIsInstance(f.Get("folder").Get("myname"), TCanvas)


class Test_write_to_pdf_file(unittest.TestCase):
    def setUp(self):
        self.fig = Figure()
        h1 = Hist1D(10, 0, 10)
        h1.Fill(5)
        self.fig.add_plottable(h1, legend_title="hist 1")

    def test_write_to_disc_with_folders(self):
        # first, delete old verion of that folder
        path = os.path.dirname(os.path.realpath(__file__)) + '/fig_folder'
        try:
            shutil.rmtree(path)
        except OSError:  # no previous file found
            pass
        name = "myfig.pdf"
        self.fig.save_to_file(name=name, path=path)
        self.assertTrue(os.path.exists(path))
        self.assertTrue(os.path.exists(path + '/' + name))

    def test_write_to_disc_without_folder(self):
        name = "myfig.pdf"
        # path = os.path.dirname(os.path.realpath(__file__))
        # first, delete old verion of that folder
        try:
            os.remove(name)
        except OSError:  # no previous file found
            pass
        self.fig.save_to_file(name=name, path='./')
        self.assertTrue(os.path.exists('./' + name))


class Test_Size_of_figures_corresponds_to_latex(unittest.TestCase):
    def setUp(self):
        self.fig = Figure()
        self.fig.ytitle = "dN_{test}/d#eta"
        self.fig.xtitle = "#psi (arb. unit)"
        h1 = Hist1D(10, 0, 10)
        h1.Fill(5)
        self.fig.add_plottable(h1, legend_title="hist 1")
        self.path = os.path.dirname(os.path.realpath(__file__)) + '/test_styles'
        shutil.rmtree(self.path, ignore_errors=True)

    @unittest.skip("Somehow, I cannot get the current page size...")
    def test_gStyle_is_unaltered(self):
        paper_width_init, paper_height_init = ROOT.Double(), ROOT.Double
        ROOT.gStyle.GetPaperSize(paper_width_init, paper_height_init)
        self.fig.save_to_file(name="fig_pres_full.pdf", path=self.path)
        paper_width_final, paper_height_final = ROOT.Double(), ROOT.Double
        ROOT.gStyle.GetPaperSize(paper_width_final, paper_height_final)
        self.assertEqual(paper_width_init, paper_width_final)
        self.assertEqual(paper_height_init, paper_height_final)

    def test_create_figures_of_different_size(self):
        self.fig.style = Styles.Presentation_full
        self.fig.save_to_file(name="fig_pres_full.pdf", path=self.path)

        self.fig.style = Styles.Presentation_half
        self.fig.save_to_file(name="fig_pres_half.pdf", path=self.path)

        self.fig.style = Styles.Public_full
        self.fig.save_to_file(name="fig_pub_full.pdf", path=self.path)

        # make a figure with exponential on y axis to see if it fits in the margin
        fig_exp = Figure()
        fig_exp.style = Styles.Presentation_half
        fig_exp.ytitle = "dN_{test}/d#eta"
        fig_exp.xtitle = "#psi (arb. unit)"
        h1 = Hist1D(10, 0, 10)
        h1.Fill(5, 0.0000000001)
        fig_exp.add_plottable(h1, legend_title="hist exp")
        fig_exp.save_to_file(name='fig_pres_half_exp.pdf', path=self.path)

        # make a pdf
        import subprocess
        test_dir = os.path.dirname(os.path.realpath(__file__))
        tex_file = './beamer.tex'
        try:
            latex_out = subprocess.check_output(
                ['pdflatex', '-file-line-error', '-interaction=nonstopmode', format(tex_file)], cwd=test_dir)
        except subprocess.CalledProcessError, e:
            print e.output
            raise e


class Test_write_to_tex_file(unittest.TestCase):
    def setUp(self):
        self.fig = Figure()
        h1 = Hist1D(10, 0, 10)
        h1.Fill(5)
        self.fig.add_plottable(h1, legend_title="hist 1")

    def test_write_to_disc_with_folders(self):
        # first, delete old verion of that folder
        path = os.path.dirname(os.path.realpath(__file__)) + '/fig_folder'
        try:
            shutil.rmtree(path)
        except OSError:  # no previous file found
            pass
        name = "myfig.pdf"
        cv = self.fig.draw_to_canvas()
        self.fig.save_to_file(name=name, path=path)
        self.assertTrue(os.path.exists(path))
        self.assertTrue(os.path.exists(path + '/' + name))


class Test_import_from_canvas(unittest.TestCase):
    def setUp(self):
        fig = Figure()
        h1 = Hist1D(10, 0, 10)
        h1.Fill(5)
        fig.add_plottable(h1, legend_title="hist 1")
        self.canvas = fig.draw_to_canvas()

    def test_import_roofi_canvas(self):
        fig = Figure()
        fig.import_plottables_from_canvas(self.canvas)
        self.assertEqual(len(fig._plottables), 1)
        self.assertIsInstance(fig._plottables[0], dict)
        fig.draw_to_canvas()

    def test_import_non_roofi_canvas(self):
        fig = Figure()
        c = Canvas()
        self.assertRaises(ValueError, fig.import_plottables_from_canvas, c)
