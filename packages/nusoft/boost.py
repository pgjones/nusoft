#!/usr/bin/env python
#
# Boost
#
# Boost packages and versions
#
# Author P G Jones - 2014-08-24 <p.g.jones@qmul.ac.uk> : New file.
####################################################################################################
import nusoft.package.conditional as conditional_package
import os

class Boost(conditional_package.ConditionalPackage):
    """ The Boost installation package.
    
    :param _tar_name: name of the tar file to download/install
    :param _version: version of Boost to install.
    """
    def __init__(self, system, repository):
        """ Initialise this boost installation package.

        :param system: class that manages system commands
        :type system: :class:`nusoft.system.System` instance
        :param repository: local name of the repository the package is from
        """
        super(Boost, self).__init__(self._version, system, repository, 
                                    headers=["boost/lambda/lambda.hpp"])
        self._tar_name = self._version + ".tar.gz"
    def get_dependencies(self):
        """ Return a list of dependency names

        :returns: list of dependency package names
        :rtype: list
        """
        return []
    def _download(self):
        """ Download the boost tar file."""
        self._system.download("http://downloads.sourceforge.net/project/boost/boost/1.56.0/" + self._tar_name)
    def _install(self):
        """ Untar the tar file to the install path."""
        self._system.untar(self._tar_name, self.get_install_path())
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
        return self._system.exists(os.path.join(self.get_install_path(), "boost/lambda/lambda.hpp"))
    
# The versions of root that can be installed
versions = [type('boost_1_56_0', (Boost, object), {"_version" : "boost_1_56_0"})]

