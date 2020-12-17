#%%
from sklearn.datasets import load_iris
iris = load_iris()
X=iris.data
Y=iris.target


# %%
from sklearn.naive_bayes import GaussianNB,MultinomialNB
gnb = GaussianNB()
gnb.fit(X,Y)
# %%
X_new = X[0:10,:]
# %%
y_hat=gnb.predict(X_new)
print(y_hat)
# %%
Y_hat = gnb.predict(X)
print(Y_hat)




# %%
import pandas as pd
df = pd.read_csv('credit.csv')
df.head()
# %%
X=df.iloc[:,2:]
y=df.iloc[:,0:1]


# %%
mnb = MultinomialNB()

# %%
mnb.fit(X,y)
y_hat=mnb.predict(X)
y_hat


#%%
X = df.iloc[:,1:]
y = df.Credit_rating
X
# %%
from mixed_naive_bayes import MixedNB
mnb = MixedNB(categorical_features=[1,2,3,4])

# %%
mnb.fit(X,y)
# %%
from sklearn.preprocessing import LabelEncoder
lm = LabelEncoder()
lm.fit([1,2,3])

# %%
X_1 = X
X_1.iloc[:,1:2] = lm.transform(X.iloc[:,1:2])
X_1.iloc[:,2:3] = lm.transform(X.iloc[:,2:3])
X_1.iloc[:,3:4] = lm.transform(X.iloc[:,3:4])
X_1.iloc[:,4:5] = lm.transform(X.iloc[:,4:5])

# %%
mnb.fit(X_1,y)
# %%
y_hat=mnb.predict(X_1)
y_hat
# %%
