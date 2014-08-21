#!/usr/bin/env python
#
# Root
#
# ROOT packages and versions
#
# Author P G Jones - 2014-08-21 <p.g.jones@qmul.ac.uk> : New file.
####################################################################################################
import nusoft.package.local as local_package
import os

class Root(local_package.LocalPackage):
    """ The ROOT installation package.
    
    :param _tar_name: name of the tar file to download/install
    :param _version: version of ROOT to install.
    """
    def __init__(self, system, repository):
        """ Initialise this root installation package.

        :param system: class that manages system commands
        :type system: :class:`nusoft.system.System` instance
        :param repository: local name of the repository the package is from
        """
        super(Root, self).__init__(self._version, system, repository)
        self._tar_name = self._version + ".source.tar.gz"
    def get_dependencies(self):
        """ Return a list of dependency names

        :returns: list of dependency package names
        :rtype: list
        """
        return ["make", "g++", "gcc", "ld", "python", "x11", "xpm", "xft", "xext", "python-dev"]
    def _download(self):
        """ Download the root tar file."""
        self._system.download("ftp://root.cern.ch/root/" + self._tar_name)
    def _install(self):
        """ Untar the tar file and install it to the install path."""
        self._system.untar(self._tar_name, self.get_install_path(), 1)
        args = ['--enable-roofit',  '--enable-python']
        self._system.configure(args=args, cwd=self.get_install_path())
        self._system.make(cwd=self.get_install_path())
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
        return self._system.exists(os.path.join(self.get_install_path(), "bin/root"))
    
# The versions of root that can be installed
versions = [type('root_v5.34.10', (Root, object), {"_version" : "root_v5.34.10"})]
