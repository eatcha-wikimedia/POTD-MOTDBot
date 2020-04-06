import pywikibot
import re, datetime

TODAY = datetime.datetime.utcnow()
SITE = pywikibot.Site()

def informatdate():
    return (TODAY).strftime('%Y-%m-%d')

def get_motd_page_today():
    return 'Template:Motd/%s' % informatdate()

def get_potd_page_today():
    return 'Template:Potd/%s' % informatdate()

def getfile(text):
    return ("File:"+re.search(r"{{(?:\s*)[MmPp]otd(?:[_\s\-]|)[Ff]ilename(?:\s*)\|(?:1=|)(.*?)\|", text).group(1))

def commit(old_text, new_text, page, summary):
    """Show diff and submit text to page."""
    out("\nAbout to make changes at : '%s'" % page.title())
    pywikibot.showDiff(old_text, new_text)
    #page.put(new_text, summary=summary, watchArticle=True, minorEdit=False)

def out(text, newline=True, date=False, color=None):
    """Just output some text to the consoloe or log."""
    if color:
        text = "\03{%s}%s\03{default}" % (color, text)
    dstr = (
        "%s: " % datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
        if date
        else ""
    )
    pywikibot.stdout("%s%s" % (dstr, text), newline=newline)

def tagPOTD(filename):
    page = pywikibot.Page(SITE, filename)
    

def tagMOTD(filename):
    page = pywikibot.Page(SITE, filename)


def main():
    potd_file = getfile(pywikibot.Page(SITE, get_potd_page_today()).get())
    motd_file = getfile(pywikibot.Page(SITE, get_motd_page_today()).get())
    try:
        tagPOTD(potd_file)
    except:
        pass
    try:
        tagPOTD(motd_file)
    except:
        pass
    
    




if __name__ == "__main__":
  try:
    main()
  finally:
    pywikibot.stopme()
