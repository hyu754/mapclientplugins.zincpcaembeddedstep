
"""
MAP Client Plugin
"""

__version__ = '0.1.0'
__author__ = 'hyu754'
__stepname__ = 'zincpcaembedded'
__location__ = ''

# import class that derives itself from the step mountpoint.
from mapclientplugins.zincpcaembeddedstep import step

# Import the resource file when the module is loaded,
# this enables the framework to use the step icon.
from . import resources_rc