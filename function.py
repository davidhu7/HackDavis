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
       return float(prediction)
    return 0

if __name__ == '__main__':
    print(get_prediction('Seattle Mariners', 2010))

