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

def Notify(UserName,File,What=None):

def commit(old_text, new_text, page, summary):
    """Show diff and submit text to page."""
    out("\nAbout to make changes at : '%s'" % page.title())
    pywikibot.showDiff(old_text, new_text)
    page.put(new_text, summary=summary, watchArticle=True, minorEdit=False)

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

def main():
    potd_page = pywikibot.Page(SITE, get_potd_page_today())
    motd_page = pywikibot.Page(SITE, get_potd_page_today())
    potd_text = potd_page.get()
    motd_text = motd_page.get()
    potd_file = getfile(potd_text)
    motd_file = getfile(motd_text)
    


if __name__ == "__main__":
  try:
    main()
  finally:
    pywikibot.stopme()
