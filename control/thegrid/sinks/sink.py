"""
sink.py

The base class and API for sink code to interact with the control core.
"""

import logging
logger = logging.getLogger(__name__)

loaded_sinks = {}


def register_sink(name):
    """
    Use this decorator to register a new sink.
    Name is used for the global name list.
    """
    def wrapper(sink):
        loaded_sinks[name] = sink
        logger.info("Registered sink {}".format(name))
        return sink
    return wrapper


class Sink:
    """
    Sink classes are responsible for receiving a new grid state as a 7x7 numpy
    boolean array, and updating their outputs appropriately.

    Their lifetime is the same as the control application.
    """

    def update(state):
        """
        This function will be called with a new grid state on an irregular
        basis, whenever an update is ready.
        """
        raise NotImplementedError
