import numpy as np
from sklearn.model_selection import StratifiedKFold, cross_validate, cross_val_predict
from sklearn.pipeline import make_pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.svm import LinearSVC
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import make_scorer, precision_score, recall_score, f1_score, confusion_matrix, classification_report
from joblib import dump

from utilities.data_util import load_csv

#load training dataset
df = load_csv("Intent_Training_Dataset.csv", required_cols=["user_input", "intent"])

df["user_input"] = df["user_input"].astype(str).str.strip()
df["intent"] = df["intent"].astype(str).str.strip()

X = df["user_input"]
y = df["intent"]

#use 3 models and choose best one
models = {
    "Logistic Regression": LogisticRegression(max_iter=1000, random_state=42),
    "Linear SVM": LinearSVC(random_state=42),
    "Naive Bayes": MultinomialNB()
}

#10 fold validation 
kfold = StratifiedKFold(n_splits=10, shuffle=True, random_state=42)

#compute performance metrics
scoring = {
    "accuracy": "accuracy",
    "precision": make_scorer(precision_score, average="macro", zero_division=0),
    "recall": make_scorer(recall_score, average="macro", zero_division=0),
    "f1": make_scorer(f1_score, average="macro", zero_division=0),
}

results = {}

#train and eval each model 
for name, clf in models.items():
    pipeline = make_pipeline(
        TfidfVectorizer(lowercase=True),
        clf
    )

    cv = cross_validate(pipeline, X, y, cv=kfold, scoring=scoring)

    #mean scores for each metric
    acc_mean = np.mean(cv["test_accuracy"])
    prec_mean = np.mean(cv["test_precision"])
    rec_mean = np.mean(cv["test_recall"])
    f1_mean = np.mean(cv["test_f1"])

    results[name] = {
        "accuracy": acc_mean,
        "precision": prec_mean,
        "recall": rec_mean,
        "f1": f1_mean,
    }

    y_pred_cv = cross_val_predict(pipeline, X, y, cv=kfold)
    print(f"{name}:")
    print("Confusion matrix (10 fold CV predictions):")
    print(confusion_matrix(y, y_pred_cv))
    print("Classification report (10 fold CV predictions):")
    print(classification_report(y, y_pred_cv))
    print("------------------------------------------------------------\n")


#selecting best model to use
best_name = None
best_score = -1.0

for name, metrics in results.items():
    score = metrics["f1"] 
    if score > best_score:
        best_score = score
        best_name = name

print(f"Best model by F1: {best_name} with F1={best_score:.3f}")


# trains best model on dataset
best_clf = models[best_name]
best_pipeline = make_pipeline(
    TfidfVectorizer(lowercase=True),
    best_clf
)
best_pipeline.fit(X, y)
dump(best_pipeline, "intent_ml_model.joblib")
print("Model saved as intent_ml_model.joblib")
