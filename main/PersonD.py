"""Class Person."""


class PersonD(object):
    """
    Person Object to insert
    """

    def __init__(self):
        """

        :return:
        """
        self.id = None
        self._name = None

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name):
        self._name = name