#!/usr/bin/env python
#
# CLHEP
#
# CLHEP packages and versions
#
# Author P G Jones - 2014-08-20 <p.g.jones@qmul.ac.uk> : New file.
####################################################################################################
import nusoft.package.local as local_package
import os

class Clhep(local_package.LocalPackage):
    """ The Clhep installation package.
    
    :param _tar_name: name of the tar file to download/install
    :param _version: version of Clhep to install.
    """
    def __init__(self, system, repository):
        """ Initialise this clhep installation package.

        :param system: class that manages system commands
        :type system: :class:`nusoft.system.System` instance
        :param repository: local name of the repository the package is from
        """
        super(Clhep, self).__init__(self._version, system, repository)
        self._tar_name = self._version + ".tgz"
    def get_dependencies(self):
        """ Return a list of dependency names

        :returns: list of dependency package names
        :rtype: list
        """
        return ["make", "g++", "gcc"]
    def _download(self):
        """ Download the clhep tar file."""
        self._system.download("http://proj-clhep.web.cern.ch/proj-clhep/DISTRIBUTION/tarFiles/" + self._tar_name)
    def _install(self):
        """ Untar the tar file to the install path."""
        self._system.untar(self._tar_name, self.get_install_path(), 2)
        self._system.configure(args=['--prefix=%s' % self.get_install_path()], cwd=self.get_install_path())
        self._system.make(cwd=self.get_install_path())
        self._system.make(args=["install"], cwd=self.get_install_path())
    def _update(self):
        """ Nothing to do here..."""
        pass
    def _remove(self):
        """ Remove the install directory."""
        self._system.remove(self.get_install_path())
    def _is_installed(self):
        """ Check if root is installed by looking for the root executable in the bin directory.

        :return: True if installed
        """
        return self._system.is_library(os.path.join(self.get_install_path(), "lib/libCLHEP"))
    
# The versions of clhep that can be installed
versions = [type('clhep-2.1.1.0', (Clhep, object), {"_version" : "clhep-2.1.1.0"}),
            type('clhep-2.1.0.1', (Clhep, object), {"_version" : "clhep-2.1.0.1"}),
            type('clhep-2.0.4.2', (Clhep, object), {"_version" : "clhep-2.0.4.2"})]


