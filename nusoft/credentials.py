#!/usr/bin/env python
#
# Credentials
#
# Collates and stores in memory user credentials needed for downloads
#
# Author P G Jones - 2014-03-23 <p.g.jones@qmul.ac.uk> : New file.
####################################################################################################
import getpass
import logging
logger = logging.getLogger(__name__)

class Credentials(object):
    """ Receives and stores credentials.
    
    :param _username: Download username
    :param _password: Download password to go with a username
    :param _token: Instead of username and password use token.
    """
    def __init__(self, token=None):
        """ Initialise the credentials.
        
        :param token: token to use
        """
        self._token = token
        self._username = None
        self._password = None
        if token is not None:
            logger.debug("Using a token")
    def authenticate(self):
        """ Returns either a token or the username and password.

        :return: token or username password tuple.
        """
        if self._token is not None:
            return self._token
        elif self._username is not None:
            return (self._username, self._password)
        else:
            self._username = raw_input("Username:").replace('\n', '')
            self._password = getpass.getpass("Password:").replace('\n', '')
            return (self._username, self._password)
    def reset(self):
        """ Reset the known username and password."""
        self._username = None
        self._password = None
        logger.warning("Username/password has been reset")
