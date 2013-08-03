#!/usr/bin/env python
    # -*- coding: utf-8 -*-

from __future__ import print_function, unicode_literals

import os
import shutil
import sys


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

act_lang = ''
root_dir = par_dir = os.path.dirname(os.path.dirname(
                                     os.path.dirname(
                                     os.path.abspath(__file__))))

if len(sys.argv) == 2:
    act_lang = sys.argv[1]
    menu_path = os.path.join(root_dir,
                            'package',
                            'plugin-gargoyle-i18n-{0}'.format(act_lang),
                            'files',
                            'www',
                            'i18n'
                            '{1}'.format(act_lang),
                            'menus.txt')

    if not os.path.exists(menu_path):
        print('Error: target language package not found.')
        sys.exit(1)
else:
    sys.stderr.write('Usage: {0} active_language\n'.format(sys.argv[0]))
    sys.stderr.write('  example: {0} English-EN\n'.format(sys.argv[0]))

pkg_dir = os.path.join(root_dir, 'package')
pkg_orig_dir = os.path.join(root_dir, 'package-orig')
shutil.copytree(pkg_dir, pkg_orig_dir)

i18n_path = os.path.join(root_dir,
                         'package',
                         'plugin-gargoyle-i18n',
                         'files',
                         'etc',
                         'uci-defaults',
                         'zzz-plugin-gargoyle-i18n')

if os.path.exists(i18n_path):
    print('Setting target language')

    with open(i18n_path, 'rb') as uci_fileFO:
        ucipage=uci_fileFO.readlines()
        new_ucipage_contents=[]

    for uciline in ucipage:
        anewline = ''

        if uciline.startswith(bytearray(b'uci set gargoyle.global.fallback_lang')):
            anewline = u('uci set gargoyle.global.fallback_lang={0}\n'.format(act_lang))
        if uciline.startswith(bytearray(b'uci set gargoyle.global.language')):
            anewline = u('uci set gargoyle.global.language={0}\n'.format(act_lang))
        if uciline.startswith(bytearray(b'change_menu_language')):
            anewline = u('change_menu_language "{0}"\n'.format(act_lang))

        if anewline != '':
            new_ucipage_contents.append(anewline)
        else:
            new_ucipage_contents.append(uciline)

    with open(i18n_path, 'wb') as out_uci_fileFO:
        out_uci_fileFO.seek(0)
        out_uci_fileFO.writelines(new_ucipage_contents)
else:
    print('ERROR: the default language settings cannot be set. Pages will not render.')
    sys.exit(1)
