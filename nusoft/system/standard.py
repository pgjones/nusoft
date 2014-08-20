#!/usr/bin/env python
#
# Standard
#
# Standard system implementation.
#
# Author P G Jones - 2014-02-22 <p.g.jones@qmul.ac.uk> : New file.
####################################################################################################
import system
import os
import shutil
import tarfile
import urllib2
import base64
import subprocess
import logging
logger = logging.getLogger(__name__)

class Standard(system.System):
    """ The standard system implementation"""
    def __init__(self, install_path):
        """ Initialise the system with an *install_path*

        :param install_path: Location to install to
        :type install_path: string
        """
        super(Standard, self).__init__(install_path)
####################################################################################################
# Comamnds to alter/create files
    def exists(self, file):
        """ Check if the *file* or directory at *file* exists
        
        :param file: to check
        :return: True if it exists
        """
        file_path = self._file_path(file)
        exists = os.path.exists(file_path)
        logger.debug("Checking file %s exists == %r" % (file_path, exists))
        return exists
    def is_library(self, file):
        """ Check if the *file* is a library

        :param file: to check
        :return: True if the *file* is a library on this system
        """
        file_path = self._file_path(file)
        library = self.exists(file_path + ".a") or self.exists(file_path + ".so")
        logger.debug("Checking file %s is a library == %r" % (file_path, library))
        return library
    def remove(self, file):
        """ Remove the *file* or directory at *file*

        :param file: to remove
        """
        file_path = self._file_path(file)
        if os.path.isdir(file_path):
            shutil.rmtree(file_path)
        elif os.path.isfile(file_path):
            os.remove(file_path)
        logger.debug("Removing file %s" % file_path)
    def set_chmod(self, file, value):
        """ Set the chmod attributes of *file*
        
        :param file: to set the chmod attributes of
        :param value: to set
        """
        file_path = self._file_path(file)
        os.chmod(file_path, value)
        logger.debug("Setting chmod of %s to %s" % (file_path, value))
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
        if self.exists(target_path):
            return
        url_request = urllib2.Request(url)
        if authenticate: # HTTP authentication needed
            credentials = self._credentials.authenticate()
            if type(credentials) is tuple:
                b64string = base64.encodestring('%s:%s' % credentials)
                url_request.add_header("Authorization", "Basic %s" % b64string)
            else:
                url_request.add_header("Authorization", "token %s" % credentials)
        try:
            remote_file = urllib2.urlopen(url_request)
            with open(target_path, 'wb') as local_file:
                local_file.write(remote_file.read())
            remote_file.close()
        except urllib2.URLError, e: # No internet connection
            logger.exception("Tried to download %s to %s" % (url, target_path))
            self.remove(target_path)
            raise
        logger.debug("Downloaded %s to %s" % (url, target_path))
    def git_clone(self, url, target):
        """ Git clone the repository at *url* to the *target* path.

        :param url: of the git repository
        :type url: string
        :param target: target location, absolute path
        :type target: string
        """
        target_path = self._file_path(target)
        self.execute("git", ["clone", url, target_path])
        logger.debug("Git cloned %s to %s" % (url, target_path))
    def git_update(self, target):
        """ Update a git repository at *target* path by fetching and merging origin/master.
        This only occurs if the repository has no changes.

        :param target: target location, absolute path
        :type target: string
        """
        target_path = self._file_path(target)
        # Check if the target has any changes, and drop out if so
        result = self.execute("git", ["status", "--porcelain"], cwd=target_path)
        if result[1] is None or result[1] == "" or result[1] == "\n":
            # Fetch the origin, checkout master merge origin master and return
            self.execute("git", ["fetch", "origin"], cwd=target_path)
            self.execute("git", ["checkout", "origin"], cwd=target_path)
            self.execute("git", ["merge", "origin/master"], cwd=target_path)
            self.execute("git", ["checkout", "-"], cwd=target_path)
            logger.debug("Git updated %s" % (target_path))
            return True
        else:
            return False # cannot update the repo
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
        if self.exists(target_path):
            self.remove(target_path)
        if strip_depth == 0: # Untar directly into target
            with tarfile.open(file_path) as tar_file:
                tar_file.extractall(target_path)
        else: # Must extract to temp target then copy strip directory to real target
            temp_path = self._file_path("tartemp")
            if self.exists(temp_path): # Delete it
                self.remove(temp_path)
            os.makedirs(temp_path)
            with tarfile.open(file_path) as tar_file:
                tar_file.extractall(temp_path)
            copy_path = temp_path
            for depth in range(0, strip_depth):
                sub_folders = os.listdir(copy_path)
                if 'pax_global_header' in sub_folders:
                    sub_folders.remove('pax_global_header')
                copy_path = os.path.join(copy_path, sub_folders[0])
            shutil.copytree(copy_path, target_path)
            self.remove(temp_path)
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
        :raises Exception: if the configure fails
        """
        logger.debug("Configuring via command %s" % command)
        result = self.execute(command, args, cwd, env)
        if not result[0]:
            raise Exception("Configuration failed")
        return result
    def make(self, command='make', args=None, cwd=None, env=None):
        """ Run a make *command* in the *cwd* directory with arguments, *args* and optional *env*, 
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
        :raises Exception: if the make fails
        """
        logger.debug("Make via command %s" % command)
        result = self.execute(command, args, cwd, env)
        if not result[0]:
            raise Exception("Make failed")
        return result
    def execute_commands(self, commands):
        
        file_name = os.path.join(self.get_install_path(), "temp.sh")
        with open(file_name, "w") as command_file:
            command_file.write('\n'.join(commands))
        self.execute("/bin/bash", args=[file_name])
        self.remove(file_name)
    def execute(self, command, args=None, cwd=None, env=None):
        """ Run a configure *command* in the *cwd* directory with arguments, *args* and optional *env*,
        environment.

        :param command: command to execute or list of commands to execute together
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
        logger.info("Executing %s" % ' '.join(shell_command))
        try:
            process = subprocess.Popen(args=shell_command, env=local_env, cwd=cwd,
                                       stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        except exceptions.OSError,e:
            logger.exception("Tried executing %s and failed" % ' '.join(shell_command))
        output, error = process.communicate()
        logger.debug("Executing %s, gives \n{\noutput : %s\nerror: %s\n}\n" % (' '.join(shell_command), output, error))
        # After process has finished
        if process.returncode != 0:
            logger.error("Tried executing %s and failed %i" % (' '.join(shell_command), process.returncode))
        return (process.returncode == 0, output) # Very useful for library checking
    def compilation_test(self, headers=None, flags=None):
        """ Test that a file can be compiled by g++ with the *headers* and linkage *flags*.
        
        :param headers: list of header names with extension
        :param flags: list of flags
        :return: True if compiles
        """
        logger.debug("Testing compilation with headers %r and flags %r" % (headers, flags))
        file_text = ""
        for header in headers:
            file_text += "#include <%s>\n" % header
        file_text += "int main( int a, char* b[] ) { }"
        file_path = self._file_path("temp.cc")
        with open(file_path, "w") as test_file:
            test_file.write(file_text)
        output = self.execute("g++", [file_path] + flags, cwd=self.get_temporary_path())
        self.remove(file_path)
        return output[0]
    
