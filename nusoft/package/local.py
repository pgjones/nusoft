#!/usr/bin/env python
#
# LocalPackage class
#
# These packages are installed to the target folder.
#
# Author P G Jones - 2014-02-14 <p.g.jones@qmul.ac.uk> : First revision
####################################################################################################
import package
import os
import logging
logger = logging.getLogger(__name__)

class LocalPackage(package.Package):
    """ Base class for packages that can be installed to the target folder. 

    :param _updated: True if the package has been updated in the current session.
    """
    def __init__(self, name, system, repository):
        """ Construct the package with a *name* and the *system* installation information.
        
        :param string name: name of this package.
        :param system: class that manages system commands
        :type system: :class:`nusoft.system.System` instance
        :param repository: local name of the repository the package is from
        """
        super(LocalPackage, self).__init__(name, system, repository)
        self._install_path = os.path.join(system.get_install_path(), self._name)
        self._updated = False
    def check_state(self):
        """ Function to force the package to check what it's status is."""
        if self._is_installed():
            self._installed = True
        else:
            self._installed = False
            self._updated = False
    def install(self):
        """ Function to install the package.

        Will check if already installed first.
        """
        logger.info("Installing %s to %s" % (self._name, self._install_path))
        if not self._installed:
            self._download()
            self._install()
            self.check_state()
    def update(self):
        """ Function to update installed package.

        Will check if already updated first.
        """
        logger.info("Updating %s in %s" % (self._name, self._install_path))
        if not self._installed:
            raise
        elif self._installed and not self._updated:
            self._update()
            self._updated = True
            self.check_state()
    def remove(self):
        """ Function to remove installed package
        
        Will check if installed first.
        """
        logger.info("Removing %s from %s" % (self._name, self._install_path))
        if not self._installed:
            raise
        else:
            self._remove()
            self.check_state()
####################################################################################################
    # Functions to override by subclasses
    def _download(self):
        
        pass
    def _install(self):

        pass
    def _update(self):

        pass
    def _remove(self):
        
        pass
