#!/usr/bin/env python
#
# X11, Xpm, Xft, Xext, python-dev
#
# Various library packages
#
# Author P G Jones - 2014-08-23 <p.g.jones@qmul.ac.uk> : New file.
####################################################################################################
import nusoft.package.library as library_package

class X11(library_package.LibraryPackage):
    """ The x11 library package."""
    def __init__(self, system, repository):
        """ Initialise the x11 library package.

        :param system: class that manages system 
        :type system: :class:`nusoft.system.System` instance
        :param repository: local name of the repository the package is from
        """
        super(X11, self).__init__("x11", system, repository, libraries=["X11"], headers=["X11/Xlib.h"])

class Xpm(library_package.LibraryPackage):
    """ The xpm library package."""
    def __init__(self, system, repository):
        """ Initialise the xpm library package.

        :param system: class that manages system 
        :type system: :class:`nusoft.system.System` instance
        :param repository: local name of the repository the package is from
        """
        super(Xpm, self).__init__("xpm", system, repository, libraries=["Xpm"], headers=["X11/xpm.h"])

class Xft(library_package.LibraryPackage):
    """ The xft library package."""
    def __init__(self, system, repository):
        """ Initialise the xft library package.

        :param system: class that manages system 
        :type system: :class:`nusoft.system.System` instance
        :param repository: local name of the repository the package is from
        """
        super(Xft, self).__init__("xft", system, repository, libraries=["Xft"])

class Xext(library_package.LibraryPackage):
    """ The xext library package."""
    def __init__(self, system, repository):
        """ Initialise the xext library package.

        :param system: class that manages system 
        :type system: :class:`nusoft.system.System` instance
        :param repository: local name of the repository the package is from
        """
        super(Xext, self).__init__("xext", system, repository, libraries=["Xext"], headers=["X11/extensions/shape.h"])

class PythonDev(library_package.LibraryPackage):
    """ The python-dev library package."""
    def __init__(self, system, repository):
        """ Initialise the python-dev library package.

        :param system: class that manages system 
        :type system: :class:`nusoft.system.System` instance
        :param repository: local name of the repository the package is from
        """
        super(PythonDev, self).__init__("python-dev", system, repository, config="python-config")


# The versions of these packages
versions = [X11, Xpm, Xft, Xext, PythonDev]
