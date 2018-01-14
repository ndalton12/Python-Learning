import pandas as pd
import os

train = pd.read_csv(os.path.join('data', "train.csv"))

subset_train = train[:500000]
subset_test = train[500000:]

subset_train.to_csv('train_subset.csv')
subset_test.to_csv('test_subset.csv')
