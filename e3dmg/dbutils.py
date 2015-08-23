# -*- coding: utf-8 -*-
#
# Copyright © 2015 Hasan Yavuz Özderya
#
# This file is part of ecad-3d-model-generator.
#
# ecad-3d-model-generator is free software: you can redistribute it
# and/or modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation, either version 3 of
# the License, or (at your option) any later version.
#
# ecad-3d-model-generator is distributed in the hope that it will be
# useful, but WITHOUT ANY WARRANTY; without even the implied warranty
# of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with ecad-3d-model-generator.  If not, see
# <http://www.gnu.org/licenses/>.

import importlib, pkgutil, os, inspect
from e3dmg import Generator

def getGenerator(module, name):
    """Returns a single generator from the database.

    `module` : module path of the generator, ex: `qfp.tqfp`
    `name` : name of the generator, ex: `TQFP64`
    """
    mod = importlib.import_module(module)
    generator = getattr(mod, name)
    if isinstance(generator, Generator):
        return {'name':name, 'package':module, 'generator':generator}
    else:
        raise Exception("%s:%s is not a generator!" % (module, name))

def onImportError(name):
    import sys
    from traceback import print_tb
    print("Error importing module %s" % name)
    type, value, traceback = sys.exc_info()
    print_tb(traceback)

def isPackage(module):
    return '__init__' in inspect.getfile(module)

def getAllAt(mpath):
    """Returns a list of generators in given module path.

    `mpath` : module or package path, ex: 'e3dmg.database.qfp.lqfp'
    """
    module = importlib.import_module(mpath)
    r = []
    if isPackage(module):
        wp = pkgutil.walk_packages([mpath.replace('.', '/')],
                                   prefix=mpath+'.',
                                   onerror=onImportError)

        for importer, modname, ispkg in wp:
            if not ispkg:
                smodule = importlib.import_module(modname)
                for name, obj in smodule.__dict__.iteritems():
                    if isinstance(obj, Generator):
                        r.append(dict(package=modname, name=name, generator=obj))

    else:
        for name, obj in module.__dict__.iteritems():
            if isinstance(obj, Generator):
                r.append(dict(package=mpath, name=name, generator=obj))

    return r
