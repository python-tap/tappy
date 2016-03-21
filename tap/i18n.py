# Copyright (c) 2016, Matt Layman

import gettext
import os

localedir = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'locale')
translate = gettext.translation('tappy', localedir, fallback=True)
_ = translate.gettext
