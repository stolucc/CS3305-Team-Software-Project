"""Polling Object."""


class Poll:
    """Class to represent a poll request."""

    def __init__(self, last_known):
        """
        Create base poll object.

        :param last_known: Last known action.
        """
        self._last_known = last_known
        self._eventQueue = None
        self._textQueue = None

    @property
    def eventQueue(self):
        """Getter for eventQueue."""
        return self._eventQueue

    @eventQueue.setter
    def eventQueue(self, queue):
        self._eventQueue = queue

    @property
    def textQueue(self):
        """Getter for textQueue."""
        return self._eventQueue

    @textQueue.setter
    def textQueue(self, queue):
        self._textQueue = queue
