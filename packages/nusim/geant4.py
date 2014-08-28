#!/usr/bin/env python
#
# Geant4
#
# GEANT4 packages and versions for nusim, this installs the python bindings
#
# Author P G Jones - 2014-08-24 <p.g.jones@qmul.ac.uk> : New file.
####################################################################################################
import nusoft.package.local as local_package
import os

class Geant4(local_package.LocalPackage):
    """ The GEANT4 installation package.
    
    :param _tar_name: name of the tar file to download/install
    :param _version: version of GEANT4 to install.
    :param _source_path: path to place the source files
    """
    def __init__(self, system, repository):
        """ Initialise this geant4 installation package.

        :param system: class that manages system commands
        :type system: :class:`nusoft.system.System` instance
        :param repository: local name of the repository the package is from
        """
        super(Geant4, self).__init__(self._version, system, repository)
        self._tar_name = self._version + ".tar.gz"
        self._source_path = os.path.join(self._system.get_install_path(), "%s-source" % self._name)
    def get_dependencies(self):
        """ Return a list of dependency names

        :returns: list of dependency package names
        :rtype: list
        """
        return ["make", "g++", "gcc", "cmake-2.8.12.1", "boost_1_56_0"]
    def _download(self):
        """ Download the geant4 tar file."""
        self._system.download("http://geant4.web.cern.ch/geant4/support/source/" + self._tar_name)
    def _install(self):
        """ Untar the tar file and install it to the install path."""
        self._system.untar(self._tar_name, self._source_path, 1)
        if not self._system.exists(self.get_install_path()):
            os.makedirs(self.get_install_path())
        cmake_opts = ["-DCMAKE_INSTALL_PREFIX=%s" % self.get_install_path(), 
                      "-DGEANT4_INSTALL_DATA=ON", self._source_path]
        cmake = os.path.join(self._dependencies["cmake-2.8.12.1"].get_install_path(), "bin/cmake")
        self._system.configure(cmake, cmake_opts, self.get_install_path())
        self._system.make(cwd=self.get_install_path())
        self._system.make(args=['install'], cwd=self.get_install_path())
        # Now the python bit
        sys = "linux64"
        if os.uname()[0] == "Darwin":
            sys = "macosx"
        python_install_path = os.path.join(self.get_install_path(), "g4py")
        os.makedirs(python_install_path)
        self._system.configure(args=[sys,
                                     "--with-g4install-dir=%s" % self.get_install_path(),
                                     "--prefix=%s" % python_install_path],
                               cwd=os.path.join(self._source_path, "environments/g4py"))
        self._system.make(cwd=os.path.join(self._source_path, "environments/g4py"))
        self._system.make(args=['install'], cwd=os.path.join(self._source_path, "environments/g4py"))
    def _update(self):
        """ Nothing to do here..."""
        pass
    def _remove(self):
        """ Remove the install directory."""
        self._system.remove(self.get_install_path())
        self._system.remove(self._source_path)
    def _is_installed(self):
        """ Check if geant4 is installed by looking for the geant4 executable in the bin directory.

        :return: True if installed
        """
        return self._system.is_library(os.path.join(self.get_install_path(), "lib/libG4event")) or \
            self._system.is_library(os.path.join(self.get_install_path(), "lib64/libG4event"))
    
# The versions of geant4 that can be installed
versions = [type('Geant410002', (Geant4, object), {"_version" : "geant4.10.00.p02"})]

