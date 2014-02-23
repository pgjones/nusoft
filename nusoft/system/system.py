#!/usr/bin/env python
#
# System
#
# Converts commands in actions.
#
# Author P G Jones - 2014-02-08 <p.g.jones@qmul.ac.uk> : New file.
####################################################################################################
import os
import tempfile
import logging
logger = logging.getLogger(__name__)

class System(object):
    """ The system commands, 

    :param _install_path: The installation path
    :param _temporary_path: The temporary/cache path
    """
    def __init__(self, install_path, temporary_path=None):
        """ Initialise the system with an *install_path* and an optional *temporary_path*

        :param install_path: Location to install to
        :type install_path: string
        :param temporary_path: Optional path to save files to temporarily
        :type temporary_path: string
        """
        self._install_path = install_path
        if temporary_path is not None:
            self._temporary_path = temporary_path
        else:
            self._temporary_path = os.path.join(tempfile.gettempdir(), "nusoft")
            if not self.exists(self._temporary_path):
                os.makedirs(self._temporary_path)
        logger.info("System initialised, the install path is %s and the temporary path is %s" % 
                    (self._install_path, self._temporary_path))
####################################################################################################
# Path commands
    def get_repositories_path(self):
        """ Return the repositories location.
        
        :return: the repositories base location
        :rtype: string
        """
        return os.path.abspath(os.path.join(os.path.dirname(__file__), "../../packages"))
    def get_install_path(self):
        """ Return the install path

        :return: the install path
        :rtype: string
        """
        return self._install_path
    def get_temporary_path(self):
        """ Return the temporary path
        
        :return: the temporary path
        :rtype: string
        """
        return self._temporary_path
    def _file_path(self, file):
        """ Return a full path for the file if required, or return the *file*
        
        :param file: file to consider
        :type file: string
        :return: an absolute path to the file
        :rtype: string
        """
        if file[0] == '/':
            return file
        else:
            return os.path.abspath(os.path.join(self.get_temporary_path(), file))
####################################################################################################
# Comamnds to alter/create files
    def exists(self, file):
        """ Check if the *file* or directory at *file* exists
        
        :param file: to check
        :return: True if it exists
        """
        pass
    def remove(self, file):
        """ Remove the *file* or directory at *file*

        :param file: to remove
        """
        pass
    def download(self, url, username=None, password=None, token=None, name=None, retries=0):
        """ Download the *url* to a file called *name* in the temporary path, if *name* is not set
        will save to the url filename. User the *username* and *password* if set or the *token*.
        Retry downloading *retries* number of times
        
        :param url: of the file to download
        :type url: string
        :param username: username for the url
        :type username: string
        :param password: password for the url
        :type username: string
        :param token: token for the url
        :type token: string
        :param name: optional name to save to in the temporary path
        :type name: string
        :param retries: number of retries
        :type retries: int
        """
        pass
    def untar(self, file, target, strip_depth=0):
        """ Untar the *file* to *target*, the *file* is assumed to be in the temporary directory.
        Optionally strip the *strip_depth* of leading directories in the tar *file*.

        :param file: name of the file
        :type file: string
        :param target: target location, absolute path
        :type target: string
        :param strip_depth: number of leading directories to strip
        :type strip_depth: int
        """
        pass
    def configure(self, command='./configure', args=None, cwd=None, env=None):
        """ Run a configure *command* in the *cwd* directory with arguments, *args* and optional *env*, 
        environment.
        
        :param command: optional command to execute
        :type command: string
        :param args: optional list of arguments
        :type args: list of strings
        :param cwd: optional path to execute the command in
        :type cwd: string
        :param env: optional dictionary of environment 
        :type env: dictionary of keys with values, all strings
        :return: standard output from command
        :rtype: string
        """
        pass
    def execute(self, command, args=None, cwd=None, env=None):
        """ Run a configure *command* in the *cwd* directory with arguments, *args* and optional *env*,
        environment.

        :param command: optional command to execute
        :type command: string
        :param args: optional list of arguments
        :type args: list of strings
        :param cwd: optional path to execute the command in
        :type cwd: string
        :param env: optional dictionary of environment
        :type env: dictionary of keys with values, all strings
        :return: standard output from command
        :rtype: string
        """
        pass
    def compilation_test(self, headers=None, flags=None):
        """ Test that a file can be compiled by g++ with the *headers* and linkage *flags*.
        
        :param headers: list of header names with extension
        :param flags: list of flags
        """
        pass
