#!/usr/bin/env python
#
# PackageManager
#
# Manages the packages on the system, installs, removes and updates.
#
# Author P G Jones - 2014-02-08 <p.g.jones@qmul.ac.uk> : First revision
####################################################################################################
import types
import logging
logger = logging.getLogger(__name__)

class PackageManager(object):
    """ Manages a dictionary of packages for installation on the system.

    :param _packages: packages keyed by package name
    :type _packages: dictionary string and :class:`nusoft.package`
    """
    def __init__(self):
        """ Initialise"""
        self._packages = {} 
    def register_package(self, package):
        """ Register a *package* in this manager

        :param package: package to register
        :type package: :class:`package.package.Package` instance
        """
        logger.debug("Registering %s package" % package.get_name())
        if package.get_name() in self._packages:
            logger.warn("Package %s already registered, replacing package from %s with package from %s." % 
                        (package.get_name(), self._packages[package].get_name(), package.get_repository()))
        package.check_state()
        self._packages[package.get_name()] = package
    def packages(self):
        """ Yields a package name, package instance tuple.

        :return: tuple name and :class:`package.package.Package` instance
        """
        for package_name in self._packages:
            yield (package_name, self._packages[package_name])
    def get_package(self, package_name):
        """ Return the package with a name equal to *package_name*

        :param package_name: name of the package
        :return: the installed package
        :rtype: :class:`nusoft.package.Package` instance
        """
        try:
            return self._packages[package_name]
        except KeyError:
            logger.exception("Package %s does not exist" % package_name, exc_info=True)
            raise
####################################################################################################
    # Functions that act on single packages
    def install_all(self):
        """ Install all the packages."""
        logger.info("Installing all packages")
        for package in self._packages:
            if not package.is_installed():
                self._install_package(package)
    def update_all(self):
        """ Update all the packages."""
        logger.info("Updating all packages")
        for package in self._packages:
            if not package.is_installed():
                self._update_package(package)
    def remove_all(self):
        """ Remove all the packages."""
        logger.info("Removing all packages")
        for package in self._packages:
            if not package.is_installed():
                self._remove_package(package, True) # Force remove
####################################################################################################
    # Functions that act on single packages
    def install_package_dependencies(self, package_name):
        """ Install the dependencies of the package with name equal to *package_name*

        :param package_name: name of the package of which dependencies should be installed
        """
        package = self.get_package(package_name)
        self._install_package_dependencies(package)
    def install_package(self, package_name):
        """ Install the package with a name equal to *package_name*

        :param package_name: name of the package to install
        :return: the installed package
        :rtype: :class:`nusoft.package.Package` instance
        """
        package = self.get_package(package_name)
        return self._install_package(package)
    def update_package(self, package_name):
        """ Update the package with a name equal to *package_name*

        :param package_name: name of the package to update
        :return: the installed package
        :rtype: :class:`nusoft.package.Package` instance
        """
        package = self.get_package(package_name)
        return self._update_package(package)
    def remove_package(self, package_name, force=False):
        """ Remove the package with a name equal to *package_name*

        This will check if the package has dependents and not remove if it does, unless *force* is 
        True.

        :param package_name: name of the package to remove
        """
        package = self.get_package(package_name)
        return self._remove_package(package, force)
####################################################################################################
    # Internal functions
    def _install_package_dependencies(self, package):
        """ Install the dependencies of the package

        :param package: package to install
        :types package: dictionary string key to :class:`nusoft.package.Package`
        """
        installed_dependencies = {}
        for dependency_name in package.get_dependencies():
            # First need to check if dependency is installed, if dependency is a list should check
            # at least one is installed.
            if isinstance(dependency_name, types.ListType): # Multiple optional dependencies
                for optional_dependency_name in dependency_name:
                    optional_dependency = self.get_package(optional_dependency_name)
                    if optional_dependency.is_installed(): # Great found one!
                        installed_dependencies[optional_dependency_name] = optional_dependency
                        break
                else: # No optional dependency is installed, thus install the first
                    dependency = self.get_package(dependency_name[0])
                    installed_dependencies[dependency_name[0]] = self._install_package(dependency)
            else: # Just a single dependency
                dependency = self.get_package(dependency_name)
                if dependency.is_installed():
                    installed_dependencies[dependency_name] = dependency
                else: # Must install it
                    installed_dependencies[dependency_name] = self._install_package(dependency)
        return installed_dependencies
    def _install_package(self, package):
        """ Install the package

        :param package: package to install
        :types package: :class:`nusoft.package.Package` instance
        :return: the installed package
        :rtype: :class:`nusoft.package.Package` instance
        """
        if package.is_installed():
            return package
        dependencies = self._install_package_dependencies(package)
        package.set_dependencies(dependencies)
        try:
            package.install()
        except Exception as e:
            logger.exception("Installation fail.", exc_info=True)
            raise Exception("Failed to install " + package.get_name() + " see log for details")
        package.check_state()
        return package        
    def _update_package(self, package):
        """ Update the package

        :param package: package to update
        :type package: :class:`nusoft.package.Package` instance
        :return: the installed package
        :rtype: :class:`nusoft.package.Package` instance
        """
        if not package.is_installed():
            raise
        dependencies = self._install_package_dependencies(package)
        package.set_dependencies(dependencies)
        package.update()
        package.check_state()
        for dependent in self._package_dependents(package):
            self._update_package(dependent)
        return package        
    def _remove_package(self, package, force):
        """ Remove the *package*

        This will check if the package has dependents and not remove if it does, unless *force* is 
        True.

        :param package: package to remove
        """
        if not package.is_installed():
            raise Exception("Package is not installed.")
        if force:
            package.remove()
        else:
            if len(self._package_dependents(package)) == 0:
                package.remove()
            else:
                raise Exception("Package has dependents.")
    def _package_dependents(self, package):
        """ Yield the name of any packages that are dependent on *package*

        :param package: package to find dependent package for
        :type package: :class:`nusoft.package.Package` instance
        :return: list of dependent pacakges
        :rtype: list of :class:`nusoft.package.Package` instances
        """
        dependents = []
        for test_name in self._packages:
            test_package = self._packages[test_name]
            # If test package has this package as a dependency then update the test package
            for dependency in test_package.get_dependencies():
                if isinstance(dependency, types.ListType): # deal with optional dependencies
                    if package.get_name() in dependency:
                        dependents.append(test_package)
                elif dependency == package.get_name():
                    dependents.append(test_package)
        return dependents

