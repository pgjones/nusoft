#!/usr/bin/env python
#
# NuSimDev
#
# The NuSim development version
#
# Author P G Jones - 2014-06-20 <p.g.jones@qmul.ac.uk> : New file.
####################################################################################################
import nusoft.package.local as local_package
import os
import nusoft.envfile

class NuSimDev(local_package.LocalPackage):
    """ The NuSimDev installation package.
    
    :param _root: version of ROOT this is dependent on
    :param _geant4: version of Geant4 this is dependent on
    """
    def __init__(self, system, repository):
        """ Initialise this nusim installation package.

        :param system: class that manages system commands
        :type system: :class:`nusoft.system.System` instance
        :param repository: local name of the repository the package is from
        """
        super(NuSimDev, self).__init__("nusim-dev", system, repository)
        self._root = "root_v5.34.18"
        self._geant4 = "nugeant4.10.00.p02"
    def get_dependencies(self):
        """ Return a list of dependency names

        :returns: list of dependency package names
        :rtype: list
        """
        return ["make", "g++", "gcc", "ld", "python", "python-dev", self._root, self._geant4]
    def _download(self):
        """ Git clone the nusim repository file."""
        self._system.git_clone("git@github.com:pgjones/nusim.git", self.get_install_path())
    def _install(self):
        """ Write an environment file and install nusim."""
        # Now write the environment file
        self.write_env_file()
        # Nothing else to do
    def write_env_file(self):
        """ Write an environment file for this package."""
        env_file = nusoft.envfile.EnvFile("#nusim environment\n")
        env_file.add_source(os.path.join(self._dependencies[self._root].get_install_path(), "bin"), "thisroot")
        env_file.add_source(os.path.join(self._dependencies[self._geant4].get_install_path(), "bin"), "geant4")
        env_file.append_python_path(os.path.join(self._dependencies[self._geant4].get_install_path(), "g4py/lib"))
        env_file.write(self._system.get_install_path(), "env_nusim-dev")
    def _update(self):
        """ Update the git repository."""
        if not self._system.git_update(self.get_install_path()):
            raise Exception("Cannot update, repository has changes")
        self._install() # Now reinstall (compile)
    def _remove(self):
        """ Remove the install directory."""
        self._system.remove(self.get_install_path())
    def _is_installed(self):
        """ Check if installed by seeing if the files exist

        :return: True if installed
        """
        return self._system.exists(self.get_install_path())
    
# The versions of NuSimDev that can be installed (only one, NusimDev) 
# [Although potentially more if the user wants].
versions = [NuSimDev]
