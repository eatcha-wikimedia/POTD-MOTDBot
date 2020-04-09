# -*- coding: utf-8 -*-
import re
import pywikibot
from datetime import datetime, timedelta

SITE = pywikibot.Site()

def informatdate(prev):
    """Current date in yyyy-mm-dd format."""
    return (datetime.utcnow()-timedelta(days=prev)).strftime('%Y-%m-%d')

def get_page_name(what,dateinformat):
    page_name = None
    if what is "MOTD":
        page_name = "Template:Motd/%s" % dateinformat
    if what is "POTD":
        page_name = "Template:Potd/%s" % dateinformat
    return page_name

def get_valid_langs(basepage):
    """returns a list of all language pages that are exists"""
    langs_array = [
        'af', 'am', 'an', 'ar', 'as', 'az',
        'be', 'bg', 'bn', 'br', 'bs',
        'ca', 'cs', 'cy',
        'da', 'de', 'dz',
        'el', 'en', 'eo', 'es', 'et', 'eu',
        'fa', 'fi', 'fo', 'fr',
        'ga', 'gl', 'gu',
        'he', 'hi', 'hr', 'ht', 'hu', 'hy',
        'id', 'is', 'it',
        'ja', 'jv',
        'ka', 'kk', 'km', 'kn', 'ko', 'ku', 'ky',
        'la', 'lb', 'lo', 'lt', 'lv',
        'mg', 'mk', 'ml', 'mn', 'mr', 'ms', 'mt', 'myv',
        'nb', 'ne', 'nl', 'nn', 'no',
        'oc', 'or', 'pa',
        'pl', 'ps', 'pt', 'qu',
        'ro', 'ru', 'rw',
        'se', 'si', 'sk', 'sl', 'sq', 'sr', 'sv', 'sw',
        'ta', 'te', 'th', 'tl', 'tr',
        'ug', 'uk', 'ur',
        'vi', 'vo',
        'wa',
        'xh',
        'zh', 'zh-hans', 'zh-hant', 'zu',
        ]
    existant_lang_pages = []
    for lang in langs_array:
        lang_page_name = basepage + "_(%s)" % lang
        page = pywikibot.Page(
            SITE,
            lang_page_name,
            )
        if page.exists():
            existant_lang_pages.append(lang_page_name)
    return existant_lang_pages

def handle(stuff):
    dateinformat = informatdate(1) # how many days before
    page_name = get_page_name(stuff,dateinformat)
    page = pywikibot.Page(
        SITE,
        page_name,)
    try:
        filename = re.search(r"[Ff]ilename\|(?:1=|)(.*?)\|", page.get()).group(1)
    except Exception as e:
        print(e)
    print("now processing - " , stuff, " - ", filename)
    if page.exists():
        langs_array = get_valid_langs(page_name)
        lang_add_list = []
        for lang in langs_array:
            print(lang)
            lang_page = pywikibot.Page(
                SITE,
                lang,
                )
            try:
                lang_text = re.search(r"[Dd]escription\|(?:1=|)(.*)\|(?:2=[a-z]{2,3}|(?:[a-z]{2,3}))\|", lang_page.get()).group(1)
            except Exception as e:
                print(e)
            lang_add_template = "{{%s|%s}}\n" % (re.search(r"\(([a-z]{2,3})\)",lang).group(1), lang_text)
            lang_add_list.append(lang_add_template)
    for p in lang_add_list:
        print(p)
            
            
        
    

def main():
    day_pages = [
        "POTD",
        "MOTD",
        ]
    for stuff in day_pages:
        handle(stuff)
        
    

if __name__ == "__main__":
  try:
    main()
  finally:
    pywikibot.stopme()
