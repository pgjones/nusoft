#!/usr/bin/env python
#
# EnvFile
#
# Writes out environment files in a correctly formated manner.
#
# Author P G Jones - 2014-03-23 <p.g.jones@qmul.ac.uk> : First revision
####################################################################################################
import os
import logging
logger = logging.getLogger(__name__)

class EnvFile( object ):
    """ Correctly formats environment files.

    :param _bash_text: The text for bash files.
    :param _csh_text: The text for csh files.
    :param _library_path: The library path environment text
    :param _path: The path environment text
    :param _python_path: The python path environment text
    :param _bash_post_text: The final text for bash files
    :param _csh_post_text: The final text for csh files
    """
    def __init__(self, comment=None):
        """ Initialise the env file with an optional *comment*.

        :param comment: Optional comment
        """
        self._bash_text = "#!/bin/bash\n" # Full text for the bash file
        self._csh_text = "#!/bin/csh\n" # Full text for the csh file
        if comment is not None:
            self._bash_text += comment
            self._csh_text += comment
        self._library_path = "" # Full library path environment text (additions)
        self._path = "" # Full path environment text (additions)
        self._python_path = "" # Full python path environment text (additions)
        self._bash_post_text = "" # Text to go at the end of the bash file
        self._csh_post_text = "" # Text to go at the end of the csh file
    def add_source(self, file_path, file_name):
        """ Add a source command, to source *file_name* at *file_path*.
        
        :param file_path: path of the file to source
        :param file_name: name of the file to source
        """
        self._bash_text += "source %s/%s.sh\n" % (file_path, file_name)
        self._csh_text += "source %s/%s.csh\n" % (file_path, file_name)
    def add_post_source(self, file_path, file_name):
        """ Add a source command to the end of the file. To source *file_name* at *file_path*.
        
        :param file_path: path of the file to source
        :param file_name: name of the file to source
        """
        self._bash_post_text += "source %s/%s.sh\n" % (file_path, file_name)
        self._csh_post_text += "source %s/%s.csh\n" % (file_path, file_name)
    def add_environment(self, key, value):
        """ Add an environment variable. *key* with *value*

        :param key: environment variable key
        :param value: value of the environment
        """
        self._bash_text += "export %s=%s\n" % (key, value)
        self._csh_text += "setenv %s %s\n" % (key, value)
    def add_command(self, command):
        """ Add a *command*.
        
        :param command: to add
        """
        self._bash_post_text += "%s\n" % command
        self._csh_post_text += "%s\n" % command
    def append_library_path(self, path):
        """ Append a path to the library path.
        
        :param path: library path to add
        """
        self._library_path += "%s:" % path
    def append_path(self, path):
        """ Append a path to the PATH.

        :param path: path to add
        """
        self._path += "%s:" % path
    def append_python_path(self, path):
        """ Append a path to the PYTHONPATH.

        :param path: path to add
        """
        self._python_path += "%s:" % path
    def write(self, directory, name):
        """ Write the env files to the directory called name.sh and name.csh.
        
        :param directory: to save the env files in
        :param name: of the env file
        """
        # Strip the trailing :
        self._library_path = self._library_path[0:-1]
        self._path = self._path[0:-1]
        self._python_path = self._python_path[0:-1]
        # First add the Path
        self._bash_text += "export PATH=%s:$PATH\n" % self._path
        self._csh_text += "setenv PATH %s:${PATH}\n" % self._path
        # Next add the python path
        if self._python_path is not "":
            self._bash_text += "export PYTHONPATH=%s:$PYTHONPATH\n" % self._python_path
            self._csh_text += ("if(${?PYTHONPATH}) then\nsetenv PYTHONPATH %s:${PYTHONPATH}\nelse\n"
                               "setenv PYTHONPATH %s\nendif\n") % (self._python_path, self._python_path)
        # Next add the libraries (Harder for cshell)
        if self._library_path is not "":
            self._bash_text += "export LD_LIBRARY_PATH=%s:$LD_LIBRARY_PATH\n" % self._library_path
            self._bash_text += "export DYLD_LIBRARY_PATH=%s:$DYLD_LIBRARY_PATH\n" % self._library_path
            self._csh_text += ("if(${?LD_LIBRARY_PATH}) then\nsetenv LD_LIBRARY_PATH %s:"
                               "${LD_LIBRARY_PATH}\nelse\nsetenv LD_LIBRARY_PATH %s\nendif\n") % \
                               (self._library_path, self._library_path)
            self._csh_text += ("if(${?DYLD_LIBRARY_PATH}) then\nsetenv DYLD_LIBRARY_PATH %s:"
                               "${DYLD_LIBRARY_PATH}\nelse\nsetenv DYLD_LIBRARY_PATH %s\nendif\n") % \
                               (self._library_path, self._library_path)
        # Finnally add the rat
        self._bash_text += self._bash_post_text
        self._csh_text += self._csh_post_text
        # Now write the files
        file_path = os.path.join(directory, name)
        with open(file_path + ".sh", "w") as bash_file:
            bash_file.write(self._bash_text)
        with open(file_path + ".csh", "w") as csh_file: 
            csh_file.write(self._csh_text)
        logger.info("%s in %s .sh and .csh written" % (name, directory))
