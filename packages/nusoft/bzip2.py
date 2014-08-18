#!/usr/bin/env python
#
# Bzip2
#
# Bzip2 packages and versions
#
# Author P G Jones - 2014-08-15 <p.g.jones@qmul.ac.uk> : New file.
####################################################################################################
import nusoft.package.conditional as conditional_package
import os

class Bzip2(conditional_package.ConditionalPackage):
    """ The Bzip2 installation package.
    
    :param _tar_name: name of the tar file to download/install
    :param _version: version of Bzip2 to install.
    """
    def __init__(self, system, repository):
        """ Initialise this bzip2 installation package.

        :param system: class that manages system commands
        :type system: :class:`nusoft.system.System` instance
        :param repository: local name of the repository the package is from
        """
        super(Bzip2, self).__init__(self._version, system, repository, libraries=["bz2"], headers=["bzlib.h"])
        self._tar_name = self._version + ".tar.gz"
    def get_dependencies(self):
        """ Return a list of dependency names

        :returns: list of dependency package names
        :rtype: list
        """
        return []
    def _download(self):
        """ Download the bzip2 tar file."""
        self._system.download("http://bzip2.haxx.se/download/" + self._tar_name)
    def _install(self):
        """ Untar the tar file to the install path."""
        self._system.untar(self._tar_name, self.get_install_path(), 1)
        self._system.execute("make", ["-f", "Makefile-libbz2_so"], self.get_install_path())
        self._system.execute("make", ["install", "PREFIX=" + self.get_install_path()], 
                             self.get_install_path())
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
        return self._system.exists(os.path.join(self.get_install_path(), "include/bzlib.h")) \
            and self._system.is_library(os.path.join(self.get_install_path(), "lib/libbz2"))
    
# The versions of root that can be installed
versions = [type('bzip2-1.0.6', (Bzip2, object), {"_version" : "bzip2-1.0.6"})]

