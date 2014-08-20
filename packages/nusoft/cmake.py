#!/usr/bin/env python
#
# Cmake
#
# Cmake packages and versions
#
# Author P G Jones - 2014-02-24 <p.g.jones@qmul.ac.uk> : New file.
####################################################################################################
import nusoft.package.local as local_package
import os

class Cmake(local_package.LocalPackage):
    """ The CMAKE installation package.
    
    :param _tar_name: name of the tar file to download/install
    :param _version: version of CMAKE to install.
    """
    def __init__(self, system, repository):
        """ Initialise this cmake installation package.

        :param system: class that manages system commands
        :type system: :class:`nusoft.system.System` instance
        :param repository: local name of the repository the package is from
        """
        super(Cmake, self).__init__(self._version, system, repository)
        self._tar_name = self._version + ".tar.gz"
    def _download(self):
        """ Download the cmake tar file."""
        self._system.download("http://www.cmake.org/files/v2.8/" + self._tar_name)
    def _install(self):
        """ Untar the tar file and install it to the install path."""
        self._system.untar(self._tar_name, self.get_install_path(), 1)
        self._system.configure(command="./bootstrap", args=["--prefix=%s" % self.get_install_path()], 
                               cwd=self.get_install_path())
        self._system.make(cwd=self.get_install_path())
        self._system.make(args=["install"], cwd=self.get_install_path())
    def _update(self):
        """ Nothing to do here..."""
        pass
    def _remove(self):
        """ Remove the install directory."""
        self._system.remove(self.get_install_path())
    def _is_installed(self):
        """ Check if cmake is installed by looking for the cmake executable in the bin directory.

        :return: True if installed
        """
        return self._system.exists(os.path.join(self.get_install_path(), "bin/cmake"))
    
# The versions of cmake that can be installed
versions = [type('Cmake28121', (Cmake, object), {"_version" : "cmake-2.8.12.1"}),
            type('Cmake288', (Cmake, object), {"_version" : "cmake-2.8.8"}),]
