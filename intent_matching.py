from joblib import load

pipeline = load("intent_ml_model.joblib") #load joblib file

#determine intent using ML model
def detect_intent(user_query: str):
    pred = pipeline.predict([user_query])[0]
    proba = pipeline.predict_proba([user_query])[0].max()


    if proba < 0.35: #threshold
        return "fallback", proba
    
    return pred, proba