# browsershots.org - Test your web design in different browsers
# Copyright (C) 2007 Johann C. Rocholl <johann@browsershots.org>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place - Suite 330, Boston,
# MA 02111-1307, USA.

"""
GUI-specific interface functions for X11.
"""

__revision__ = "$Rev$"
__date__ = "$Date$"
__author__ = "$Author$"


import os
import time
import shutil
from shotfactory04.gui import linux as base


class Gui(base.Gui):
    """
    Special functions for Galeon.
    """

    def reset_browser(self):
        """
        Delete crash file and browser cache.
        """
        home = os.environ['HOME'].rstrip('/')
        crashfile = home + '/.galeon/session_crashed.xml'
        if os.path.exists(crashfile):
            print 'deleting crash file', crashfile
            os.unlink(crashfile)
        dotdir = os.path.join(home, '.galeon/mozilla')
        if not os.path.exists(dotdir):
            return
        for profile in os.listdir(dotdir):
            # Delete cache
            cachedir = os.path.join(dotdir, profile, 'Cache')
            if os.path.exists(cachedir):
                print 'deleting cache', cachedir
                shutil.rmtree(cachedir)