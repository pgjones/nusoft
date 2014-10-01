#!/usr/bin/env python
#
# RatDev
#
# The RAT development version
#
# Author P G Jones - 2014-06-19 <p.g.jones@qmul.ac.uk> : New file.
####################################################################################################
import nusoft.package.local as local_package
import os
import nusoft.envfile

class RatDev(local_package.LocalPackage):
    """ The RatDev installation package.
    
    :param _root: version of ROOT this is dependent on
    :param _geant4: version of Geant4 this is dependent on
    :param _scons: version of scons this is dependent on 
    :param _curl: version of CURL this is dependent on 
    :param _bzip: version of bzip this is dependent on 
    """
    def __init__(self, system, repository):
        """ Initialise this rat installation package.

        :param system: class that manages system commands
        :type system: :class:`nusoft.system.System` instance
        :param repository: local name of the repository the package is from
        """
        super(RatDev, self).__init__("rat-dev", system, repository)
        self._root = "root_v5.34.21"
        self._geant4 = "geant4.10.00.p02"
        self._scons = "scons-2.1.0"
        self._curl = "curl-7.26.0"
        self._bzip = "bzip2-1.0.6"
    def get_dependencies(self):
        """ Return a list of dependency names

        :returns: list of dependency package names
        :rtype: list
        """
        return ["make", "g++", "gcc", "ld", "python", "python-dev", self._root, self._geant4, 
                self._scons, self._curl, self._bzip]
    def _download(self):
        """ Git clone the rat repository file."""
        self._system.git_clone("git@github.com:snoplus/rat.git", self.get_install_path())
    def _install(self):
        """ Write an environment file and install rat."""
        # Now write the environment file
        self.write_env_file()
        commands = ["source " + os.path.join(self._system.get_install_path(), "env_rat-dev.sh"),
                    "cd " + self.get_install_path(),
                    "./configure",
                    "source env.sh",
                    "scons"]
        self._system.execute_commands(commands)
    def write_env_file(self):
        """ Write an environment file for this package."""
        env_file = nusoft.envfile.EnvFile("#rat environment\n")
        env_file.add_environment("ROOTSYS", self._dependencies[self._root].get_install_path())
        env_file.add_environment("RAT_SCONS", self._dependencies[self._scons].get_install_path())
        env_file.append_path("$ROOTSYS/bin")
        env_file.append_python_path("$ROOTSYS/lib")
        env_file.append_library_path("$ROOTSYS/lib")
        env_file.add_source(os.path.join(self._dependencies[self._geant4].get_install_path(), "bin"), "geant4")

        if self._dependencies[self._curl].get_install_path() is not None: # If CURL is installed locally
            env_file.append_path(os.path.join(self._dependencies[self._curl].get_install_path(), "bin"))
            env_file.append_library_path(os.path.join(self._dependencies[self._curl].get_install_path(), "lib"))
        if self._dependencies[self._bzip].get_install_path() is not None: # If BZIP is installed locally
            env_file.add_environment("BZIPROOT", self._dependencies[self._bzip].get_install_path())
            env_file.append_library_path(os.path.join(self._dependencies[self._bzip].get_install_path(), "lib"))

        env_file.add_post_source(self.get_install_path(), "env")
        env_file.write(self._system.get_install_path(), "env_rat-dev")
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
        return self._system.exists(os.path.join(self.get_install_path(), "bin/rat_%s" % sys)) \
            and self._system.exists(os.path.join(self.get_install_path(), "bin/root")) \
            and self._system.is_library(os.path.join(self.get_install_path(), "lib/librat_%s" % sys)) \
            and self._system.is_library(os.path.join(self.get_install_path(), "lib/libRATEvent_%s" % sys))
    
# The versions of RatDev that can be installed (only one, RatDev) 
# [Although potentially more if the user wants].
versions = [RatDev]
