from setuptools import setup

setup(
    name='roofi',
    version='0.1',
    description="Convinient way to make simple plots with root",
    author='Christian Bourjau',
    author_email='c.bourjau@posteo.de',
    packages=['roofi', 'roofi.tests'],
    long_description=open('README.rst').read(),
    # url='https://github.com/chrisboo/roofi',
    # download_url='https://github.com/chrisboo/pyhistogram/tarball/0.1',
    keywords=['root', 'rootpy', 'plotting'],
    classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.7",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering :: Mathematics",
        "Topic :: Scientific/Engineering :: Physics",
        "Development Status :: 3 - Alpha",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    install_requires=[],
    extras_require={},
    test_suite='roofi.tests',
)
