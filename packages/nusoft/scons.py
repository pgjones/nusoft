#!/usr/bin/env python
#
# SCons
#
# SCons packages and versions
#
# Author P G Jones - 2014-08-15 <p.g.jones@qmul.ac.uk> : New file.
####################################################################################################
import nusoft.package.local as local_package
import os

class SCons(local_package.LocalPackage):
    """ The SCons installation package.
    
    :param _tar_name: name of the tar file to download/install
    :param _version: version of SCons to install.
    """
    def __init__(self, system, repository):
        """ Initialise this scons installation package.

        :param system: class that manages system commands
        :type system: :class:`nusoft.system.System` instance
        :param repository: local name of the repository the package is from
        """
        super(SCons, self).__init__(self._version, system, repository)
        self._tar_name = self._version + ".tar.gz"
    def get_dependencies(self):
        """ Return a list of dependency names

        :returns: list of dependency package names
        :rtype: list
        """
        return ["python"]
    def _download(self):
        """ Download the scons tar file."""
        self._system.download("http://downloads.sourceforge.net/project/scons/scons/" +
                              self._number + "/" + self._tar_name)
    def _install(self):
        """ Untar the tar file to the install path."""
        self._system.untar(self._tar_name, self.get_install_path(), 1)
        self._system.set_chmod(os.path.join(self.get_install_path(), "script/scons"), 0755)
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
        return self._system.exists(os.path.join(self.get_install_path(), "script/scons"))
    
# The versions of root that can be installed
versions = [type('scons-2.1.0', (SCons, object), {"_version" : "scons-2.1.0",
                                                  "_number" : "2.1.0"}),
            type('scons-1.2.0', (SCons, object), {"_version" : "scons-1.2.0",
                                                  "_number" : "1.2.0"})]

