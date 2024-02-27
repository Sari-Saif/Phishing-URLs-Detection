import pandas as pd
import joblib
import numpy as np
import matplotlib.pyplot as pyp
import seaborn as sns
import warnings
warnings.filterwarnings("ignore")
import preprocessing
import feacher_extraction

# load the rfc
rfc = joblib.load("rfc.joblib")

# get URL from user
url = input("Enter url: ")

# pre-processing
parsed_urls = preprocessing.pre_process([url])


# exstract feachers
df = feacher_extraction.build_df(parsed_urls)

# prepare to prediction
X_data = df.drop(["id", "url"], axis=1)

# prediction
predict_lables = rfc.predict(X_data)
print(predict_lables[0])
