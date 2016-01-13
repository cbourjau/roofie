"""
A class mirroring a subset of the Latex beamer functinality.

It is intended as an easy way to compile many roofie figures with small annotations into a valid tex document.
At the same time, it tries to abstract earthly problems like uniqueness of the filenames of the plots.
This is at the expense of customizability of the folder structure
"""

import os
import random
import re
import string
import subprocess
import textwrap


class Beamerdoc(object):
    def __init__(self):
        self.title = ''
        self.author = ''
        self.sections = []
        self.output_dir = './summary_slides/'
        self.preamble = textwrap.dedent(r"""
        \documentclass[xcolor=dvipsnames]{{beamer}}

        \usepackage{{graphicx,subfigure,url, tikz}}

        % example themes
        \usetheme[nat,style=simple]{{Frederiksberg}}

        % put page numbers
        \setbeamertemplate{{footline}}[frame number]{{}}
        % remove navigation symbols
        \setbeamertemplate{{navigation symbols}}{{}}
        \author{{{author}}}
        \institute[NBI, Copenhagen]{{Niels Bohr Institute, Copenhagen\\HMTF MC benchmark studies\\Supervisor: Michele Floris}}

        \title{{{title}}}
        \begin{{document}}

        \frame[plain]{{\titlepage}}
        \frame[plain]{\tableofcontents}

        """)
        self.postamble = r"""\end{document}\n"""

    class Section(object):
        def __init__(self, document, sec_title):
            self.document = document
            self.title = sec_title
            self.figures = []
            self.frames = []
            self.frame_template = textwrap.dedent(r"""
            \begin{{frame}}[plain]
            \frametitle{{{title}}}
            \begin{{columns}}
            \begin{{column}}{{.45\textwidth}}
            {}\\
            {}
            \end{{column}}
            \begin{{column}}{{.45\textwidth}}
            {}\\
            {}
            \end{{column}}
            \end{{columns}}
            \end{{frame}}

            """)

        def add_figure(self, fig):
            self.figures.append(fig)

        def _make_section_body(self):
            """
            Convert this section to latex. This writes the figures to disc

            Returns
            -------
            string :
                Latex code for this section with linkes to the figures already included
            """
            fig_paths = self._write_figures_to_disc()
            section_body = '\section*{{{}}}'.format(self.title)
            figs_per_frame = 4
            for frame_num in xrange(0, len(fig_paths), figs_per_frame):
                ig_cmds = ['' for i in range(figs_per_frame)]
                for fig_num_frame, path in enumerate(fig_paths[frame_num:(frame_num + figs_per_frame)]):
                    ig_cmds[fig_num_frame] = format(r'\includegraphics[width=\textwidth]{{{}}}'.format(path))
                section_body += self.frame_template.format(title=self.title, *ig_cmds)
            return section_body

        def _write_figures_to_disc(self):
            """
            Write the figures of this section to disc.

            Returns
            -------
            list :
                Paths to the files written to disc, relative to where the tex file will be
            """
            paths = []
            # make a save folder name out of the section title
            t = re.compile("[a-zA-Z0-9.,_-]")
            fig_folder_safe = 'figures/' + "".join([ch for ch in self.title if t.match(ch)]) + "/"
            for fig in self.figures:
                rand_name = ''.join(random.choice(string.ascii_letters) for _ in range(5)) + ".pdf"
                fig.save_to_file(self.document.output_dir + fig_folder_safe, rand_name)
                paths.append("./" + fig_folder_safe + rand_name)
            return paths

    def add_section(self, sec_title):
        self.sections.append(self.Section(self, sec_title=sec_title))
        return self.sections[-1]

    def _create_latex_and_save_figures(self):
        body = ''
        body += self.preamble.format(title=self.title, author=self.author)
        for sec in self.sections:
            body += sec._make_section_body()
        body += self.postamble
        return body

    def finalize_document(self):
        """
        Assamble the latex document and run the compile command
        """
        output_file_name = "summary.tex"
        try:
            os.makedirs(self.output_dir)
        except OSError:
            pass

        with file(os.path.abspath(self.output_dir) + "/" + output_file_name, 'w')as f:
            f.write(self._create_latex_and_save_figures())

        cmd = ['pdflatex', '-file-line-error', '-interaction=nonstopmode', format(output_file_name)]
        try:
            out = subprocess.check_output(cmd, cwd=os.path.abspath(self.output_dir))
            out = subprocess.check_output(cmd, cwd=os.path.abspath(self.output_dir))
        except subprocess.CalledProcessError:
            print "An error occured while compiling the latex document. See 'summary.log' for details"

# from roofie.figure import Figure
# from rootpy.plotting import Hist1D
# f = Figure()
# h = Hist1D(10, 0, 10)
# h.fill(5)
# f.add_plottable(h)
# latexdoc = Beamerdoc()
# latexdoc.author = "Christian Bourjau"
# latexdoc.title = "Test"
# sec = latexdoc.add_section("My section")
# sec.add_figure(f)
# latexdoc.finalize_document()
