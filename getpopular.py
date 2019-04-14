import pymorphy2
import requests
import json
from bs4 import BeautifulSoup

morph = pymorphy2.MorphAnalyzer()

STOP_WORDS = ['программист']


def get_all_pages():
    list_pages = []
    i = 0

    while True:
        url = 'https://api.hh.ru/vacancies'
        parametres = {'text': 'python', 'area':'1','experience': 'noExperience', 'page':i}
        r = requests.get(url, parametres)
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


def get_vacancy(id_):
    url_vac = 'https://api.hh.ru/vacancies/' + id_
    r = requests.get(url_vac)
    description = r.json()
    text_wo_tg = BeautifulSoup(description['description'], "lxml").text
    return text_wo_tg


def get_all_descriptions(vacancies_id):
    descriptions_list = []
    for id_ in vacancies_id:
        description = get_vacancy(id_)
        descriptions_list.append(description)
    return descriptions_list


def normal_form_list(clean_list):
    words_list = []
    for small_list in clean_list:
        words_list.append([])
        this_index = len(words_list) - 1
        for word in small_list:
            p = morph.parse(word)[0]
            words_list[this_index].append(p.normal_form)
    return words_list


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
        list_words = str_.split(' ')
        clean_list.append([])
        this_index = len(clean_list) - 1
        for word in list_words:
            if len(word) >= 3:
                clean_list[this_index].append(word)
    return clean_list


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


def process():
    list_pages = get_all_pages()
    descriptions_list = get_all_descriptions(get_all_id(list_pages))
    clean_list = get_main_list(descriptions_list)
    main_list = normal_form_list(clean_list)
    words_dict = get_popular(main_list, STOP_WORDS)
    print(json.dumps(words_dict, indent=4, ensure_ascii=False))


process()
