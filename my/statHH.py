import requests
import pymorphy2
from bs4 import BeautifulSoup
from time import sleep

morph = pymorphy2.MorphAnalyzer()


# Download job pages
def get_all_pages():
    list_pages = []
    i = 0

    while True:
        url = 'https://api.hh.ru/vacancies'
        parameters = {'area': '1',
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
    url_vac = 'https://api.hh.ru/vacancies/' + str(id_)
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
        sleep(0.5)
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
def get_clean_list(descriptions_list):
    clean_list = []
    for description in descriptions_list:
        description = description.lower()
        bad = ['\\', '/', ':', '*', '?', '"', '<', '>', '|', '●', '!', '.',
               ',', ';', '(', ')', '#', '-', '+', '=', '&', '@', '№', '%']
        str_ = description.translate({ord(c): ' ' for c in bad})
        list_words = str_.split(' ')
        clean_list.append([])
        this_index = len(clean_list) - 1
        for word in list_words:
            if len(word) >= 3:
                clean_list[this_index].append(word)
    return clean_list


# Create a dictionary with words
def get_popular(clean_list):
    words_dict = {}
    for words_list in clean_list:
        for word in words_list:
            if word in words_dict.keys():
                words_dict[word] += 1
            else:
                words_dict[word] = 1
    return words_dict


# Sort the list of words by the number of repetitions
def sort_dict(words_dict):
    sorted_list = []
    for key in words_dict.keys():
        sorted_list.append([])
        index = len(sorted_list) - 1
        sorted_list[index].append(key)
        sorted_list[index].append(words_dict[key])
    sorted_list.sort(key=lambda element: element[1], reverse=True)
    return sorted_list


def text(words_list):
    f = open('STOP_WORDS.txt', 'w')
    for word in words_list:
        f.write(word + '\n')
    f.close()
    print('Стоп слова успешно добавлены.')


# Main function
def get_stop_words():
    list_pages = get_all_pages()
    descriptions_list = get_all_descriptions(get_all_id(list_pages))
    clean_list = normal_form_list(get_clean_list(descriptions_list))
    words_dict = get_popular(clean_list)
    sorted_list = sort_dict(words_dict)
    words_list = []
    for element in sorted_list:
        words_list.append(element[0])
    text(words_list[:2000])


get_stop_words()
