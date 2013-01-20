# coding: utf-8
import os.path
import gettext

TRANSLATION_DOMAIN = "despertador"
LOCALE_DIR = os.path.join(os.path.dirname(__file__), "locale")

gettext.install(TRANSLATION_DOMAIN, LOCALE_DIR)
_ = gettext.gettext
