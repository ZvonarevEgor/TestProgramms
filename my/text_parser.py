from PIL import Image
import pytesseract
import os


# Get links to files in the directory
def get_links():
    absolute_links = []
    while True:
        try:
            directory = str(input('Please write link on directory:\n'))
            links = os.listdir(directory)
            for link in links:
                absolute_links.append('{}\{}'.format(directory, link))
            return absolute_links
        except:
            print('Please check if the link is correct.')


# Get the text of each file
def get_descriptions(absolute_links):
    descriptions = {}
    for link in absolute_links:
        text = pytesseract.image_to_string(Image.open(link), lang='rus')
        text = text.replace('\n', ' ')
        file_name = link.split('\\')[-1]
        descriptions[file_name] = text
    return descriptions


# Receive files containing the necessary word
def get_files(descriptions, keyword):
    suitable_files = {}
    for value in descriptions.values():
        words = value.lower().split(' ')
        if keyword.lower() in words:
            for key in descriptions.keys():
                if descriptions[key] == value:
                    suitable_files[key] = value
    return suitable_files


# Receive the full name of the person and we form the answer
def get_result(suitable_files):
    default_words = ['доверяю', 'доверяет', 'уполномачивает', 'уполномачиваю']
    result = {}
    upper_words = []
    for key in suitable_files.keys():
        bad = ['\\', '/', ':', '*', '?', '"', '<', '>', '|', '●', '!', '.',
               ',', ';', '(', ')', '»', '«', '-', '_', '+', '`', '‘']
        clean_str = (suitable_files[key]).translate({ord(symbol): ' ' for symbol in bad})
        for word in default_words:
            if word in clean_str.lower().split(' '):
                index = clean_str.find(word)
                clean_str = clean_str[index:]
        clean_words = clean_str.split(' ')
        for word in clean_words:
            if len(word) > 0:
                if word[0].isupper():
                    upper_words.append(clean_words.index(word))
        good_words = get_index_name(upper_words)
        full_name = '{} {} {}'.format(clean_words[good_words[0]], clean_words[good_words[1]], clean_words[good_words[2]])
        result[key] = full_name
        upper_words.clear()
    return result


# Looking for the right person
def get_index_name(upper_words):
    finish_list = []
    last_word = upper_words[0]
    finish_list.append(last_word)
    for i in range(len(upper_words)):
        if i > 0:
            if int(upper_words[i]) - int(last_word) == 1:
                finish_list.append(int(upper_words[i]))
            else:
                if len(finish_list) < 3:
                    finish_list.clear()
                else:
                    if len(finish_list) > 3:
                        return finish_list[-4:-1]
                    else:
                        return finish_list
        last_word = upper_words[i]


# Main function
def process():
    string = ''
    absolute_links = get_links()
    keyword = str(input('\n\nPlease write keyword:\n'))
    descriptions = get_descriptions(absolute_links)
    suitable_files = get_files(descriptions, keyword)
    result = get_result(suitable_files)
    for key in result.keys():
        string += 'File: {}\nPerson: {}\n\n'.format(key, result[key])
    print(string)


if __name__ == '__main__':
    process()
