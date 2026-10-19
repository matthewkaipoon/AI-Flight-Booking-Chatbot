import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# PLOTTING HEATMAP
data = {
    "Question 01": [4, 4, 3, 3],
    "Question 02": [2, 3, 4, 1],
    "Question 03": [4, 3, 4, 3],
    "Question 04": [3, 4, 3, 4],
    "Question 05": [4, 3, 2, 3],
    "Question 06": [2, 3, 4, 1],
    "Question 07": [5, 4, 4, 5],
    "Question 08": [1, 2, 4, 2],
    "Question 09": [5, 4, 5, 4],
    "Question 10": [5, 4, 4, 4],
    "Question 11": [4, 3, 4, 3]
}

df = pd.DataFrame(data)

df_long = df.melt(var_name='Question', value_name='Response')

response_pivot = df_long.pivot_table(index='Question', columns='Response', aggfunc=len, fill_value=0)

plt.figure(figsize=(12,8))
sns.heatmap(response_pivot, annot=True, cmap="YlGnBu", fmt="d")
plt.title("Likert Scale Questionnaire Responses (4 Participants)")
plt.ylabel("Question")
plt.show()


# PLOTTING STACKED BAR CHART
counts = {
    "Strongly Disagree": [0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 0],
    "Disagree":          [0, 1, 0, 0, 1, 1, 0, 1, 0, 0, 0],
    "Neutral":           [2, 1, 2, 2, 2, 1, 0, 1, 0, 0, 2],
    "Agree":             [2, 1, 2, 2, 1, 1, 2, 1, 2, 3, 2],
    "Strongly Agree":    [0, 0, 0, 0, 0, 0, 2, 0, 2, 1, 0]
}


df_chart = pd.DataFrame(counts, index=[f"Question {i+1:02d}" for i in range(11)])

df_chart.plot(kind='bar', stacked=True, figsize=(12, 6), colormap='viridis')

plt.xlabel("Questions")
plt.ylabel("Number of Responses")
plt.title("Likert Scale Responses (Usability Testing)")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()