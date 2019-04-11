def get_popular(descriptions_list, stop_words):
    words_dict = {}
    for words in descriptions_list:
        words_list = words.split(' ')
        max_index = len(words_list) - 1
        for word in words_list:
            this_index = words_list.index(word)
            if word not in stop_words:
                if word in words_dict.keys():
                    words_dict[word]['counts'] += 1
                else:
                    words_dict[word] = {'counts': 1, 'prev_words': {}, 'next_words': {}}
                if this_index > 0 and this_index < max_index:
                    prev_word = words_list[this_index - 1]
                    next_word = words_list[this_index + 1]
                    if prev_word not in stop_words and next_word not in stop_words:
                        prev_words_dict = words_dict[word]['prev_words']
                        next_words_dict = words_dict[word]['next_words']
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
                        next_words_dict = words_dict[word]['next_words']
                        if next_word not in next_words_dict.keys():
                            words_dict[word]['next_words'][next_word] = 1
                        else:
                            words_dict[word]['next_words'][next_word] += 1
                    else:
                        prev_word = words_list[this_index - 1]
                        prev_words_dict = words_dict[word]['prev_words']
                        if prev_word not in prev_words_dict.keys():
                            words_dict[word]['prev_words'][prev_word] = 1
                        else:
                            words_dict[word]['prev_words'][prev_word] += 1

    return words_dict


descriptions_list = ['привет как дела', 'ало как жизнь', 'жизнь как классная штука']
stop_words = ['жизнь']
words_dict = get_popular(descriptions_list, stop_words)
print(words_dict)
                                
                    
                    
                    
        
