# Copyright (c) 2018, Matt Layman and contributors

import gettext
import os

localedir = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'locale')
translate = gettext.translation('tappy', localedir, fallback=True)
_ = translate.gettext
