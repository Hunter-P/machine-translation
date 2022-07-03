# coding:utf-8
import re
from collections import Counter
from sklearn.externals import joblib

# rnn attention, crf, seq2seq


def build_words():
    text = open('big.txt').read()
    # 统计词频
    WORDS = Counter(re.findall(r'\w+', text.lower()))
    joblib.dump(WORDS, 'data/WORDS')
    print("WORDS:", WORDS)


class Correction:
    def __init__(self):
        self.WORDS = WORDS = joblib.load('data/WORDS')

    def edits1(self, word):
        """
        编辑距离为1
        :param word:
        :return:
        """
        letters = 'abcdefghijklmnopqrstuvwxyz'
        splits = [(word[:i], word[i:]) for i in range(len(word)+1)]
        deletes = [l+r[1:] for l, r in splits if r]
        transposes = [l+r[1]+r[0]+r[2:] for l, r in splits if len(r)>1]
        replaces = [l+c+r[1:] for l, r in splits if r for c in letters]
        inserts = [l+c+r for l, r in splits for c in letters]
        # print(set(deletes+transposes+replaces+inserts))
        return set(deletes+transposes+replaces+inserts)

    def edits2(self, word):
        """
        编辑距离为2
        :param word:
        :return:
        """
        return (e2 for e1 in self.edits1(word) for e2 in self.edits1(e1))

    def known(self, words):
        """
        过滤掉不存在的单词
        :param words:
        :return:
        """
        return set(w for w in words if w in self.WORDS)

    def prob(self, word):
        """
        计算单词的出现概率
        :param word:
        :param N:
        :return:
        """
        N = sum(self.WORDS.values())
        return self.WORDS[word]/N

    def correction_word(self, word):
        """
        返回概率最大的候选词
        :param word:
        :return:
        """
        return max(self.candidates(word), key=self.prob)

    def correction_sentence(self, sentence):
        correct_sentence = [self.correction_word(word) for word in sentence]
        return correct_sentence

    def candidates(self, word):
        """
        生成候选集
        :param word:
        :return:
        """
        a = (self.known([word]) or self.known(self.edits1(word)) or self.known(self.edits2(word)) or [word])
        return a


# build_words()
input_data = input("input a word or sentence:")
if not input_data:
    data_list = re.findall(r'\w+', input_data.lower())
    if len(data_list) == 1:
        print(Correction().correction_word(data_list[0]))
    else:
        correct_sentence = Correction().correction_sentence(data_list)
        input_data_list = input_data.lower().split(' ')
        result = []
        for i, j in zip(correct_sentence, input_data_list):
            if j[-1] not in 'abcdefghijklmnopqrstuvwxyz':
                i += j[-1]
            result.append(i)
        print(' '.join(result))



