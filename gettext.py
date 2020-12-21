# I copied these lines from jss367.github.io 
import re
def gettext(raw, title, author):
  
    start_regex = '\*\*\*\s?START OF TH(IS|E) PROJECT GUTENBERG EBOOK.*\*\*\*'
    draft_start_position = re.search(start_regex, raw)
    begining = draft_start_position.end()

    if re.search(title.lower(), raw[draft_start_position.end():].lower()):
        title_position = re.search(title.lower(), raw[draft_start_position.end():].lower())
        begining += title_position.end()
        # If the title is present, check for the author's name as well
        if re.search(author.lower(), raw[draft_start_position.end() + title_position.end():].lower()):
            author_position = re.search(author.lower(), raw[draft_start_position.end() + title_position.end():].lower())
            begining += author_position.end()
    
    end_regex = 'end of th(is|e) project gutenberg ebook'
    end_position = re.search(end_regex, raw.lower())

    text = raw[begining:end_position.start()]
    
    return text