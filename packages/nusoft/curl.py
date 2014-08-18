#!/usr/bin/env python
#
# Curl
#
# Curl packages and versions
#
# Author P G Jones - 2014-08-15 <p.g.jones@qmul.ac.uk> : New file.
####################################################################################################
import nusoft.package.conditional as conditional_package
import os

class Curl(conditional_package.ConditionalPackage):
    """ The Curl installation package.
    
    :param _tar_name: name of the tar file to download/install
    :param _version: version of Curl to install.
    """
    def __init__(self, system, repository):
        """ Initialise this curl installation package.

        :param system: class that manages system commands
        :type system: :class:`nusoft.system.System` instance
        :param repository: local name of the repository the package is from
        """
        super(Curl, self).__init__(self._version, system, repository, libraries=["curl"], headers=["curl/curl.h"])
        self._tar_name = self._version + ".tar.gz"
        self._source_path = os.path.join(self._system.get_install_path(), "%s-source" % self._name)
    def get_dependencies(self):
        """ Return a list of dependency names

        :returns: list of dependency package names
        :rtype: list
        """
        return [["uuid", "ossp-uuid"]]
    def _download(self):
        """ Download the curl tar file."""
        self._system.download("http://curl.haxx.se/download/" + self._tar_name)
    def _install(self):
        """ Untar the tar file to the install path."""
        self._system.untar(self._tar_name, self._source_path(), 1)
        self._system.configure(args=["--prefix=%s" % self.get_install_path()],
                               cwd=self._source_path)
        self._system.execute("make", [], cwd=self._source_path)
        self._system.execute("make", ["install"], cwd=self._source_path)
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
        return self._system.exists(os.path.join(self.get_install_path(), "include/curl/curl.h")) \
            and self._system.is_library(os.path.join(self.get_install_path(), "lib/libcurl")) \
            and self._system.exists(os.path.join(self.get_install_path(), "bin/curl-config"))
    
# The versions of root that can be installed
versions = [type('curl-7.26.0', (Curl, object), {"_version" : "curl-7.26.0"})]

