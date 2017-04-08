# coding: utf-8
# Wordnet via Python3
# 
# ref:
#   WordList_JP: http://compling.hss.ntu.edu.sg/wnja/
#   python3: http://sucrose.hatenablog.com/entry/20120305/p1

import sys, sqlite3
from collections import namedtuple
import MeCab
import random
import Vocabulary1

conn = sqlite3.connect("./wnjpn.db", check_same_thread = False)

Word = namedtuple('Word', 'wordid lang lemma pron pos')

def getWords(lemma):
  cur = conn.execute("select * from word where lemma=?", (lemma,))
  return [Word(*row) for row in cur]

 
Sense = namedtuple('Sense', 'synset wordid lang rank lexid freq src')

def getSenses(word):
  cur = conn.execute("select * from sense where wordid=?", (word.wordid,))
  return [Sense(*row) for row in cur]

Synset = namedtuple('Synset', 'synset pos name src')

def getSynset(synset):
  cur = conn.execute("select * from synset where synset=?", (synset,))
  return Synset(*cur.fetchone())

def getWordsFromSynset(synset, lang):
  cur = conn.execute("select word.* from sense, word where synset=? and word.lang=? and sense.wordid = word.wordid;", (synset,lang))
  return [Word(*row) for row in cur]

def getWordsFromSenses(sense, lang="jpn"):
  synonym = {}
  for s in sense:
    lemmas = []
    syns = getWordsFromSynset(s.synset, lang)
    for sy in syns:
      lemmas.append(sy.lemma)
    synonym[getSynset(s.synset).name] = lemmas
  return synonym

def getSynonym (word):
    synonym = {}
    words = getWords(word)
    if words:
        for w in words:
            sense = getSenses(w)
            s = getWordsFromSenses(sense)
            synonym = dict(list(synonym.items()) + list(s.items()))
    return synonym


def synonymlist(sentence):
    wordwrite = sentence
    synonym = getSynonym(wordwrite)
    synonym2 = list(synonym.values())
    synonym3 = []
    for syno in range(len(synonym2)):
      synonym3.append(' '.join(synonym2[syno]))
    synonym4 = ' '.join(synonym3)
    wordlist = synonym4.rstrip(" \n").split(" ")
    wordlist2 = []
    for w in wordlist:
      t4 = MeCab.Tagger("mecabrc")
      m3 = t4.parse(w)
      if '名詞' in m3:
        wordlist2.append(w)
    # wordlist2と語彙リストを比較して一致する単語を返す
    # print(wordlist2)
    wordlist2_set = set(wordlist2)
    vocabulary_set = set(Vocabulary1.vocabulary)
    vocabulary_list = list(wordlist2_set & vocabulary_set)
    # print(vocabulary_list)
    
    max_list = []
    if len(vocabulary_list) == 0:
      vocabulary_list.append(sentence)
      word = vocabulary_list[-1]
    elif len(vocabulary_list) == 1:
      word = vocabulary_list[-1]
    else:
      for w1 in vocabulary_list:
        number = 0
        w2 = ()
        for n1 in range(len(sentence)):
          number += w1.count(sentence[n1])
        w2 = (w1, number)
        max_list.append(w2)
      max_dic = dict(max_list)
      # print("----------類義語の一致度:", max_list)
      word_max = max(max_dic.items(), key = lambda x:x[1])[0]
      word = word_max
    # \\\\\\\\\\
    # print("----------語彙リストとの比較結果:", vocabulary_list)    
    return word

def synonymwords(sentence):
    wordwrite = sentence
    synonym = getSynonym(wordwrite)
    synonym2 = list(synonym.values())
    synonym3 = []
    for syno in range(len(synonym2)):
      synonym3.append(' '.join(synonym2[syno]))
    synonym4 = ' '.join(synonym3)
    return synonym4


def sentence_generator(speech):
    sentenceInput = speech
    wordlist2 = []
    t = MeCab.Tagger("-Owakati")
    m = t.parse(sentenceInput)
    result = m.rstrip(" \n").split(" ")
    for (i, sen) in enumerate(result):
        t2 = MeCab.Tagger("mecabrc")
        m2 = t2.parse(sen)
        if '名詞' in m2:
            synonym6 = synonymlist(sen)
            if synonym6 != '':
                result[i] = synonym6
    sentence2 = ''.join(result)
    # print(sentence2)
    return sentence2
