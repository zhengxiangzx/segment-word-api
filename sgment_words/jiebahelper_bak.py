# -*- coding: utf-8 -*-

import jieba
import jieba.analyse
import jieba.posseg
import re

from smart_open import smart_open

'''
 分词模块-分词去停用词（去掉非汉字字母的其他所有字符）
 添加自定义词典（发现有新词没有被分出时手动添加）
'''

# 过滤非汉字字母的其他字符条件
pattern = re.compile(u'[^\u4e00-\u9fa5^a-z^A-Z]')
# user_dict_path = '/data/download/jieba_dependencies/user_dict.txt'
# stop_words_path = '/data/download/jieba_dependencies/stop_words.txt'
user_dict_path = './dependencies/user_dict.txt'
stop_words_path = './dependencies/stop_words.txt'


def load_stop_words():
    """
    加载停用词
    :return: 返回停用词词典
    """
    stop_words_list = []
    with smart_open(stop_words_path, 'rb', encoding='utf-8') as fin:
        for word in fin:
            stop_words_list.append(word)
    return stop_words_list


# 加载停用词
stop_words = load_stop_words()
emptyList = ["\t", "\r\n", "\r", "\n"]


def segment(sentence):
    """
    进行分词 去停用词,精确模式,不加词性标注
    :param sentence:要被分词的句子
    :return:返回分好的词
    """
    # 加载自定义词典(自定义词典是变化的-需要调用的时候再重新加载)
    jieba.load_userdict(user_dict_path)
    # 非汉字字母的部分
    sentence = pattern.sub(r'', sentence)
    # 去掉url地址
    sentence = re.sub(r'(https|http)?:\/\/(\w|\.|\/|\?|\=|\&|\%)*\b', '', sentence, flags=re.MULTILINE)
    # 执行jieba分词 HMM开启,精确模式
    sentence_segment = jieba.lcut(sentence.strip())
    # 去停用词
    output_words = " ".join(list(filter(lambda x: (x not in stop_words and x not in emptyList), sentence_segment)))
    return output_words


def extract_tags(content, topk):
    """

    :param content:
    :param topk:
    :return:
    """
    content = content.strip()
    tags = jieba.analyse.extract_tags(content, topK=topk)
    return ','.join(tags)


def add_dict(words):
    """
    发现的新词添加到自定义词典里
    :param words:
    :return:
    """
    # 返回的词典中没有的和已有的 但是频数不一致的
    words = words.strip()
    add_words = words.split('|')
    words_dict = {}
    for w in add_words:
        name = w.split(' ')[0].strip()
        num = w.split(' ')[-1].strip()
        words_dict[name] = int(num)
    add_words_dict = add_check(words_dict)
    with smart_open(user_dict_path, 'ab+', encoding='utf-8') as fin:
        for name, count in add_words_dict.items():
            fin.write(name + " " + str(count) + "\n")
    return '添加修改成功'


def add_check(add_word):
    local_word = load_dict()
    word_not_exist = list(filter(lambda x: x not in local_word.keys(), add_word.keys()))
    # word_exist = list(filter(lambda x: x in local_word.keys(), add_word.keys()))
    add_words_dict = {}
    for word in word_not_exist:
        add_words_dict[word] = add_word[word]
    # for word in word_exist:
    #     if add_word[word] != local_word[word]:
    #         add_words_dict[word] = add_word[word]
    #     else:
    #         print('添加的词：%s 已添加过,频数也一样不用在添加' % word)
    return add_words_dict


def load_dict():
    """
    读取自定义词典
    :return: 返回自定义词典的列表
    """
    word_list = {}
    with smart_open(user_dict_path, 'rb', encoding='utf-8') as fin:
        for word in fin:
            name = word.split(' ')[0].strip()
            num = word.split(' ')[-1].strip()
            word_list[name] = int(num)
    return word_list

# if __name__ == '__main__':
#     add_dict('你好 2|不好 7')
