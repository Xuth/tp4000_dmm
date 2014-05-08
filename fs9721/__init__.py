try:
    from .client import Client
except ImportError:
    # We need to allow this to be OK if we are going to
    # import __version__ from setup.
    pass


__version__ = '1.0'
