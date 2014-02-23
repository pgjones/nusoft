#!/usr/bin/env python
#
# CommandPackage 
#
# Packages that are global system commands e.g. g++
#
# Author P G Jones - 2014-02-23 <p.g.jones@qmul.ac.uk> : First revision
####################################################################################################
import package
import os
import logging
logger = logging.getLogger(__name__)

class CommandPackage(package.Package):
    """ Packages that are global system commands

    :param _command: The package command
    :type _command: string
    """
    def __init__(self, name, system, repository, command):
        """ Construct the package with a *name* and the *system* installation information.
        This package is executed by it's *command*.
        
        :param string name: name of this package.
        :param system: class that manages system commands
        :type system: :class:`nusoft.system.System` instance
        :param repository: local name of the repository the package is from
        :param command: name of the command to execute the package
        :type command: string
        """
        super(CommandPackage, self).__init__(name, system, repository)
        self._command = command
    def check_state(self):
        """ Try to find the location of the command."""
        result = self._system.execute("which", [self._command])
        logger.debug("Command which gives location at %r" % result[1])
        if result[1] is not None and result[1] != "" and result[1] != "\n":
            self._install_path = os.path.abspath(result[1])
            self._installed = True
