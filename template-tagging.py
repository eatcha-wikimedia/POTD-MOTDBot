import pywikibot
import re,sys
from datetime import timedelta,datetime

TODAY = datetime.utcnow()
SITE = pywikibot.Site()

def informatdate():
    return (TODAY+timedelta(time_to_change)).strftime('%Y-%m-%d')

def formatMotdTemplateTag():
    return (TODAY+timedelta(time_to_change)).strftime('%Y|%-m|%-d')

def get_page_today(what):
    if what is "MOTD":
        return 'Template:Motd/%s' % informatdate()
    elif what is "POTD":
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

def Tagger(filename,what):
    page = pywikibot.Page(SITE, filename)
    if page.isRedirectPage():
        page = pywikibot.Page(SITE, page.getRedirectTarget().title())
    old_text = page.get()
    if what is "POTD":
        check_text_list = ["{{picture of the day", "POTD=1", "POTDyear=", "POTDmonth=",]
        summary = "POTD tagging, see [[Template:Potd/%s]]" % informatdate()
        template = "\n{{Picture of the day|%s}}\n" % formatMotdTemplateTag()
    if what is "MOTD":
        check_text_list = ["{{media of the day"]
        summary = "MOTD tagging, from [[Template:Motd/%s]]" % informatdate()
        template = "\n{{Media of the day|%s}}\n" % formatMotdTemplateTag()
    if check_text_list:
        for check_text in check_text_list:
            if check_text.lower() in old_text.lower():
                out("Tag already there, exiting program.", color="lightyellow")
                return
    if what is "POTD":
        end = findEndOfTemplate(old_text, "[Aa]ssessments")
    else:
        if re.search(r"\{\{(?:|\s*)[Ll]ocation", old_text):
            end = findEndOfTemplate(old_text, "[Ll]ocation")
        elif re.search(r"\{\{(?:|\s*)[Oo]bject[_\s][Ll]ocation", old_text):
            end = findEndOfTemplate(old_text, "[Oo]bject[_\s][Ll]ocation")
        else:
            end = findEndOfTemplate(old_text, "[Ii]nformation")

    if "{{assessment}}" not in old_text.lower() and what is "MOTD":
        new_text = (
                old_text[:end]
                + "\n=={{Assessment}}==\n{{Media of the day|%s}}\n" % formatMotdTemplateTag()
                + old_text[end:]
            )
    else:
        new_text = (
                old_text[:end]
                + template
                + old_text[end:]
            )

    try:
        commit(old_text, new_text, page, summary,)
    except pywikibot.LockedPage as error:
        out("Page is locked '%s', but ignoring since it's just the motd tag."% error, color="lightyellow",)

def run():
    try:
        Tagger(getfile(pywikibot.Page(SITE, get_page_today("POTD")).get()),"POTD")
    except:
        pass
    try:
        Tagger(getfile(pywikibot.Page(SITE, get_page_today("MOTD")).get()),"MOTD")
    except:
        pass

def main():
    """Tags every thing in 2 months range"""
    for x in range(-15, 45):
        global time_to_change
        time_to_change = x
        run()

if __name__ == "__main__":
  try:
    main()
  finally:
    pywikibot.stopme()
