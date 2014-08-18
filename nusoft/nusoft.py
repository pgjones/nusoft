#!/usr/bin/env python
#
# Nusoft
#
# Executes user actions
#
# Author P G Jones - 2014-08-15 <p.g.jones@qmul.ac.uk> : New file.
####################################################################################################
import system.standard
import system.mac
import package_manager
import package_loader
import re
import logging
import os
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
        if os.uname()[0] == "Darwin":
            logger.info("Using Mac system")
            self._system = system.mac.Mac(install_path)
        else:
            logger.info("Using Standard system")
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
        """ This installs the package *package_name*

        :param package_name: name of package to install
        :type package_name: string
        """
        logger.info("Installing %s" % package_name)
        self._package_loader.load()
        print HEADER + ("Installing %s" % package_name) + END
        try:
            self._package_manager.install_package(package_name)
            print OKBLUE + ("%s installed" % package_name) + END
        except Exception, error:
            print FAIL + "Installation failed" + END
            print error
    def update(self, package_name):
        """ This updates the package *package_name*

        :param package_name: name of package to update
        :type package_name: string
        """
        logger.info("Updating %s" % package_name)
        self._package_loader.load()
        try:
            self._package_manager.update_package(package_name)
            print OKBLUE + ("%s updated" % package_name) + END
        except Exception, error:
            print FAIL + "Cannot update package " + package_name + END
            print error
    def remove(self, package_name):
        """ This removes the package *package_name*

        :param package_name: name of package to remove
        :type package_name: string
        """
        logger.info("Removing %s" % package_name)
        self._package_loader.load()
        try:
            self._package_manager.remove_package(package_name)
            print OKGREEN + ("%s removed" % package_name) + END
        except Exception, error:
            print FAIL + "Cannot remove package " + package_name + END
            print error
    def query(self, package_name):
        """ This queries the package *package_name*.

        It outputs useful infomration about the package

        :param package_name: name of package to query
        :type package_name: string
        """
        logger.info("Querying %s" % package_name)
        self._package_loader.load()
        try:
            package = self._package_manager.get_package(package_name)
            if package.is_installed():
                print OKBLUE + ("%s from %s is installed" % (package.get_name(), package.get_repository())) + END
                return # Nothing else to say
            print HEADER + ("%s is not installed and requires the following dependencies" % package_name) + END
            for dependency in package.get_dependencies():
                dependency_package = self._package_manager.get_package(dependency)
                if dependency_package.is_installed():
                    print OKBLUE + ("%s from %s is installed" % (dependency, dependency_package.get_repository())) + END
                else:
                    print ("%s from %s is known" % (dependency, dependency_package.get_repository()))
        except Exception, error:
            print FAIL + "Cannot query package " + package_name + END
            print error
