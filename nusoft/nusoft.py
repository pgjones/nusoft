#!/usr/bin/env python
#
# Nusoft
#
# Executes user actions
#
# Author P G Jones - 2014-08-15 <p.g.jones@qmul.ac.uk> : New file.
####################################################################################################
import system.standard
import package_manager
import package_loader
import re
import logging
logger = logging.getLogger(__name__)

HEADER = '\033[95m'
OKBLUE = '\033[94m'
OKGREEN = '\033[92m'
WARNING = '\033[93m'
COMMAND = '\033[96m'
FAIL = '\033[91m'
END = '\033[0m'

class Nusoft(object):
    """ The default nusoft installer.
    
    :param _system: The system used to alter files etc...
    :param _package_manager: The package manger 
    :param _package_loader: The package loader.
    """
    def __init__(self, install_path):
        """ Initialise the nusoft installer with an installation path

        :param install_path: path to install everything to
        :type install_path: string
        """
        self._system = system.standard.Standard(install_path)
        self._package_manager = package_manager.PackageManager()
        self._package_loader = package_loader.PackageLoader(self._system, self._package_manager)
    def list(self):
        """ The list command."""
        self._package_loader.load()
        logger.info("Listing all packages.")
        for package in sorted(self._package_manager.packages()):
            if package[1].is_installed():
                print OKBLUE + ("%s from %s is installed" % (package[0], package[1].get_repository())) + END
            else:
                print ("%s from %s is known" % (package[0], package[1].get_repository()))
    def search(self, name):
        """ The search command, searches for packages that match *name*

        *name* can be a regular expression

        :param name: name of package to find
        :type name: string
        """
        logger.info("Searching for %s" % name)
        self._package_loader.load()
        re_name = re.compile(name)
        for package in self._package_manager.packages():
            if re_name.match(package[0]):
                print package[0]
    def install(self, package_name):
        """ The install command.

        :param package_name: name of package to install
        :type package_name: string
        """
        logger.info("Installing %s" % package_name)
        self._package_loader.load()
        print HEADER + ("Installing %s" % package_name) + END
        self._package_manager.install_package(package_name)
        print OKBLUE + ("%s installed" % package_name) + END
    def update(self, package_name):
        """ The update command.

        :param package_name: name of package to update
        :type package_name: string
        """
        logger.info("Updating %s" % package_name)
        self._package_loader.load()
        self._package_manager.update_package(package_name)
        print OKBLUE + ("%s updated" % package_name) + END
    def remove(self, package_name):
        """ The remove command.

        :param package_name: name of package to remove
        :type package_name: string
        """
        logger.info("Removing %s" % package_name)
        self._package_loader.load()
        self._package_manager.remove_package(package_name)
        print OKGREEN + ("%s removed" % package_name) + END
    
