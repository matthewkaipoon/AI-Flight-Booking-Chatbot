import re
import nltk

MONTHS = {
    "january": "01", "february": "02", "march": "03",
    "april": "04", "may": "05", "june": "06",
    "july": "07", "august": "08", "september": "09",
    "october": "10", "november": "11", "december": "12"
}

MONTHS_ABBR = {
    "jan": "01", "feb": "02", "mar": "03",
    "apr": "04", "may": "05", "jun": "06",
    "jul": "07", "aug": "08", "sep": "09",
    "oct": "10", "nov": "11", "dec": "12"
}


DATE_FORMAT = re.compile(r"^(\d{1,2})[/-](\d{1,2})[/-](\d{4})$")

def remove_suffix(token: str):
    return re.sub(r'(st|nd|th)$', '', token)

def normalise_date(user_input: str):
    input = user_input.lower().strip()

    if DATE_FORMAT.match(input):
        return input

    tokens = nltk.word_tokenize(input)

    red_tokens = []
    for t in tokens:
        if re.match(r'^\d{1,2}(st|nd|rd|th)?$', t):
            red_tokens.append(t)
        elif t.isalpha():
            red_tokens.append(t)
    if len(red_tokens) < 2:
        return None
    
    day = None
    month = None

    for t in red_tokens:
        if re.match(r'^\d{1,2}(st|nd|rd|th)?$', t):
            reduced = remove_suffix(t)
            if reduced.isdigit():
                day = reduced
        
        if t in MONTHS:
            month = MONTHS[t]

        if t in MONTHS_ABBR:
            month = MONTHS_ABBR[t]

    
    year = "2025"
    pad_day = day.zfill(2)

    return f"{pad_day}/{month}/{year}"