#!/usr/bin/env python
#
# WCSimDev
#
# The HyperK WCSim development version
#
# Author P G Jones - 2014-06-20 <p.g.jones@qmul.ac.uk> : New file.
####################################################################################################
import nusoft.package.local as local_package
import os
import nusoft.envfile

class WCSimDev(local_package.LocalPackage):
    """ The WCSimDev installation package.
    
    :param _root: version of ROOT this is dependent on
    :param _geant4: version of Geant4 this is dependent on
    """
    def __init__(self, system, repository):
        """ Initialise this wcsim installation package.

        :param system: class that manages system commands
        :type system: :class:`nusoft.system.System` instance
        :param repository: local name of the repository the package is from
        """
        super(WCSimDev, self).__init__("wcsim-dev", system, repository)
        self._root = "root_v5.34.10"
        self._geant4 = "geant4.9.4.p04"
    def get_dependencies(self):
        """ Return a list of dependency names

        :returns: list of dependency package names
        :rtype: list
        """
        return ["make", "g++", "gcc", "ld", "python", "python-dev", self._root, self._geant4]
    def _download(self):
        """ Git clone the wcsim repository file."""
        self._system.git_clone("ssh://git@poset.ph.qmul.ac.uk/hk-WCSim", self.get_install_path())
    def _install(self):
        """ Write an environment file and install wcsim."""
        # Now write the environment file
        self.write_env_file()
        commands = ["source " + os.path.join(self._system.get_install_path(), "env_wcsim-dev.sh"),
                    "cd " + self.get_install_path(),
                    "make rootcint",
                    "make "]
        self._system.execute_commands(commands)
    def write_env_file(self):
        """ Write an environment file for this package."""
        env_file = nusoft.envfile.EnvFile("#wcsim environment\n")
        env_file.add_source(os.path.join(self._dependencies[self._root].get_install_path(), "bin"), "thisroot")
        env_file.add_source(os.path.join(self._dependencies[self._geant4].get_install_path(), 
                                         "share/geant4-9.4.4/config"), 
                            "geant4-9.4.4")
        env_file.write(self._system.get_install_path(), "env_wcsim-dev")
    def _update(self):
        """ Update the git repository."""
        if not self._system.git_update(self.get_install_path()):
            raise Exception("Cannot update, repository has changes")
        self._install() # Now reinstall (compile)
    def _remove(self):
        """ Remove the install directory."""
        self._system.remove(self.get_install_path())
    def _is_installed(self):
        """ Check if root is installed by looking for the root executable in the bin directory.

        :return: True if installed
        """
        sys = os.uname()[0]
        return False
    
# The versions of WCSimDev that can be installed (only one, WCSimDev) 
# [Although potentially more if the user wants].
versions = [WCSimDev]
