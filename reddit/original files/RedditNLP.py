import json
import string
import numpy as np
import datetime
import pandas as pd
import matplotlib.pyplot as plt

from nltk import word_tokenize
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfVectorizer
from nltk.stem.porter import PorterStemmer
from collections import Counter


stemmer = PorterStemmer()
remove_punc = str.maketrans('', '', string.punctuation)
remove_numbers = str.maketrans('', '', "0123456789")


# Load a reddit dump from file
def load_reddit_dump(file):
    data = json.load(open(file))
    submissions = []
    documents = []
    for sub in data:
        submissions.append(sub)
        documents.append(transform_submission_into_document(sub))
    return submissions, documents


# Organizes all submissions based on the week that the submission was posted
def group_submissions_by_date(submissions, date_key_format='%Y_%m'):
    submission_groups = []
    dates = {}

    # Loop through all submissions, grouping them by date
    for sub in submissions:
        # Compute the date key for this submission. The default is Year_Month#
        date_key = datetime.datetime.fromtimestamp(int(sub["created"])).strftime(date_key_format)
        dates[date_key] = date_key
        # Record the submission
        submission_groups.append(date_key)

    return submission_groups, dates.keys()


# Recursively merge all comments in a submission into a single document
def transform_submission_into_document(submission):
    doc = submission["body"] + '\n'
    for c in submission["comments"]:
        doc = _transform_submission_into_document(doc, submission["comments"][c])
    return doc
def _transform_submission_into_document(doc, comment):
    doc = doc + comment["body"] + '\n'
    for c in comment["comments"]:
        doc = _transform_submission_into_document(doc, comment["comments"][c])
    return doc


# Compute the tfidf for a collection of submissions
def compute_tfidf_for_submissions(submissions):
    tfv = TfidfVectorizer(
        analyzer="word",  # The analyzer to use
        stop_words='english',       # Remove all english stopwords
        ngram_range=(1,2),          # Include n-grams
        sublinear_tf=True,          # Apply a logorithmic transformation to the weights
        #max_features=None,          # The maximum number of features to record
        #strip_accents="unicode",    # Treat this as unicode text
        #token_pattern=r'w{1,}',     #
        #use_idf=True,               #
        #smooth_idf=True,            #
        #max_df=0,                   # Only record weights that are greater than this value (ignore corpus-specific "stopwords")
        # tokenizer=tokenize,
    )
    tfs = tfv.fit_transform(submissions)
    return tfs, tfv


def top_tfidf_feats(row, features, top_n=25):
    ''' Get top n tfidf values in row and return them with their corresponding feature names.'''
    topn_ids = np.argsort(row)[::-1][:top_n]
    top_feats = [(features[i], row[i]) for i in topn_ids]
    df = pd.DataFrame(top_feats)
    df.columns = ['feature', 'tfidf']
    return df


def top_feats_in_doc(Xtr, features, row_id, top_n=25):
    ''' Top tfidf features in specific document (matrix row) '''
    row = np.squeeze(Xtr[row_id].toarray())
    return top_tfidf_feats(row, features, top_n)


def top_mean_feats(Xtr, features, grp_ids=None, min_tfidf=0.1, top_n=25):
    ''' Return the top n features that on average are most important amongst documents in rows
        indentified by indices in grp_ids. '''
    if grp_ids is not None:
        D = Xtr[grp_ids].toarray()
    else:
        D = Xtr.toarray()

    D[D < min_tfidf] = 0
    tfidf_means = np.mean(D, axis=0)
    return top_tfidf_feats(tfidf_means, features, top_n)


def top_feats_by_period(Xtr, y, features, min_tfidf=0.1, top_n=25):
    ''' Return a list of dfs, where each df holds top_n features and their mean tfidf value
        calculated across documents with the same class label. '''
    dfs = []
    labels = np.unique(y)
    for label in labels:
        ids = np.where(y==label)
        feats_df = top_mean_feats(Xtr, features, ids, min_tfidf=min_tfidf, top_n=top_n)
        feats_df.label = label
        dfs.append(feats_df)
    return dfs


def plot_tfidf_classfeats_h(dfs):
    ''' Plot the data frames returned by the function plot_tfidf_classfeats(). '''
    fig = plt.figure(figsize=(12, 9), facecolor="w")
    x = np.arange(len(dfs[0]))
    for i, df in enumerate(dfs):
        ax = fig.add_subplot(1, len(dfs), i+1)
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)
        ax.set_frame_on(False)
        ax.get_xaxis().tick_bottom()
        ax.get_yaxis().tick_left()
        ax.set_xlabel("Mean Tf-Idf Score", labelpad=16, fontsize=14)
        ax.set_title("label = " + str(df.label), fontsize=16)
        ax.ticklabel_format(axis='x', style='sci', scilimits=(-2,2))
        ax.barh(x, df.tfidf, align='center', color='#3F5D7D')
        ax.set_yticks(x)
        ax.set_ylim([-1, x[-1]+1])
        yticks = ax.set_yticklabels(df.feature)
        plt.subplots_adjust(bottom=0.09, right=0.97, left=0.15, top=0.95, wspace=0.52)
    plt.show()