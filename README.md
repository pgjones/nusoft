Nusoft package manager 
======================
A package manager for software used in particle physics experiments.

Installation
------------
Clone this repository and source the env.(c)sh file.

Requirements
------------
* Python 2.7

Usage
-----
To see the list of packages available run

    nusoft list

To install the package run

    nusoft install package_name

Documentation
-------------
Sphinx based documentation is available in the `docs` directory. To build HTML documentation,

    cd doc
    make html

Output is placed in `doc/_build/html`.

Testing
-------
To test the code is working as expected run

    python -m unittest discover nusoft/test/

