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
from shotfactory04.inifile import IniFile


class Gui(base.Gui):
    """
    Special functions for Opera.
    """

    def reset_browser(self):
        """
        Reset crashed state and delete browser cache.
        """
        home = os.environ['HOME'].rstrip('/')
        inifile = home + '/.opera/opera6.ini'
        if os.path.exists(inifile):
            print 'removing crash dialog from', inifile
            ini = IniFile(inifile)
            ini.set('State', 'Run', 0)
            ini.set('User Prefs', 'Show New Opera Dialog', 0)
            ini.save()
        cachedir = os.path.join(home, '.opera/cache4')
        if not os.path.exists(cachedir):
            return
        if os.path.exists(cachedir):
            print 'deleting cache', cachedir
            shutil.rmtree(cachedir)
        cachedir = os.path.join(home, '.opera/opcache')
        if not os.path.exists(cachedir):
            return
        if os.path.exists(cachedir):
            print 'deleting cache', cachedir
            shutil.rmtree(cachedir)