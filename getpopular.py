import pymorphy2
import requests
import json
from bs4 import BeautifulSoup
# -*- coding: utf-8 -*-

morph = pymorphy2.MorphAnalyzer()

STOP_WORDS = ['программист']


# Download job pages
def get_all_pages():
    list_pages = []
    i = 0

    while True:
        url = 'https://api.hh.ru/vacancies'
        parameters = {'text': 'python', 'area': '1',
                      'experience': 'noExperience', 'page': i}
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
    url_vac = 'https://api.hh.ru/vacancies/' + id_
    r = requests.get(url_vac)
    description = r.json()
    text_wo_tg = BeautifulSoup(description['description'], "lxml").text
    return text_wo_tg


# Get a description of all vacancies found
def get_all_descriptions(vacancies_id):
    descriptions_list = []
    for id_ in vacancies_id:
        description = get_vacancy(id_)
        descriptions_list.append(description)
    return descriptions_list


# Get the normal form of each word in the description
def normal_form_list(clean_list):
    words_list = []
    for small_list in clean_list:
        words_list.append([])
        this_index = len(words_list) - 1
        for word in small_list:
            p = morph.parse(word)[0]
            words_list[this_index].append(p.normal_form)
    return words_list


# Get rid of punctuation in description
def get_main_list(descriptions_list):
    clean_list = []
    for description in descriptions_list:
        description = description.lower()
        str_ = description.replace('.', ' ')
        str_ = str_.replace(';', ' ')
        str_ = str_.replace(',', ' ')
        str_ = str_.replace(':', ' ')
        str_ = str_.replace('/', ' ')
        str_ = str_.replace('(', ' ')
        str_ = str_.replace(')', ' ')
        str_ = str_.replace('-', ' ')
        str_ = str_.replace('"', ' ')
        str_ = str_.replace('●', ' ')
        list_words = str_.split(' ')
        clean_list.append([])
        this_index = len(clean_list) - 1
        for word in list_words:
            if len(word) >= 3:
                clean_list[this_index].append(word)
    return clean_list


# Create a dictionary with words and their repetitions
def get_popular(main_list, stop_words):
    words_dict = {}
    for words_list in main_list:
        max_index = len(words_list) - 1
        for word in words_list:
            this_index = words_list.index(word)
            if word not in stop_words:
                if word in words_dict.keys():
                    words_dict[word]['counts'] += 1
                else:
                    words_dict[word] = {'counts': 1, 'prev_words': {}, 'next_words': {}}
                prev_words_dict = words_dict[word]['prev_words']
                next_words_dict = words_dict[word]['next_words']
                if this_index > 0 and this_index < max_index:
                    prev_word = words_list[this_index - 1]
                    next_word = words_list[this_index + 1]
                    if prev_word not in prev_words_dict:
                        words_dict[word]['prev_words'][prev_word] = 1
                    else:
                        words_dict[word]['prev_words'][prev_word] += 1
                    if next_word not in next_words_dict:
                        words_dict[word]['next_words'][next_word] = 1
                    else:
                        words_dict[word]['next_words'][next_word] += 1
                else:
                    if this_index == 0:
                        next_word = words_list[this_index + 1]
                        if next_word not in next_words_dict.keys():
                            words_dict[word]['next_words'][next_word] = 1
                        else:
                            words_dict[word]['next_words'][next_word] += 1
                    else:
                        prev_word = words_list[this_index - 1]
                        if prev_word not in prev_words_dict.keys():
                            words_dict[word]['prev_words'][prev_word] = 1
                        else:
                            words_dict[word]['prev_words'][prev_word] += 1

    return words_dict


# Sort the list of main words by the number of repetitions
def sort_dict(words_dict):
    sorted_list = []
    for key in words_dict.keys():
        sorted_list.append([])
        index = len(sorted_list) - 1
        sorted_list[index].append(key)
        sorted_list[index].append(words_dict[key]['counts'])
    sorted_list.sort(key=lambda element: element[1], reverse=True)
    return sorted_list


# Sort the list of words that occur before the main word
def sort_prev(prev_words_dict):
    sorted_prev = []
    for key in prev_words_dict.keys():
        sorted_prev.append([])
        index = len(sorted_prev) - 1
        sorted_prev[index].append(key)
        sorted_prev[index].append(prev_words_dict[key])
    sorted_prev.sort(key=lambda element: element[1], reverse=True)
    return sorted_prev


# Sort the list of words that occur after the main word
def sort_next(next_words_dict):
    sorted_next = []
    for key in next_words_dict.keys():
        sorted_next.append([])
        index = len(sorted_next) - 1
        sorted_next[index].append(key)
        sorted_next[index].append(next_words_dict[key])
    sorted_next.sort(key=lambda element: element[1], reverse=True)
    return sorted_next


# Form a message to answer
def make_message(words, prev_words, next_words):
    message = 'Слово: ' + words[0] + ' - ' + str(words[1]) + '\n' + \
              'До:    ' + prev_words[0][0] + ' - ' + \
              str(prev_words[0][1]) + '\n' + '       ' + \
              prev_words[1][0] + ' - ' + str(prev_words[1][1]) + '\n' + \
              'После: ' + next_words[0][0] + ' - ' + \
              str(next_words[0][1]) + '\n' + '       ' + \
              next_words[1][0] + ' - ' + str(next_words[1][1]) + '\n\n'
    return message


# Main function
def process():
    list_pages = get_all_pages()
    descriptions_list = get_all_descriptions(get_all_id(list_pages))
    message = 'Всего вакансий обработано: ' + str(len(descriptions_list)) + '\n\n'
    main_list = normal_form_list(get_main_list(descriptions_list))
    words_dict = get_popular(main_list, STOP_WORDS)
    sorted_list = sort_dict(words_dict)
    for words in sorted_list[:10]:
        word = words[0]
        sorted_prev = sort_prev(words_dict[word]['prev_words'])
        sorted_next = sort_next(words_dict[word]['next_words'])
        message += make_message(words, sorted_prev[:3], sorted_next[:3])
    return message


print(process())
