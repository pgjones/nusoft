#!/usr/bin/env python
#
# Mac
#
# Mac system implementation.
#
# Author P G Jones - 2014-08-15 <p.g.jones@qmul.ac.uk> : New file.
####################################################################################################
import standard
import os
import shutil
import tarfile
import urllib2
import base64
import subprocess
import logging
logger = logging.getLogger(__name__)

class Mac(standard.Standard):
    """ The mac system implementation"""
    def __init__(self, install_path):
        """ Initialise the system with an *install_path*

        :param install_path: Location to install to
        :type install_path: string
        """
        super(Mac, self).__init__(install_path)
        # Now check for various installation locations and add to the c++ paths
        # Check if XCode in 10.7 installs X11 to /usr/X11
        if os.path.exists("/usr/X11"):
            self._append_environment("PATH", "/usr/X11/bin")
            self._append_environment("LIBRARY_PATH", "/usr/X11/lib")
            self._append_environment("CPLUS_INCLUDE_PATH", "/usr/X11/include")
        # Check if Open Motif has installed somewhere else
        if os.path.exists("/usr/OpenMotif"):
            self._append_environment("PATH", "/usr/OpenMotif/bin")
            self._append_environment("LIBRARY_PATH", "/usr/OpenMotif/lib")
            self._append_environment("CPLUS_INCLUDE_PATH", "/usr/OpenMotif/include")
####################################################################################################
    def is_library(self, file):
        """ Check if the *file* is a library, Mac looks for dylib

        :param file: to check
        :return: True if the *file* is a library on this system
        """
        file_path = self._file_path(file)
        library = self.exists(file_path + ".a") or self.exists(file_path + ".so") or \
                  self.exists(file_path + ".dylib")
        logger.debug("Checking file %s is a library == %r" % (file_path, library))
        return library
####################################################################################################
    def _append_environment(self, key, value, env=os.environ):
        """ Append the value to environment (env) variable key, if key exists, if not make it.

        :param key: to append to
        :param value: to append
        :param env: environment to use, defaults to os.environ"""
        if key in env:
            env[key] = "%s:%s" % (value, env[key])
        else:
            env[key] = value
