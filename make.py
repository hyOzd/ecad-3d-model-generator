#!/usr/bin/python
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

# This is the main generator script for component models.
#
# Run `./make.py --help` for usage instructions.

from e3dmg.exporters import export
from e3dmg.dbutils import getGenerator, getAllAt
import sys, argparse, os

def initParser():
    """Initializes and returns argument parser."""
    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter, # do not re-format epilog and description
        description="Create 3D models of electronic components in various formats.",
        epilog="""

  * if no output type is specified all types are enabled by default
  ** --s_vrml option should produce a smaller VRML file but its features are limited
  *** --vrml and --s_vrml can't be selected at the same time

Examples:

List all generators in the database:
    %(prog)s --list-all

List some generators in the database:
    %(prog)s --list qfp.tqfp

Create a certain model:
    %(prog)s qfp.tqfp:tqfp5x5x5

Create models for all components:
    %(prog)s all

Create STEP files for all components:
    %(prog)s --step all
        """)
    parser.add_argument('--list-all', action='store_true',
                        help="list all database")
    parser.add_argument('--list', metavar='MODULE',
                        help="list generators under given module path")
    parser.add_argument('--step', action='store_true',
                        help="generate a STEP file")
    parser.add_argument('--vrml', action='store_true',
                        help="generate a VRML file")
    parser.add_argument('--s_vrml', action='store_true',
                        help="generate a VRML file using simple exporter")
    parser.add_argument('--x3d', action='store_true',
                        help="generate a X3D file")
    parser.add_argument('--freecad', action='store_true',
                        help="generate a FreeCAD file")
    parser.add_argument('--dont-fuse', action='store_true',
                        help="do not fuse model to a single part/mesh")
    parser.add_argument('--outdir', default='./output',
                        help="output directory of models")
    parser.add_argument('--scale', default=None, type=float,
                        help="scale output model")
    parser.add_argument('component', nargs='?',
                        help="component model to generate or 'all'")
    return parser

def listDatabase(module=None):
    """Prints a list of all component generators in database."""
    if not module:
        module = 'e3dmg.database'
    else:
        module = 'e3dmg.database.' + module

    for cg in getAllAt(module):
        print(cg['package'].split('e3dmg.database.')[1] + ':' + cg['name'])

def makeOne(args, name, generator, package):
    """
    `args` : argument parser result
    `name` : name of the component
    `generator` : generator object
    `package` : component database path
    """
    print("Making %s:%s..." % (package, name))
    model = generator.generate()

    # create output directory if it doesn't exist
    odir = os.path.abspath(args.outdir)
    odir = '/'.join(odir.split('/') + package[len('e3dmg.database.'):].split('.'))
    if not os.path.exists(odir):
        os.makedirs(odir)

    fname = odir+'/'+name
    fuse = not args.dont_fuse
    if args.step:
        export("STEP", name, model, fname+'.step', fuse, args.scale)
    if args.vrml:
        export("VRML", name, model, fname+'.wrl', fuse, args.scale)
    if args.s_vrml:
        export("S_VRML", name, model, fname+'.wrl', fuse, args.scale)
    if args.x3d:
        export("X3D", name, model, fname+'.x3d', fuse, args.scale)
    if args.freecad:
        export("FREECAD", name, model, fname+'.fcstd', fuse, args.scale)
    print("Done %s:%s..." % (package, name))

def make(args):
    component = args.component
    if component == 'all': # make whole database
        generators = getAllAt('e3dmg.database')
    elif not (':' in component): # make sub package/path
        generators = getAllAt('e3dmg.database.' + component)
    else: # make single component
        module, part = component.split(':')
        generators = [getGenerator('e3dmg.database.' + module, part)]

    for g in generators:
        makeOne(args, g['name'], g['generator'], g['package'])

def run():
    parser = initParser()
    args = parser.parse_args()

    # check arguments
    if args.vrml and args.s_vrml:
        raise Exception("VRML and Simple VRML exporters cannot be selected at the same time!")

    # select all file types if none selected
    if not (args.step or args.vrml or args.s_vrml or args.x3d or args.freecad):
        args.step = True
        args.vrml = True
        args.s_vrml = False
        args.x3d = True
        args.freecad = True

    if args.list_all:
        listDatabase()
        return
    elif args.list:
        listDatabase(args.list)
        return
    elif args.component:
        make(args)
    else:
        parser.error("Provide a component name/module to create!")

if __name__ == "__main__":
    run()
