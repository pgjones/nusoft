#!/usr/bin/env python
#
# Package class
#
# Base class for all packages
#
# Author P G Jones - 2014-02-08 <p.g.jones@qmul.ac.uk> : First revision
####################################################################################################

class Package(object):
    """ Base class for all packages.

    :param _name: the package name
    :param _system: the system used to install packages
    :param _install_path: the installation path of this package
    :param _installed: True when the state has been checked and the package is installed
    :param _dependencies: dict of name keyed dependency packages
    :param _repository: Local name of repository this package belongs to
    """
    def __init__(self, name, system, repository):
        """ Construct the package with a *name* and the *system* installation information.
        
        :param string name: name of this package.
        :param system: class that manages system commands
        :type system: :class:`nusoft.system.System` instance
        :param repository: local name of the repository the package is from
        """
        self._name = name
        self._system = system
        self._repository = repository
        self._install_path = None
        self._installed = False
        self._dependencies = {}
    def get_name(self):
        """ Return the package name.
        
        :return: string name of the package
        """
        return self._name
    def get_repository(self):
        """ Return the repository name.
        
        :return: local name of the repository this package is part of
        """
        return self._repository
    def set_dependencies(self, dependencies):
        """ Set the dependencies for this package.

        :param dependencies: dict of name keyed dependency packages
        """
        self._dependencies = dependencies
####################################################################################################
    # Functions to override by subclasses
    def get_dependencies(self):
        """ Return a list of dependency names

        :return: list of dependency package names
        :rtype: list
        """
        return []
    def is_installed(self):
        """ Check and return if package is installed.

        :retruns: True if installed, False if not
        :rtype: bool
        """
        return self._installed
    def get_install_path(self):
        """ Return a the package installation path.
        
        :return: the installation path
        :rtype: string
        """
        return self._install_path
    def check_state(self):
        """ Function to force the package to check what it's status is."""
        pass
    def install(self):
        """ Function to install the package, raises exception unless implemented."""
        raise
    def update(self):
        """ Function to update installed package, raises exception unless implmented."""
        raise
    def remove(self):
        """ Function to remove installed package, raises exception unless implmented."""
        raise
