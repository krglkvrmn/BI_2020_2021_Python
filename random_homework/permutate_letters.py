import random
import re


text = input("Enter text: ")
words = re.findall(r"\w+", text)
for word in words:
    if len(word) > 3:
        middle_word = list(word[1:-1])
        random.shuffle(middle_word)
        perm_word = word[0] + "".join(middle_word) + word[-1]
        word_pos = text.find(word)
        text = text[:word_pos] + perm_word + text[word_pos + len(word):]
print(text)
