import unicodedata


def strip_diacritics(string):
    string = unicodedata.normalize('NFKD', string)
    string = string.encode('ascii', 'ignore')
    return string.decode()
