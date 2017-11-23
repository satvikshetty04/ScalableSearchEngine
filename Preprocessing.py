# ---------------------- Importing necessary libraries
import pandas as pd
from datetime import datetime
import sys
import os
import numpy as np

# ---------------------- Reading csv file
base_dir = os.getcwd()
os.chdir(os.path.join(base_dir, "ML_Train_Folder"))
df = pd.read_csv("news_data.csv", header=None, sep="\n\n", skip_blank_lines=False)
df = pd.DataFrame(df.values.reshape(-1,8), columns=['news_title', 'news_text', 'news_link', 'news_no', 'news_date',
                                               'news_publisher', 'news_category', 'extra'])

# ---------------------- Modifying df
df.drop(['news_link','news_no','news_publisher','news_date','extra'], axis=1, inplace=True)
df['news_category'] = np.where(df['news_category'] == 'sci_tech', 'Science/Technology', df['news_category'])
df['news_category'] = np.where(df['news_category'] == 'us', 'USA', df['news_category'])
df['news_category'] = df['news_category'].str.title()

# ---------------------- Replacing null values
df['news_text'].fillna(" ", inplace=True)
df['news_title'].fillna(" ", inplace=True)

# ---------------------- Combining text columns
df['news_overall']= df['news_title'] + ' ' + df['news_text']
df.drop(['news_title','news_text'], axis=1, inplace=True)
# ---------------------- Saving csv file
df.to_csv("cleaned_news_data.csv", index=False)