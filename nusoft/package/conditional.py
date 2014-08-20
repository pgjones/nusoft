#!/usr/bin/env python
#
# ConditionalPackage class
#
# These packages are installed to the target folder iff they are not already on the system.
#
# Author P G Jones - 2014-02-14 <p.g.jones@qmul.ac.uk> : First revision
####################################################################################################
import package
import os
import logging
logger = logging.getLogger(__name__)

class ConditionalPackage(package.Package):
    """ Base class for packages that can be installed to the target folder, iff they are not 
    already on the system.

    :param _updated: True if the package has been updated in the current session.
    :param _libraries: list of libraries
    :param _headers: list of headers with extension
    :param _flags: list of flags
    :param _config: config command
    """
    def __init__(self, name, system, repository, libraries=None, headers=None, flags=None, config=None):
        """ Construct the package with a *name* and the *system* installation information.
        
        :param string name: name of this package.
        :param system: class that manages system commands
        :type system: :class:`nusoft.system.System` instance
        :param repository: local name of the repository the package is from
        :param libraries: list of libraries
        :param headers: list of headers with extension
        :param flags: list of flags
        :param config: config command
        """
        super(ConditionalPackage, self).__init__(name, system, repository)
        self._updated = False
        self._libraries = []
        self._headers = []
        self._flags = []
        if libraries is not None:
            self._libraries = ["-l" + library for library in libraries]
        if headers is not None:
            self._headers = headers
        if flags is not None:
            self._flags = flags
        self._config = config
    def check_state(self):
        """ Function to force the package to check what it's status is.

        If checking on the system try to find the location of the config command first (if 
        specified) and use it to find the library and headers. If not just try compiling against 
        the library with the headers.."""
        # First see if installed on the system
        if self._config is not None:
            result = self._system.execute("which", [self._config])
            logger.debug("Command which gives config location at %r" % result[1])
            if result[1] is not None and result[1] != "" and result[1] == "\n":
                output = self._system.execute(self._config, ['--libs'])
                self._libraries = output[1].strip('\n').split()
                output = self._system.execute(self._config, ['--cflags'])
                self._flags = output[1].strip('\n').split()

        if self._system.compilation_test(self._headers, self._libraries + self._flags):
            self._installed = True
            
        # Not on system so set a local install path
        self._install_path = os.path.join(self._system.get_install_path(), self._name)
        # Now check the local install folder
        if not self._installed:
            if self._is_installed():
                self._installed = True
            else:
                self._installed = False
                self._updated = False
    def install(self):
        """ Function to install the package.

        Will check if already installed first.
        """
        logger.info("Installing %s to %s" % (self._name, self._install_path))
        if not self._installed:
            self._download()
            self._install()
            self.check_state()
    def update(self):
        """ Function to update installed package.

        Will check if already updated first.
        """
        logger.info("Updating %s in %s" % (self._name, self._install_path))
        if not self._installed:
            raise
        elif self._installed and not self._updated:
            self._update()
            self._updated = True
            self.check_state()
    def remove(self):
        """ Function to remove installed package
        
        Will check if installed first.
        """
        logger.info("Removing %s from %s" % (self._name, self._install_path))
        if not self._installed:
            raise
        else:
            self._remove()
            self.check_state()
####################################################################################################
    # Functions to override by subclasses
    def write_env_file(self):
        """ Write an environment file for this package."""
        pass
    def _download(self):
        
        pass
    def _install(self):

        pass
    def _write_env_file(self):
        """ Function to write a environment file for this package."""
        pass
    def _update(self):

        pass
    def _remove(self):
        
        pass
