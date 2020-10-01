import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import pickle

dataset=pd.read_excel(r'C:\Users\SACHIN PUROHIT\Desktop\healthdata.xlsx')

dataset['Sugar'].fillna(0,inplace=True)
dataset['BP'].fillna(dataset['BP'].mean(),inplace=True)

X = dataset.iloc[:, :3]

y = dataset.iloc[:, -1]

from sklearn.linear_model import LinearRegression
regressor = LinearRegression()

regressor.fit(X, y)

pickle.dump(regressor, open('model.pkl','wb'))

model = pickle.load(open('model.pkl','rb'))
print(model.predict([[80, 65,55 ]]))