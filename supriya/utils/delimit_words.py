def delimit_words(string):
    wordlike_characters = ('<', '>', '!')
    current_word = ''
    for character in string:
        if (
            not character.isalpha() and
            not character.isdigit() and
            character not in wordlike_characters
            ):
            if current_word:
                yield current_word
                current_word = ''
        elif not current_word:
            current_word += character
        elif character.isupper():
            if current_word[-1].isupper():
                current_word += character
            else:
                yield current_word
                current_word = character
        elif character.islower():
            if current_word[-1].isalpha():
                current_word += character
            else:
                yield current_word
                current_word = character
        elif character.isdigit():
            if current_word[-1].isdigit():
                current_word += character
            else:
                yield current_word
                current_word = character
        elif character in wordlike_characters:
            if current_word[-1] in wordlike_characters:
                current_word += character
            else:
                yield current_word
                current_word = character
    if current_word:
        yield current_word
