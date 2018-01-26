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
#%option
#% key: pattern
#% description: File name pattern to import
#%end
#%flag
#% key: l
#% description: Link raster data instead of importing
#%end

import os
import sys
import re

import grass.script as gs
from grass.exceptions import CalledModuleError

def import_file(filename, link=False):
    module = 'r.external' if link else 'r.import'
    mapname = os.path.splitext(os.path.basename(filename))[0]
    if link:
        gs.message('Linking <{}>...'.format(mapname))
    else:
        gs.message('Importing <{}>...'.format(mapname))
    try:
        gs.run_command(module, input=filename, output=mapname)
    except CalledModuleError as e:
        pass # error already printed
    
def main():
    input_dir = options['input']
    if not os.path.exists(input_dir):
        gs.fatal('{} not exists'.format(input_dir))

    if options['pattern']:
        filter_p = '.*' + options['pattern'] + '.jp2$'
    else:
        filter_p = r'.*_B.*.jp2$'
    pattern = re.compile(filter_p)
    files = []
    for rec in os.walk(input_dir):
        if not rec[-1]:
            continue

        match = filter(pattern.match, rec[-1])
        if match is None:
            continue

        for f in match:
            import_file(os.path.join(rec[0], f), flags['l'])

    return 0

if __name__ == "__main__":
    options, flags = gs.parser()
    sys.exit(main())
