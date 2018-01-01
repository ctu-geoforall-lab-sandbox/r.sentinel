#!/usr/bin/env python2
#
############################################################################
#
# MODULE:      r.sentinel.import
# AUTHOR(S):   Martin Landa
# PURPOSE:     Imports Sentinel data downloaded from Copernicus Open Access Hub
#              using r.sentinel.download.
# COPYRIGHT:   (C) 2018 by Martin Landa, and the GRASS development team
#
#              This program is free software under the GNU General Public
#              License (>=v2). Read the file COPYING that comes with GRASS
#              for details.
#
#############################################################################

#%Module
#% description: Imports Sentinel data downloaded from Copernicus Open Access Hub using r.sentinel.download.
#% keyword: raster
#% keyword: imagery
#% keyword: sentinel
#% keyword: import
#%end
#%option G_OPT_M_DIR
#% key: input
#% description: Name for input directory where downloaded Sentinel data lives
#% required: yes
#%end
#%flag
#% key: l
#% description: Link raster data instead of importing
#%end

import os
import sys
import re

import grass.script as gs

def import_file(filename, link=False):
    module = 'r.external' if link else 'r.import'
    mapname = os.path.splitext(os.path.basename(filename))[0]
    gs.run_command(module, input=filename, output=mapname)
    
def main():
    input_dir = options['input']
    if not os.path.exists(input_dir):
        gs.fatal('{} not exists'.format(input_dir))

    pattern = re.compile(r'.*_B.*.jp2$')
    files = []
    for rec in os.walk(input_dir):
        if not rec[-1]:
            continue

        match = filter(pattern.match, rec[-1])
        if match:
            for f in match:
                gs.message('Importing <{}>...'.format(f))
                import_file(os.path.join(rec[0], f), flags['l'])

                
    return 0

if __name__ == "__main__":
    options, flags = gs.parser()
    sys.exit(main())
