#!/usr/bin/env python
#
# DryRun
#
# Dry run system implementation, just saves the relevant commands to a file.
#
# Author P G Jones - 2014-06-18 <p.g.jones@qmul.ac.uk> : New file.
####################################################################################################
import system
import logging
logger = logging.getLogger(__name__)

class DryRun(system.System):
    """ The standard system implementation"""
    def __init__(self, install_path, file_name=None):
        """ Initialise the system with an *install_path*

        :param install_path: Location to install to
        :type install_path: string
        :param file_name: optional filename to output commands too, defaults to dry_run_date.nusoft
        """
        super(Standard, self).__init__(install_path)
        if file_name is None:
            file_name = "dry_run_" + datetime.datetime.now().isoformat() + ".nusoft"
        self._file = open(file_name, "w")
        self._file.write("Installing to %s\n" % install_path)
    def __del__(self):
        """ Closes the open file. """
        self._file.close();
####################################################################################################
# Comamnds to alter/create files
    def exists(self, file):
        """ Check if the *file* or directory at *file* exists
        
        :param file: to check
        :return: True if it exists
        """
        file_path = self._file_path(file)
        self._file.write("Check %s exists\n" % file_path)
        logger.debug("Checking file %s exists == %r" % (file_path, exists))
        return False
    def is_library(self, file):
        """ Check if the *file* is a library

        :param file: to check
        :return: True if the *file* is a library on this system
        """
        file = file.split(".")[0]
        file_path = self._file_path(file)
        self._file.write("Check %s is a library\n" % file_path)
        library = self.exists(file_path + ".a") or self.exists(file_path + ".so") or self.exists(file_path + ".dylib")
        logger.debug("Checking file %s is a library == %r" % (file_path, library))
        return library
    def remove(self, file):
        """ Remove the *file* or directory at *file*

        :param file: to remove
        """
        file_path = self._file_path(file)
        self._file.write("Remove the file %s\n" % file_path)
        logger.debug("Removing file %s" % file_path)
    def download(self, url, authenticate=False, name=None, retries=0):
        """ Download the *url* to a file called *name* in the temporary path, if *name* is not set
        will save to the url filename. If *authenticate* is True the credentials are queried and
        required. Retry downloading *retries* number of times
        
        :param url: of the file to download
        :type url: string
        :param authenticate: True if authentication is required.
        :param name: optional name to save to in the temporary path
        :type name: string
        :param retries: number of retries
        :type retries: int
        """
        if name is None:
            name = url.split('/')[-1]
        target_path = self._file_path(name)
        self._file.write("Download %s to %s\n" % (url, target_path))
        logger.debug("Downloaded %s to %s" % (url, target_path))
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
        file_path = self._file_path(file)
        target_path = self._file_path(target)
        self._file.write("Untar %s to %s, strip %i leading folders\n" % (file_path, target_path, strip_depth))
        logger.debug("Untaring file %s to %s, with %i stripped" % (file_path, target_path, strip_depth))
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
        self._file.write("Configure: %s\n" % command)
        if args is not None:
            self._file.write("\twith args: %r\n" % args)
        if cwd is not None:
            self._file.write("\tin directory: %s\n" % cwd)
        if env is not None:
            self._file.write("\tand environment: %r\n" % env)
        logger.debug("Configuring via command %s" % command)
        return self.execute(command, args, cwd, env)
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
        :return: tuple, Truth if returncode is 0 and standard output from command
        :rtype: tuple bool and string
        """
        if cwd is None:
            cwd = self.get_install_path()
        # Firstly setup the environment
        local_env = os.environ.copy()
        if env is not None:
            pass
        # Now open and run the shell_command
        shell_command = [command]
        if args is not None:
            shell_command.extend(args)
        self._file.write("Executing %s\n" % ' '.join(shell_command))
        self._file.write("\twith environment: %r\n" % local_env)
        logger.info("Executing %s" % ' '.join(shell_command))
        return (True, "")
    def compilation_test(self, headers=None, flags=None):
        """ Test that a file can be compiled by g++ with the *headers* and linkage *flags*.
        
        :param headers: list of header names with extension
        :param flags: list of flags
        :return: True if compiles
        """
        self._file.write("Test compilation with headers %r and flags %r" % (headers, flags))
        logger.debug("Testing compilation with headers %r and flags %r" % (headers, flags))
        return ""
    
