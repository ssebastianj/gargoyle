#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function, unicode_literals

import glob
import shutil
import sys
import os

PY2 = sys.version_info[0] == 2
if not PY2:
    text_type = str
    string_types = (str,)
    unichr = chr

    def u(s):
        return s

    def b(s):
        return s.encode('utf-8')
else:
    text_type = unicode
    string_types = (str, unicode)
    unichr = unichr

    def u(s):
        return unicode(s, 'unicode_escape')

    def b(s):
        return s

tran_type = ''
active_lang = ''
root_dir = par_dir = os.path.dirname(os.path.dirname(
                                     os.path.dirname(
                                     os.path.abspath(__file__))))

if len(sys.argv) == 2 and sys.argv[1] == 'localize':
    tran_type=sys.argv[1]
elif len(sys.argv) == 3 and sys.argv[1] == 'internationalize':
    tran_type=sys.argv[1]
    active_lang=sys.argv[2]
else:
    sys.stderr.write('Usage: {0} localize\n'.format(sys.argv[0]))
    sys.stderr.write('  example: {0} internationalize English-EN\n'.format(sys.argv[0]))
    sys.exit(1)

# if localize, ensure hidden .config file is devoid of i18n
# if internationalize, ensure the hidden .config file contains plugin-gargoyle-i18n and the target language package
# if os.path.exists('./package/plugin-gargoyle-i18n/files/etc/uci-defaults/zzz-plugin-gargoyle-i18n'):
for config_file in glob.glob('./*-src/.config'):
    # there should be only one
    if tran_type == 'internationalize':
        print('Editing config file to build in {0} translation\n'.format(active_lang))

    with open(config_file, 'rb') as cfg_fileFO:
        cfg_doc=cfg_fileFO.readlines()

    newcfg_doc = []
    for cline in cfg_doc:
        anewline = ''

		if (cline.startswith('CONFIG_PACKAGE_plugin-gargoyle-i18n') or cline.startswith('CONFIG_PACKAGE_gargoyle-i18n')) and tran_type=='localize' :
            anewline = '# ' + cline
		if (cline.startswith('CONFIG_PACKAGE_plugin-gargoyle-i18n') or cline.startswith('CONFIG_PACKAGE_gargoyle-i18n')) and tran_type=='internationalize' :
            # sorry, but I'm sure your some slick brotha and you've got mad dope skillz, but...
            anewline= '# ' + cline
		if cline.startswith('CONFIG_PACKAGE_haserl-i18n') and tran_type=='localize' :
			anewline='CONFIG_PACKAGE_haserl=y\n'

        if anewline != '':
            newcfg_doc.append(anewline)
        else:
            newcfg_doc.append(cline)

    if tran_type == 'internationalize':
        newcfg_doc.append('#\n')
        newcfg_doc.append('# Gargoyle I18N\n')
        newcfg_doc.append('#\n')
        newcfg_doc.append('\n')
		newcfg_doc.append('CONFIG_PACKAGE_gargoyle-i18n=y\n')

        found_lang = False
        search_path = os.path.join(root_dir,
                                  'package',
                                  'plugin-gargoyle-i18n-*',
                                  'files',
                                  'www',
                                  'i18n',
                                  '*')

        for langpack in glob.glob(search_path):
            lang = os.path.basename(langpack)

            if lang == active_lang:
                found_lang = True
                newcfg_doc.append('CONFIG_PACKAGE_plugin-gargoyle-i18n-{0}=y\n'.format(lang))
            else:
                newcfg_doc.append('CONFIG_PACKAGE_plugin-gargoyle-i18n-{0}=m\n'.format(lang))

        newcfg_doc.append('\n')

        if not found_lang:
            sys.stderr.write('finalize was unable to find the target language\n')
            sys.exit(1)

    with open(config_file, 'wb') as cfg_fileFO:
        cfg_fileFO.seek(0)
        cfg_fileFO.writelines(newcfg_doc)

