import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

#df1 = pd.read_csv("agent_data.csv")
#df3 = pd.read_csv("model_data.csv",index_col=False)
frames = []
keys = []
for i in range(100):
    df = pd.read_csv("data_v1/agent_data{}.csv".format(i),index_col=False)
    frames.append(df)
    keys.append('d_{}'.format(i))
df2 = pd.concat(frames,keys=keys)
#arr = df2.groupby(['influenciability'])['influenciability'].size()/len(np.unique(df2['Step']))
arr2 = df2.groupby(['Step','belief'])['belief'].size()/100
arr2.unstack().plot()
#arr2.hist()
#df3.iloc[:,1:].plot()
plt.show()
