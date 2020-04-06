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

def uploader(file_name, link=True):
    """Return the link to the user that uploaded this file"""
    history = pywikibot.Page(SITE,file_name).getVersionHistory(reverseOrder=True, total=1)
    if not history:
        return "Unknown"
    if link:
        return "[[User:%s|%s]]" % (history[0][2], history[0][2])
    else:
        return history[0][2]

def Notify(page,File,What=None):
    old_text = page.get()
    if What == "POTD":
        new_text = old_text + "\n\n== [[%s|POTD Notification]] ==\n{{POTDpromotion|%s}} //~~~~" % (get_potd_page_today(),File,)
        EditSummary = "POTD Notification for [[%s]]" % File
    elif What == "MOTD":
        new_text = old_text + "\n\n== [[%s|MOTD Notification]] ==\n{{MOTDpromotion|%s}} //~~~~" % (get_motd_page_today(),File,)
        EditSummary = "MOTD Notification for [[%s]]" % File
    commit(old_text, new_text, page, EditSummary)
    

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

def main():
    potd_page = pywikibot.Page(SITE, get_potd_page_today())
    motd_page = pywikibot.Page(SITE, get_motd_page_today())
    potd_text = potd_page.get()
    motd_text = motd_page.get()
    potd_file = getfile(potd_text)
    motd_file = getfile(motd_text)
    potd_uploader = uploader(potd_file, link=False)
    motd_uploader = uploader(motd_file, link=False)

    if  potd_uploader:
        potd_uploader_talk_page = pywikibot.Page(SITE, ('User talk:'+potd_uploader))
        Notify(potd_uploader_talk_page,potd_file,What="POTD")
    if  motd_uploader:
        motd_uploader_talk_page = pywikibot.Page(SITE, ('User talk:'+motd_uploader))
        Notify(motd_uploader_talk_page,motd_file,What="MOTD")



if __name__ == "__main__":
  try:
    main()
  finally:
    pywikibot.stopme()
