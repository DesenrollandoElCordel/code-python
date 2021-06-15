import re

frequency = {}

document_text = open('test.txt', 'r')
text_string = document_text.read().lower()
match_pattern = re.findall(r'\b[a-z]{4,15}\b', text_string)

for word in match_pattern:
    count = frequency.get(word, 0)
    frequency[word] = count + 1

frequency_list = sorted(frequency.items(), key=lambda x:x[1], reverse=True)
sorted_frequency_list = dict(frequency_list)

for words in sorted_frequency_list:
    print(words, frequency[words])
