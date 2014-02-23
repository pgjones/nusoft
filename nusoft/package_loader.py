#!/usr/bin/env python
#
# PackageLoader
#
# Loads the packages from the relevant repos and places them in the package manager.
#
# Author P G Jones - 2014-02-14 <p.g.jones@qmul.ac.uk> : First revision
####################################################################################################
import os
import imp
import logging
logger = logging.getLogger(__name__)

class PackageLoader(object):
    """ Loads nusoft packages from a repository. 

    :param _system: The system
    :param _package_manager: The package manager to load packages into
    """
    def __init__(self, system, package_manager):
        """ Initialises the loader with the current *system* information and a *package manger*

        :param system: 
        :type system:
        """
        self._system = system
        self._package_manager = package_manager
        self._repositories = {}
        logger.debug("The system repository location is %s" % self._system.get_repositories_path())
        for dir in os.listdir(self._system.get_repositories_path()):
            location = os.path.join(self._system.get_repositories_path(), dir)
            if os.path.isdir(location):
                logger.info("Found %s in system repositories" % dir)
                self._repositories[dir] = location
    def add_repository(self, name, url):
        """ Adds a new repository to nusoft, this doesn't load the packages.
        
        :param name: local name for the repository
        :param url: git repository url
        """
        logger.info("Adding %s with name %s" % (url, name))
        self._repositories[name] = os.path.join(self._system.get_repositories_path(), name)
        self._system.execute_command()
    def update_repository(self, name):
        """ Updates the repository with the local name.
        
        :param name: local name for the repository
        """
        pass
    def load(self):
        """ Load the packages from the repositories. """
        for repository in self._repositories:
            for module in os.listdir(self._repositories[repository]):
                if module[-3:] == '.py':
                    module = imp.load_source(module[:-3], os.path.join(self._repositories[repository],  module))
                    for package in module.versions:
                        self._package_manager.register_package(package(self._system, repository))
                        logger.debug("Loaded package %s" % package.__name__)
