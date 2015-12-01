from setuptools import setup

install_requires = ['ROOT', 'rootpy']
tests_require = ['nose']

setup(
    name='roofie',
    version='0.0.1',
    description="Convinient way to make simple and good looking plots with root",
    author='Christian Bourjau',
    author_email='christian.bourjau@cern.ch',
    packages=['roofie', 'roofie.tests'],
    long_description=open('README.rst').read(),
    url='https://github.com/cbourjau/roofie',
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
    install_requires=install_requires,
    extras_require={'test': tests_require},
    test_suite='nose.collector',
)
