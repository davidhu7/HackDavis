import pandas as pd
import tensorflow as tf 
from tensorflow import keras




model = tf.keras.models.load_model('./MLmodels/games.h5')
dataset= pd.read_csv("./MLmodels/data.csv")

def get_prediction(name,year):
    data = dataset.loc[(dataset["name"]==name) & (dataset["yearID"] == year)].copy()
    data.drop(["yearID","name"],axis=1,inplace=True)
    datas =data.copy()
    if len(datas.index)!=0:
       prediction = model.predict(datas.values)
       return prediction
    return 0

print(get_prediction("Arizona Diamondbacks",2001))