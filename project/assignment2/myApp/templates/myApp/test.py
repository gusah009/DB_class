import pandas as pd

df = pd.read_csv('./students.csv', header=None)
# print(df)
for index, row in df.iterrows():
  print(row[1])
  print("-------------")