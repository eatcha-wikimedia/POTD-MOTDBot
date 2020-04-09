# -*- coding: utf-8 -*-
import re
import pywikibot
from datetime import datetime


def get_page_name(what,dateinformat):
    page_name = None
    if what is "MOTD":
        page_name = "Template:Motd/%s" % dateinformat
    if what is "POTD":
        page_name = "Template:Potd/%s" % dateinformat
    return page_name

def main():
    

if __name__ == "__main__":
  try:
    main()
  finally:
    pywikibot.stopme()
