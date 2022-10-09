import pandas as pd
import numpy as np
import os

df = pd.read_csv("allDecks.csv", index_col=0, header = None)


df["other_champs"] = df.count(axis = 1) - 4
df["deck_rating"] = df[4]/2000 + df[5]/5000*df[4] + df[6]*80*df["other_champs"]
df.fillna("", inplace = True)


df["champs"] = df[1] + "+" + df[2] + "+" +df[3]
df = df.drop([1, 2, 3], axis = 1)
df1 = df["champs"].str.get_dummies("+")
df = pd.concat([df, df1], axis = 1)

print(df)
rating = []

for champ in df[df1.columns].columns:
    champ_data = df.loc[df[champ] == 1]
    l = (champ_data.values == 1).any(axis=0)
    cols = [champ_data.columns[idx] for idx in np.where(l == True)[0]]
    print(cols)
    cols.remove(champ)
    if 6 in cols:
        cols.remove(6)
    if "other_champs" in cols:
        cols.remove("other_champs")
    # print(champ, sum(champ_data["deck_rating"]), cols)
    neighbors = ",".join(cols)
    champ_value = (len(cols)+1)*sum(champ_data["deck_rating"])
    rating.append((champ, champ_value, neighbors))

toprint = sorted(rating, key=lambda x: x[1], reverse=True)
file_object = open('rating.txt', 'w')
for i in range(1, len(toprint)+1):
    strin = f"{i}. Champion {toprint[i-1][0]} has a rating of {toprint[i-1][1]:.2f} and combines with {toprint[i-1][2]} \n"
    print(strin)
    file_object.write(strin)
file_object.close()

os.remove("allDecks.csv")