__author__ = 'gogasca'


class PortNotOpened(Exception):
    def __init__(self, value):
        self.value = value
        self.code = 5

    def __str__(self):
        return repr(self.value)


class InvalidParameter(Exception):
    def __init__(self, value):
        self.value = value
        self.code = 6

    def __str__(self):
        return repr(self.value)


class InvalidPassword(Exception):
    def __init__(self, value):
        self.value = value
        self.code = 7

    def __str__(self):
        return repr(self.value)


class InvalidUserName(Exception):
    def __init__(self, value):
        self.value = value
        self.code = 8

    def __str__(self):
        return repr(self.value)


class InvalidHostName(Exception):
    def __init__(self, value):
        self.value = value
        self.code = 9

    def __str__(self):
        return repr(self.value)


class InvalidPort(Exception):
    def __init__(self, value):
        self.value = value
        self.code = 10

    def __str__(self):
        return repr(self.value)


class ConnectivityError(Exception):
    def __init__(self, value):
        self.value = value
        self.code = 11

    def __str__(self):
        return repr(self.value)


class UndefinedDataStore(Exception):
    def __init__(self, value):
        self.value = value
        self.code = 12

    def __str__(self):
        return repr(self.value)


class NoDataStoreDefined(Exception):
    def __init__(self, value):
        self.value = value
        self.code = 13

    def __str__(self):
        return repr(self.value)


class InvalidTemplateParameter(Exception):
    def __init__(self, value):
        self.value = value
        self.code = 14

    def __str__(self):
        return repr(self.value)


class ParameterNotFoundInTemplate(Exception):
    def __init__(self, value):
        self.value = value
        self.code = 15

    def __str__(self):
        return repr(self.value)


class InvalidConfigurationFile(Exception):
    def __init__(self, value):
        self.value = value
        self.code = 16

    def __str__(self):
        return repr(self.value)


class InvalidDirectoryPath(Exception):
    def __init__(self, value):
        self.value = value
        self.code = 17

    def __str__(self):
        return repr(self.value)


class UndefinedDirectory(Exception):
    def __init__(self, value):
        self.value = value
        self.code = 18

    def __str__(self):
        return repr(self.value)


class CreateDirectoryFailure(Exception):
    def __init__(self, value):
        self.value = value
        self.code = 19

    def __str__(self):
        return repr(self.value)


class SSHConnectivityError(Exception):
    def __init__(self, value):
        self.value = value
        self.code = 20

    def __str__(self):
        return repr(self.value)


class HTTPSConnectivityError(Exception):
    def __init__(self, value):
        self.value = value
        self.code = 21

    def __str__(self):
        return repr(self.value)


class InvalidProvider(Exception):
    def __init__(self, value):
        self.value = value
        self.code = 22

    def __str__(self):
        return repr(self.value)


class SendSCPException(Exception):
    def __init__(self, value):
        self.value = value
        self.code = 23

    def __str__(self):
        return repr(self.value)


class FirewallException(Exception):
    def __init__(self, value):
        self.value = value
        self.code = 24

    def __str__(self):
        return repr(self.value)


class DBReadException(Exception):
    def __init__(self, value):
        self.value = value
        self.code = 25

    def __str__(self):
        return repr(self.value)


class DiscoveryException(Exception):
    def __init__(self, value):
        self.value = value
        self.code = 26

    def __str__(self):
        return repr(self.value)


class InvalidHostRequest(Exception):
    def __init__(self, value):
        self.value = value
        self.code = 27

    def __str__(self):
        return repr(self.value)


class InvalidInstanceRequest(Exception):
    def __init__(self, value):
        self.value = value
        self.code = 28

    def __str__(self):
        return repr(self.value)


class InvalidCampaignRequest(Exception):
    def __init__(self, value):
        self.value = value
        self.code = 29

    def __str__(self):
        return repr(self.value)


class InvalidCredentials(Exception):
    def __init__(self, value):
        self.value = value
        self.code = 30

    def __str__(self):
        return repr(self.value)


class DatabaseConnectivity(Exception):
    def __init__(self, value):
        self.value = value
        self.code = 31

    def __str__(self):
        return repr(self.value)


class DatabaseParameters(Exception):
    def __init__(self, value):
        self.value = value
        self.code = 32

    def __str__(self):
        return repr(self.value)


class ImageDownloadException(Exception):
    def __init__(self, value):
        self.value = value
        self.code = 33

    def __str__(self):
        return repr(self.value)


__version__ = '0.1'
