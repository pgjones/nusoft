#!/usr/bin/env python
#
# LibraryPackage
#
# Packages that are global system libraries e.g. X11
#
# Author P G Jones - 2014-02-23 <p.g.jones@qmul.ac.uk> : First revision
####################################################################################################
import package
import os
import logging
logger = logging.getLogger(__name__)

class LibraryPackage(package.Package):
    """ Packages that are global system commands

    :param _libraries: list of libraries
    :param _headers: list of headers with extension
    :param _flags: list of flags
    :param _config: config command
    """
    def __init__(self, name, system, repository, libraries=None, headers=None, flags=None, config=None):
        """ Construct the package with a *name* and the *system* installation information.
        This package is a *library* with *headers* and *flags* OR a *config* command with *headers* to 
        find the library and flags.
        
        :param string name: name of this package.
        :param system: class that manages system commands
        :type system: :class:`nusoft.system.System` instance
        :param repository: local name of the repository the package is from
        :param libraries: list of libraries
        :param headers: list of headers with extension
        :param flags: list of flags
        :param config: config command
        """
        super(LibraryPackage, self).__init__(name, system, repository)
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
        """ Try to find the location of the config command first (if specified) and use it
        to find the library and headers. If not just try compiling against the library with
        the headers.."""
        if self._config is not None:
            result = self._system.execute("which", [self._config])
            logger.debug("Command which gives config location at %r" % result[1])
            if result[1] is None or result[1] == "" or result[1] == "\n":
                return # Is not installed.
            output = self._system.execute(self._config, ['--libs'])
            self._libraries = output[1].strip('\n').split()
            output = self._system.execute(self._config, ['--cflags'])
            self._flags = output[1].strip('\n').split()

        if self._system.compilation_test(self._headers, self._libraries + self._flags):
            self._installed = True
        
