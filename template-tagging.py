import pywikibot
import re
from datetime import timedelta,datetime

TODAY = datetime.datetime.utcnow()
SITE = pywikibot.Site()

def informatdate():
    return (TODAY+timedelta(2)).strftime('%Y-%m-%d')

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
    page.put(new_text, summary=summary, watchArticle=True, minorEdit=False)

def out(text, newline=True, date=False, color=None):
    """Just output some text to the consoloe or log."""
    if color:
        text = "\03{%s}%s\03{default}" % (color, text)
    dstr = (
        "%s: " % TODAY.strftime("%Y-%m-%d %H:%M:%S")
        if date
        else ""
    )
    pywikibot.stdout("%s%s" % (dstr, text), newline=newline)

# The following was written by Zitrax on GitHub
def findEndOfTemplate(text, template):
    """Find end of any template, by Zitrax"""
    m = re.search(r"{{\s*%s" % template, text)
    if not m:
        return 0

    lvl = 0
    cp = m.start() + 2

    while cp < len(text):
        ns = text.find("{{", cp)
        ne = text.find("}}", cp)

        # If we see no end tag, we give up
        if ne == -1:
            return 0

        # Handle case when there are no more start tags
        if ns == -1:
            if not lvl:
                return ne + 2
            else:
                lvl -= 1
                cp = ne + 2

        elif not lvl and ne < ns:
            return ne + 2
        elif ne < ns:
            lvl -= 1
            cp = ne + 2
        else:
            lvl += 1
            cp = ns + 2
    # Apparently we never found it
    return 0

def tagPOTD(filename):
    page = pywikibot.Page(SITE, filename)
    if page.isRedirectPage():
        page = pywikibot.Page(SITE, page.getRedirectTarget().title())
    old_text = page.get()
    words = ['a']
    if words in old_text:
        return

    new_text = None
    

def tagMOTD(filename):
    page = pywikibot.Page(SITE, filename)
    if page.isRedirectPage():
        page = pywikibot.Page(SITE, page.getRedirectTarget().title())
    old_text = page.get()
    words = ['a']
    if words in old_text:
        return

    new_text = None


def main():
    potd_file = getfile(pywikibot.Page(SITE, get_potd_page_today()).get())
    motd_file = getfile(pywikibot.Page(SITE, get_motd_page_today()).get())
    try:
        tagPOTD(potd_file)
    except:
        pass
    try:
        tagMOTD(motd_file)
    except:
        pass


if __name__ == "__main__":
  try:
    main()
  finally:
    pywikibot.stopme()
