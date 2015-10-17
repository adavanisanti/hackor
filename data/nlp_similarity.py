import re
import pandas as pd
np = pd.np
np.norm = np.linalg.norm
from datetime import datetime, date

import matplotlib
import sklearn
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer, TfidfVectorizer
from sklearn.linear_model import SGDClassifier
from sklearn.grid_search import GridSearchCV
from sklearn.pipeline import Pipeline
from sklearn.cross_validation import train_test_split

pacs_scraped = pd.DataFrame.from_csv('public.raw_committees_scraped.csv')  # id
pacs = pd.DataFrame.from_csv('public.raw_committees.csv')  # no ID that I can find
print(pacs_scraped.info())
print(candidates.info())

df = pacs_scraped
names = df.index.values
corpus = [' '.join(str(f) for f in fields if (not isinstance(f, (float, int, datetime, date, np._int, np._float)) and not f in (None, np.nan)))
          for fields in zip(*[df[col] for col in df.columns if df[col].dtype == pd.np.dtype('O')])]
print(corpus[:3])

from collections import Counter
from itertools import chain
tf = Counter(chain(*[doc.split() for doc in corpus]))
print(tf.most_common(10))

# so we need to exclude dates and numbers and "nan"s (we'll let nltk and sklearn handle stop words)
bad_words = set(['nan'])
regex = re.compile(r'^[a-zA-Z][-_a-zA-Z]*[a-zA-Z0-9][!.?]*$')
corpus = [' '.join(token for token in doc.split() if regex.match(token) and token not in bad_words)
          for doc in corpus]

vectorizer = TfidfVectorizer(analyzer='word', ngram_range=(1, 2), stop_words='english')
# rows should be documents, columns should be "words"
vectors = vectorizer.fit(corpus)
tfidf = vectors.transform(corpus)
tfidf_df = pd.DataFrame(tfidf.todense(), index=names)
print(dir(tfidf))
cov = tfidf * tfidf.T
cov_df = pd.DataFrame(cov.todense(), columns=names, index=names)

# to get some interesting e-mails to colate with politicians
# sudo apt-get install pv gzip
# curl -O --anyauth https://raw.githubusercontent.com/jamesmishra/mysqldump-to-csv/master/mysqldump_to_csv.py
# chmod +x mysqldump_to_csv.py
# pv aminno_member_email.dump.gz | zcat | python2 mysqldump_to_csv.py > aminno_member_email.csv

import pandas as pd
import csv
import os
import re
home = os.getenv('HOME')
emails = ''
mem_MB = 2000
top_tlds = {
        '.com': ('Commercial': 4860000000),
        '.org': ('Noncomercial', 1950000000),
        '.edu': ('US accredited postsecondary institutions': 1550000000),
        '.gov': ('United States Government': 1060000000),
        '.uk':  ('United Kingdom', 473000000),
        '.net': ('Network services', 206000000),
        '.ca': ('Canada', 165000000),
        '.de': ('Germany', 145000000),
        '.jp': ('Japan', 139000000),
        '.fr': ('France', 96700000),
        '.au': ('Australia', 91000000),
        '.us': ('United States', 68300000),
        '.ru': ('Russian Federation', 67900000),
        '.ch': ('Switzerland', 62100000),
        '.it': ('Italy', 55200000),
        '.nl': ('Netherlands', 45700000),
        '.se': ('Sweden', 39000000),
        '.no': ('Norway', 32300000),
        '.es': ('Spain', 31000000),
        '.mil': ('US Military', 28400000)
        }
tlds = set(top_tlds)
email_regex = re.compile('[a-zA-Z0-9-.!#$%&*+-/=?^_`{|}~]+@[a-zA-Z0-9-.]+(' + '|'.join(''tlds) + ')')
with open('/home/hobs/Downloads/dmps/aminno_member_email.csv') as f:
    reader = csv.reader(f)
    for i, row in enumerate(reader):
        em = email_regex.search(em)
        if em:
            emails += em.group() + '\n'
        if len(emails) > MB * 1000000:
            break
        if not (i % 100000):
            print(i / 100000.)
with open('/home/hobs/Downloads/dmps/emails3gb.txt', 'w') as f:
    f.write(emails)
print(emails[:100])
del emails
emails = pd.DataFrame.from_csv('/home/hobs/Downloads/dmps/emails3gb.txt').index
intersection = []
candidates = pd.DataFrame.from_csv('public.raw_candidate_filings.csv')  # id_nmbr
candidates = set(candidates['email'].unique())
for i, em in enumerate(candidates):
    if str(em).lower().strip() in emails:
        intersection += [em]
        print('{}'.format(em))
    if not i * 100:
        print(i)
print(intersection)