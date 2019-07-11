"""This module contains helper functions for reading/writing netCDF files
"""


def walktree(top):
    """
    The function walktree is a Python generator that is used to walk the directory tree

    :return: All children groups within a netCDF file
    :rtype: Python array
    """
    values = top.groups.values()
    yield values
    for value in top.groups.values():
        for children in walktree(value):
            yield children
