
from newspaper import nlp
from newspaper.nlp import split_sentences,keywords, split_words, length_score, sbs, dbs, sentence_position 
from collections import Counter


def _new_score(sentences, keywords):
    """Score sentences based on different features
    """
    senSize = len(sentences)
    ranks = Counter()
    for i, s in enumerate(sentences):
        sentence = split_words(s)
        sentenceLength = length_score(len(sentence))
        sentencePosition = sentence_position(i + 1, senSize)
        sbsFeature = sbs(sentence, keywords)
        dbsFeature = dbs(sentence, keywords)
        frequency = (sbsFeature + dbsFeature) / 2.0 * 10.0
        # Weighted average of scores from four categories
        totalScore = ( frequency*2.0 +
                      sentenceLength*1.0 + sentencePosition*1.0)/4.0
        ranks[(i, s)] = totalScore
    return ranks

nlp.score = _new_score

def _new_summarize( text='', max_sents=5):
    
    

    summaries = []
    sentences = split_sentences(text)
    keys = keywords(text)
 

    # Score sentences, and use the top 5 or max_sents sentences
    ranks = nlp.score(sentences, keys).most_common(max_sents)
    for rank in ranks:
        summaries.append(rank[0])
    summaries.sort(key=lambda summary: summary[0])
    return [summary[1] for summary in summaries]




nlp.summarize = _new_summarize

import os
import nltk

import tldextract 
import csv
import enchant



data=[]	

filename='teesta_setal_input.csv'
currentdirpath=os.getcwd()
file_path=os.path.join(os.getcwd(),filename)


with open(file_path,'r+'  ) as reports_file:
  reader = csv.reader(reports_file, delimiter='\t')
  for row in reader:


    article = row[0]
    summary_sentents=nlp.summarize(text = article)

    
    summary = '\n'.join(summary_sentents)
   
    row.append(summary)
    
    textkeys=keywords(article).keys()

    row.append(textkeys)
    
    with open((os.path.join(os.getcwd(),'final_tee.csv')),'a') as newfile:
      writer = csv.writer(newfile, delimiter='\t')
      try:
        writer.writerow(row)

        
      except Exception, e:
        pass
      