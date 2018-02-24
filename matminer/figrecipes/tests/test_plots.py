"""
PlotlyFig testing. Most tests are run by comparing generated Plotly figures
with pre-generated json files. Some are just ensuring Plotly does not throw
errors.
"""

__author__ = "Alex Dunn <ardunn@lbl.gov>"

import unittest
import json
import numpy as np
import pandas as pd
from pymatgen.util.testing import PymatgenTest
from matminer.figrecipes.plot import PlotlyFig


a = [1.6, 2.1, 3]
b = [1, 4.2, 9]
c = [14, 15, 17]
xlabels = ['low', 'med', 'high']
ylabels = ['worst', 'mediocre', 'best']

def refresh(open_plots=False):
    """
    For developer use. Refresh the json files and open plots to see if they
    look good. Use this function to set the current PlotlyFig build outputs
    as the true values of the tests.

    Args:
        open_plots (bool): If True, opens all plots generated. Useful if you
            want to check the current build outputs to make sure they look good.
            If False, just generates the json files and quits.
    """

    pf = PlotlyFig()
    xys = pf.xy([(a, b)], return_plot=True)
    xym = pf.xy([(a, b), (b, a)], return_plot=True)
    hmb = pf.heatmap_basic([a, b, c], xlabels, ylabels, return_plot=True)
    his = pf.histogram(a + b + c, n_bins=5, return_plot=True)
    bar = pf.bar(x=a, y=b, labels=xlabels, return_plot=True)
    pcp = pf.parallel_coordinates([a, b], cols=xlabels, return_plot=True)

    # Layout is compared for the plots which always convert to dataframes,
    # as dataframes are not easily encoded by json.dump
    vio = pf.violin([a, b, c, b, a, c, b], cols=xlabels, return_plot=True)
    scm = pf.scatter_matrix([a, b, c], return_plot=True)

    fnamedict = {"xys": xys, "xym": xym, "hmb": hmb, "his": his, "bar": bar,
                 "pcp": pcp, "vio": vio, "scm": scm}

    for fname, obj in fnamedict.items():
        if obj in [vio, scm]:
            obj = obj['layout']
        json.dump(obj, open("template_{}.json".format(fname), "w"))

    if open_plots:
        for obj in fnamedict.values():
            pf.create_plot(obj, return_plot=False)



class PlotlyFigTest(PymatgenTest):
    def setUp(self):
        self.pf = PlotlyFig()

    def test_xy(self):
        # Single trace
        xys_test = self.pf.xy([(a, b)], return_plot=True)
        xys_true = json.load(open("template_xys.json", "r"))
        self.assertTrue(xys_test == xys_true)

        # Multi trace
        xym_test = self.pf.xy([(a, b), (b, a)], return_plot=True)
        xym_true = json.load(open("template_xym.json", "r"))
        self.assertTrue(xym_test == xym_true)
#
    def test_heatmap_basic(self):
        hmb_test = self.pf.heatmap_basic([a, b, c], xlabels, ylabels, return_plot=True)
        hmb_true = json.load(open("template_hmb.json", "r"))
        self.assertTrue(hmb_test == hmb_true)

    def test_histogram(self):
        his_test = self.pf.histogram(a + b + c, n_bins=5, return_plot=True)
        his_true = json.load(open("template_his.json", "r"))
        self.assertTrue(his_test == his_true)

    def test_bar(self):
        bar_test = self.pf.bar(x=a, y=b, labels=xlabels, return_plot=True)
        bar_true = json.load(open("template_bar.json", "r"))
        self.assertTrue(bar_test == bar_true)

    def test_parallel_coordinates(self):
        pcp_test = self.pf.parallel_coordinates([a, b], cols=xlabels, return_plot=True)
        pcp_true = json.load(open("template_pcp.json", "r"))
        self.assertTrue(pcp_test == pcp_true)

    def test_violin(self):
        vio_test = self.pf.violin([a, b, c, b, a, c, b], cols=xlabels,return_plot=True)['layout']
        vio_true = json.load(open("template_vio.json", "r"))
        self.assertTrue(vio_test == vio_true)

    def test_scatter_matrix(self):
        scm_test = self.pf.scatter_matrix([a, b, c], return_plot=True)['layout']
        scm_true = json.load(open("template_scm.json"))
        self.assertTrue(scm_test == scm_true)

    def test_heatmap_df(self):
        a = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        b = [2, 4, 6, 8, 10, 2, 4, 6, 8, 10]
        c = [10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
        df = pd.DataFrame(data=np.asarray([a, b, c]).T, columns=['a', 'b', 'c'])
        x_labels = ['low', 'high']
        y_labels = ['small', 'large']
        self.pf.heatmap_df(df, x_labels=x_labels, y_labels=y_labels,
                           return_plot=True)

if __name__ == "__main__":

    # refresh(open_plots=True)
    unittest.main()