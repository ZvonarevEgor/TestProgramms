
import requests
import json
from collections import Counter
from bs4 import BeautifulSoup


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
            break
        i += 1

#Making 1 list only with vacancies
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
    #print(json.dumps(main_text[0], indent = 4, ensure_ascii = False))

def get_all_descriptions(vacancies_id):
    descriptions = []
    for id_ in vacancies_id:
        description = get_vacancy(id_)
        descriptions.append(description)
    return descriptions

def get_main_list(descriptions):
    main_list = []
    for description in descriptions:
        str_ = description.replace('.', ' ')
        str_ = str_.replace(':', ' ')
        str_ = str_.replace('/', ' ')
        list_words = str_.split(' ')
        for word in list_words:
            if len(word) < 3:
                pass
            else:
                main_list.append(word)
    return main_list

def sort_words(main_list):
    words = Counter(main_list)
    popular = words.most_common(100)
    return popular


vacancies_id = get_all_id(get_all_pages())
popular = sort_words(get_main_list(get_all_descriptions(vacancies_id)))
print(popular)

