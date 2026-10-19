import pandas as pd
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from sklearn.metrics.pairwise import cosine_similarity

from utilities.data_util import load_csv

#load qa dataset
qa = load_csv("COMP3074-CW1-Dataset.csv", required_cols=[
    "QuestionID", "Question"])
qa = qa.dropna(subset=["Question", "Answer"])
qa["Question"] = qa["Question"].astype(str).str.strip()
qa["Answer"] = qa["Answer"].astype(str).str.strip()

qa_questions = qa["Question"].tolist()
qa_answers = qa["Answer"].tolist()

#tfidf
count_vect = CountVectorizer(stop_words=stopwords.words('english'))
X_train_counts = count_vect.fit_transform(qa_questions)

tfidf = TfidfTransformer(use_idf=True, sublinear_tf=True).fit(X_train_counts)
X_tfidf = tfidf.transform(X_train_counts)



#retreiving answer from qa dataset
def get_answer(user_query: str):
    query_vect = tfidf.transform(count_vect.transform([user_query]))
    
    sims = cosine_similarity(query_vect, X_tfidf).ravel()
    best_idx = sims.argmax()
    best_score = sims[best_idx]

    if best_score > 0.3:
        return (qa_answers[best_idx], best_score)
    else:
        return("Sorry, I'm not sure what you mean. Could you please rephrase?", best_score)
    
