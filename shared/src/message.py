"""A module for creating serialisable messages from simple objects."""

from datetime import datetime
import pickle


class Message:
    """
    A class representing a network message.

    A class which models a single network-ready message formed from a
    simple object.
    """

    def __init__(self, obj, player_id):
        """
        Initialise a Message object.

        :param obj: The object to be stored in the message.
        :param player_id: The id of the player.
        """
        self._obj = obj
        self._id = player_id
        self._type = obj.__class__.__name__
        self._timestamp = datetime.now()

    def __str__(self):
        """Return a String representation of a Message object."""
        return ("<Message obj: '%s' player_id: '%s' type: '%s' timestamp: "
                "'%s'>" %
                (str(self._obj), str(self._id), str(self._type),
                 str(self._timestamp)))

    def serialise(self):
        """
        Serialise Message object to byte string.

        :returns: bytes -- The serialised message value
        """
        return pickle.dumps(self)

    @property
    def obj(self):
        """Return the stored object in this message."""
        return self._obj

    @property
    def id(self):
        """Return the id in this message."""
        return self._id

    @property
    def type(self):
        """Return the type of the object stored in this message."""
        return self._type

    @property
    def timestamp(self):
        """Return the timestamp at which this message was created."""
        return self._timestamp

    @staticmethod
    def deserialise(bytestring):
        """
        Deserialise byte string to Message object.

        :param bytestring: bytes -- The string of bytes to be deserialised
            to a message object.
        """
        return pickle.loads(bytestring)
