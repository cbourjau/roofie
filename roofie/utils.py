import ROOT


def _turn_on_style():
    """
    Would be nice to scope this style, but root is very wonky in this regard...
    """
    # self._previous_style = ROOT.gStyle.Clone('previous_style')
    ROOT.gStyle.Reset("Plain")
    ROOT.gStyle.SetOptTitle(0)
    ROOT.gStyle.SetOptStat(0)
    ROOT.gStyle.SetPalette(1)
    ROOT.gStyle.SetCanvasColor(10)
    ROOT.gStyle.SetCanvasBorderMode(0)
    ROOT.gStyle.SetFrameLineWidth(1)
    ROOT.gStyle.SetTextFont(43)
    ROOT.gStyle.SetLegendBorderSize(0)
    ROOT.gStyle.SetLegendFont(43)
