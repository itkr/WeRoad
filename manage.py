#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import codecs

import scripts


def proxy(script_name, argv):
    if hasattr(scripts, script_name):
        main_module = getattr(scripts, script_name)
        if hasattr(main_module, "main"):
            main_script = getattr(main_module, "main")
            main_script(argv)


def main():
    sys.stdout = codecs.getwriter('utf8')(sys.stdout)
    site_root = os.path.dirname(os.path.realpath(__file__))
    argv = sys.argv
    proxy(argv[1], argv[2:])


if __name__ == '__main__':
    main()