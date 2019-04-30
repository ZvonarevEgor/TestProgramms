import pymorphy2
import requests
from bs4 import BeautifulSoup
from time import sleep
# -*- coding: utf-8 -*-

morph = pymorphy2.MorphAnalyzer()


# Download job pages
def get_all_pages():
    list_pages = []
    i = 0

    while True:
        url = 'https://api.hh.ru/vacancies'
        parameters = {'text': 'junior python developer', 'experience': 'noExperience',
                      'order_by': 'relevance', 'period': '30', 'page': i}
        r = requests.get(url, parameters)
        i_list = r.json()
        list_pages.append(i_list)
        pages_count = i_list['pages']
        if i == pages_count - 1:
            return list_pages
        i += 1


# Making 1 list only with vacancies
def get_all_id(list_pages):
    vacancies_id = []
    for dict_ in list_pages:
        for vacancy in dict_['items']:
            vacancies_id.append(vacancy['id'])
    return vacancies_id


# Get a list with all the id's found
def get_vacancy(id_):
    url_vac = 'https://api.hh.ru/vacancies/' + str(id_)
    r = requests.get(url_vac)
    description = r.json()
    text_wo_tg = BeautifulSoup(description['description'], "lxml").text
    return text_wo_tg


# Get a description of all vacancies found
def get_all_descriptions(vacancies_id):
    descriptions_list = []
    for id_ in vacancies_id:
        if len(descriptions_list) < (len(vacancies_id) // 3):
            description = get_vacancy(id_)
            descriptions_list.append(description)
        sleep(0.5)
    return descriptions_list


# Get the normal form of each word in the description
def normal_form_list(clean_list):
    words_list = []
    for small_list in clean_list:
        words_list.append([])
        for word in small_list:
            p = morph.parse(word)[0]
            words_list[-1].append(p.normal_form)
    return words_list


# Get rid of punctuation in description
def get_clean_list(descriptions_list):
    clean_list = []
    for description in descriptions_list:
        description = description.lower()
        bad = ['\\', '/', ':', '*', '?', '"', '<', '>', '|', '●', '!', '.',
               ',', ';', '(', ')', '»', '«', '-', '_', '+', '`']
        clean_str = description.translate({ord(symbol): ' ' for symbol in bad})
        list_words = clean_str.split(' ')
        clean_list.append([])
        for word in list_words:
            if len(word) >= 2:
                clean_list[-1].append(word)
    return clean_list


# Get a list with stop words from txt
def get_stop_words():
    with open('STOP_WORDS.txt', 'r') as f:
        data = f.read()
    data = data.replace('\n', ' ')
    stop_words = data.split(' ')
    return stop_words  


# Create a dictionary with words and their repetitions
def get_popular(clean_list, stop_words):
    words_dict = {}
    for words_list in clean_list:
        max_index = len(words_list) - 1
        for word in words_list:
            this_index = words_list.index(word)
            if word not in stop_words:
                if word in words_dict.keys():
                    if words_dict[word]['last_vacancy'] != words_list:
                        words_dict[word]['counts'] += 1
                        words_dict[word]['last_vacancy'] = words_list
                else:
                    words_dict[word] = {'counts': 1, 'last_vacancy': words_list, 'next_words': {}}
                next_words_dict = words_dict[word]['next_words']

                if 0 <= this_index < max_index:
                    next_word = words_list[this_index + 1]
                    if next_word in next_words_dict:
                        words_dict[word]['next_words'][next_word] += 1
                    elif next_word not in stop_words:
                        words_dict[word]['next_words'][next_word] = 1

    return words_dict


# Sort the list of main words by the number of repetitions
def sort_dict(words_dict):
    """
    words_dict: {"<word>": {"counts": int, "last_vacancy": list, "next_words": int}}
    """
    sorted_list = []
    for key in words_dict.keys():
        sorted_list.append([])
        sorted_list[-1].append(key)
        sorted_list[-1].append(words_dict[key]['counts'])
    sorted_list.sort(key=lambda element: element[1], reverse=True)
    return sorted_list


# Sort the list of words that occur before the main word
def sort_not_main(not_main_words):
    """
    not_main_words: {"<word>": int}
    """
    sorted_words = []
    for key in not_main_words.keys():
        sorted_words.append([])
        index = len(sorted_words) - 1
        sorted_words[index].append(key)
        sorted_words[index].append(not_main_words[key])
    sorted_words.sort(key=lambda element: element[1], reverse=True)
    return sorted_words


# Form a message to answer
def make_message(words, next_words):
    message = ''
    if len(next_words) == 0:
        message = '{} - {}'.format(words[0], words[1])
    else:
        if next_words[0][1] > (words[1] // 2):
            min_count = min(next_words[0][1], words[1])
            message += '{} {} - {}'.format(words[0], next_words[0][0], min_count)
        else:
            message = '{} - {}'.format(words[0], words[1])
    return message


# Filter same words
def make_positions(sorted_list, words_dict):
    finish_list = []
    for words in sorted_list:
        word = words[0]
        sorted_next = sort_not_main(words_dict[word]['next_words'])
        one_position = make_message(words, sorted_next)
        finish_list.append(one_position)
    return finish_list


# Skills can be 1 or 2 words. Get a list with long skills
def get_long(finish_list):
    long_positions = []
    for position in finish_list:
        elements_position = position.split(' ')
        index = elements_position.index('-')
        if index == 2:
            long_positions.append(position)
    return long_positions


# Delete same positions
def filter_same(finish_list, count):
    long_positions = get_long(finish_list)
    long_list, finish = get_long_words(finish_list, long_positions)
    deleted_same = sum_long_short(finish, long_list, long_positions)
    sorted_positions = sort_positions(deleted_same)
    sorted_positions_str = make_percents(sorted_positions, count)
    return sorted_positions_str


# Get only long words wo percents
def get_long_words(finish_list, long_positions):
    long_list = []
    finish = finish_list.copy()
    for long in long_positions:
        index = finish.index(long)
        finish.pop(index)
        list_words_long = long.split(' ')[:2]
        for word in list_words_long:
            long_list.append(word)
    return long_list, finish


# Sum list with long words and list with short words
def sum_long_short(finish, long_list, long_positions):
    deleted_same = []
    for position in finish:
        position_word = position.split(' ')[0]
        if position_word not in long_list:
            deleted_same.append(position)
    for long in long_positions:
        deleted_same.append(long)
    return deleted_same


# Sort positions in list by count
def sort_positions(deleted_same):
    sorted_positions = []
    for position in deleted_same:
        position_words_list = position.split(' ')
        sorted_positions.append(position_words_list)
    sorted_positions.sort(key=lambda element: int(element[-1]), reverse=True)
    return sorted_positions


# Replace count on percents
def make_percents(sorted_positions, count):
    sorted_positions_str = ''
    for position in sorted_positions:
        numbers = position[-1]
        sorted_positions_str += '\n'
        for word in position:
            if word == numbers:
                one_percent_value = int(count)/100
                percents = int(word)/one_percent_value
                percents = float('{:.2f}'.format(percents))
                sorted_positions_str += '{}%'.format(str(percents))
            else:
                sorted_positions_str += '{} '.format(word)
    return sorted_positions_str


# Main function
def process():
    list_pages = get_all_pages()
    descriptions_list = get_all_descriptions(get_all_id(list_pages))
    count = str(len(descriptions_list))
    message = 'Всего вакансий найдено: {}\nСтатистика представлена только по {} ' \
              'для большей точности, так как вакансии сортируются по соответствию.\n' \
              'Работодатели чаще всего ждут знания:\n\n'.format(int(count)*3, count)
    clean_list = normal_form_list(get_clean_list(descriptions_list))
    stop_words = get_stop_words()
    words_dict = get_popular(clean_list, stop_words)
    sorted_list = sort_dict(words_dict)
    finish_list = make_positions(sorted_list[:20], words_dict)
    filtered_finish = filter_same(finish_list, count)
    for text in filtered_finish:
        message += text
    return message


if __name__ == '__main__':
    print(process())
