#!/usr/bin/env python
#
# Make, GPP, GCC, LD, Python
#
# Various command packages
#
# Author P G Jones - 2014-08-23 <p.g.jones@qmul.ac.uk> : New file.
####################################################################################################
import nusoft.package.command as command_package

class Make(command_package.CommandPackage):
    """ The make command package."""
    def __init__(self, system, repository):
        """ Initialise the make command package.

        :param system: class that manages system commands
        :type system: :class:`nusoft.system.System` instance
        :param repository: local name of the repository the package is from
        """
        super(Make, self).__init__("make", system, repository, "make")

class GPP(command_package.CommandPackage):
    """ The g++ command package."""
    def __init__(self, system, repository):
        """ Initialise the g++ command package.

        :param system: class that manages system commands
        :type system: :class:`nusoft.system.System` instance
        :param repository: local name of the repository the package is from
        """
        super(GPP, self).__init__("g++", system, repository, "g++")

class GCC(command_package.CommandPackage):
    """ The gcc command package."""
    def __init__(self, system, repository):
        """ Initialise the gcc command package.

        :param system: class that manages system commands
        :type system: :class:`nusoft.system.System` instance
        :param repository: local name of the repository the package is from
        """
        super(GCC, self).__init__("gcc", system, repository, "gcc")

class LD(command_package.CommandPackage):
    """ The ld command package."""
    def __init__(self, system, repository):
        """ Initialise the ld command package.

        :param system: class that manages system commands
        :type system: :class:`nusoft.system.System` instance
        :param repository: local name of the repository the package is from
        """
        super(LD, self).__init__("ld", system, repository, "ld")

class Python(command_package.CommandPackage):
    """ The python command package."""
    def __init__(self, system, repository):
        """ Initialise the python command package.

        :param system: class that manages system commands
        :type system: :class:`nusoft.system.System` instance
        :param repository: local name of the repository the package is from
        """
        super(Python, self).__init__("python", system, repository, "python")

# The versions of these packages
versions = [Make, GPP, GCC, LD, Python]
