import pywikibot
import re,sys
from datetime import timedelta,datetime

TODAY = datetime.utcnow()
SITE = pywikibot.Site()
time_to_change = 1
def informatdate():
    return (TODAY+timedelta(time_to_change)).strftime('%Y-%m-%d')

def formatMotdTemplateTag():
    gar = (TODAY+timedelta(time_to_change)).strftime('%Y|%-m|%-d')
    return gar

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
    print("potd")
    page = pywikibot.Page(SITE, filename)
    if page.isRedirectPage():
        page = pywikibot.Page(SITE, page.getRedirectTarget().title())
    old_text = page.get()

    word1 = "Picture of the day"
    word2 = "picture of the day"
    redir = "#REDIRECT"
    if word1 in old_text: 
        out("Tag already there, exiting program.", color="lightred")
        sys.exit(0)
    if word2 in old_text: 
        out("Tag already there, exiting program.", color="lightred")
        sys.exit(0)    
    if redir in old_text: 
        out("Redirected Page", color="lightred")
        sys.exit(0) 
    end = findEndOfTemplate(old_text, "[Aa]ssessments")
    new_text = (
            old_text[:end]
            + "\n{{Picture of the day|%s}}" % formatMotdTemplateTag()
            + old_text[end:]
        )

    try:
        commit(
            old_text, new_text, page, "POTD tagging, see [[Template:Potd/%s]]" % informatdate()
        )
    except pywikibot.LockedPage as error:
        out(
            "Page is locked '%s', but ignoring since it's just the motd tag."
            % error,
            color="lightyellow",
        )
    

def tagMOTD(filename):
    print("motd")
    page = pywikibot.Page(SITE, filename)
    if page.isRedirectPage():
        page = pywikibot.Page(SITE, page.getRedirectTarget().title())
    old_text = page.get()
    print("old text got")
    word1 = "{{Media of the day"
    word2 = "{{media of the day"
    redir = "#REDIRECT"
    Assdetect = "{{Assessment}}"
    if word1 in old_text: 
        out("Tag already there, exiting program.", color="lightred")
        sys.exit(0)
    if word2 in old_text:
        out("Tag already there, exiting program.", color="lightred")
        sys.exit(0)
    if redir in old_text: 
        out("Redirected Page", color="lightred")
        sys.exit(0)    
    end = findEndOfTemplate(old_text, "[Ii]nformation")
    if Assdetect not in old_text:
        new_text = (
                old_text[:end]
                + "\n=={{Assessment}}==\n{{Media of the day|%s}}\n" % formatMotdTemplateTag()
                + old_text[end:]
            )
    else:
        new_text = (
                old_text[:end]
                + "\n{{Media of the day|%s}}\n" % formatMotdTemplateTag()
                + old_text[end:]
                )

    try:
        commit(
            old_text, new_text, page, "MOTD tagging, from [[Template:Motd/%s]]" % informatdate()
        )
    except pywikibot.LockedPage as error:
        out(
            "Page is locked '%s', but ignoring since it's just the motd tag."
            % error,
            color="lightyellow",
        )

def main():
    potd_file = getfile(pywikibot.Page(SITE, get_potd_page_today()).get())
    motd_file = getfile(pywikibot.Page(SITE, get_motd_page_today()).get())
    try:
        tagPOTD(potd_file)
    except:
        pass

    tagMOTD(motd_file)



if __name__ == "__main__":
  try:
    main()
  finally:
    pywikibot.stopme()
