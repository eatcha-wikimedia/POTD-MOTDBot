# -*- coding: utf-8 -*-
import re
import pywikibot
from datetime import datetime, timedelta
#from googletrans import Translator
#translator = Translator()


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

def out(text, newline=True, date=False, color=None):
    """Just output some text to the consoloe or log."""
    if color:
        text = "\03{%s}%s\03{default}" % (color, text)
    dstr = (
        "%s: " % datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
        if date
        else ""
    )
    pywikibot.stdout(
        "%s%s" % (dstr, text),
        newline=newline,
        )

def commit(old_text, new_text, page, summary):
    """Show diff and submit text to the wiki server."""
    out("\nAbout to make changes at : '%s'" % page.title())
    pywikibot.showDiff(old_text,new_text,)
    page.put(new_text,summary=summary,watchArticle=True,minorEdit=False,)

def add_to_file(filename,list_of_lang_templates,stuff,template_name):
    page = pywikibot.Page(
        SITE,
        filename,
        )
    old_text = page.get()
    try:
        desc_text = re.search(r"\|[Dd]escription(?:\s*?)=(?:\s*?)([\s\S]*?)\n(?:\s*?)\|",old_text).group(1)
    except AttributeError:
        return
    text_to_append = ""
    for template in list_of_lang_templates:
        text_to_append = "%s\n%s" % (text_to_append,template)
    updated_desc = desc_text + text_to_append
    new_text = old_text.replace(desc_text,updated_desc)
    if old_text == new_text:
        out("nothing new to add")
        return
    summary = "Adding descriptions from [[%s|%s]] template." % (template_name,stuff)
    commit(old_text, new_text, page, summary)

def detectUnIdentifedlangs(text):
    regex = r"description(?:\s*)=(?:\s*)({{[\s\S]*?}})\n(?:\s*)\|"
    try:
        text_to_remove = re.search(regex,text).group(1)
    except:
        text_to_remove = ""
    without_identfied_langs = re.sub(text_to_remove,"",text)

def checkIfTemplatePresent(langcode,text):
    regex = "{{(?:\s*)%s(?:\s*)\|" % langcode

    try:
        re.search(regex,text).group()
    except:
        return False
    return True

def handle(stuff,num):

    dateinformat = informatdate(num) # how many days before
    page_name = get_page_name(stuff,dateinformat)
    page = pywikibot.Page(
        SITE,
        page_name,)
    try:
        filename = "File:"+re.search(r"[Ff]ilename\|(?:1=|)(.*?)\|", page.get()).group(1)
    except Exception as e:
        out(e,color="red")
    if pywikibot.Page(SITE,filename,).isRedirectPage():
        filename = pywikibot.Page(SITE,filename,).getRedirectTarget().title()
    out("now processing - " + stuff + " - " + filename,color="green")
    if page.exists():
        langs_array = get_valid_langs(page_name)
        lang_add_list = []
        for lang in langs_array:
            out(lang,color="white")
            lang_page = pywikibot.Page(
                SITE,
                lang,
                )
            try:
                lang_text = re.search(r"[Dd]escription\|(?:1=|)(.*)(?:\n|)\|(?:2=[a-z]{2,3}|(?:[a-z]{2,3}))\|", lang_page.get() , flags=re.MULTILINE).group(1)
            except Exception as e:
                out(e,color="red")
                return
            lang_add_template = "{{%s|%s}}" % (re.search(r"\(([a-z]{2,3})\)",lang).group(1), lang_text)
            if not checkIfTemplatePresent(re.search(r"\(([a-z]{2,3})\)",lang).group(1), pywikibot.Page(SITE,filename,).get()):
                lang_add_list.append(lang_add_template)
            else:
                continue
    add_to_file(filename,lang_add_list,stuff,page_name)


def main():
    day_pages = [
        "POTD",
        "MOTD",
        ]

    for num in range(85,5648):
        for stuff in day_pages:
            handle(stuff,num)
        
    

if __name__ == "__main__":
  try:
    main()
  finally:
    pywikibot.stopme()
