# -*- coding: utf-8 -*-
"""regression term paper

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1hzmZI-PC8Wg1zJeT9sfJXAPm52VZH56M
"""

from google.colab import drive
drive.mount('/content/drive')

import pandas as pd

cards = pd.read_csv("/content/drive/My Drive/Colab Notebooks/itog.csv", sep = ';')
display(cards.head())

l = cards['Number of Likes']
l = [i.replace('K', '00') for i in l]
cards['Number of Likes'] = l
lq = cards['Number of Owners']
lq = [i.replace('K', '00') for i in lq]
cards['Number of Owners'] = lq
lp = cards['Volume Traded']
lp = [i.replace('K', '00') for i in lp]
cards['Volume Traded'] = lp
display(cards.head())

cards.Likes=cards.Likes.str.replace(',', '.', regex=False)
cards.Offers=cards.Offers.str.replace(',', '.', regex=False)
cards.sentiment=cards.sentiment.str.replace(',', '.', regex=False)
cards = cards.astype(float)
print(cards.dtypes)

display(cards.info()) # 데이터타입, null정보등 확인

# Commented out IPython magic to ensure Python compatibility.
from sklearn.datasets import load_boston
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression

import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

import statsmodels.api as sm
from statsmodels.stats.outliers_influence import variance_inflation_factor

# %matplotlib inline

iup = cards['Sale Price (in cryptocurrency)']
iup = [i.replace(',', '.') for i in iup]
print(iup)
cards['Sale Price (in cryptocurrency)'] = iup
display(cards.head())

#cards['Number of Likes'] = cards['Number of Likes'].astype(float)
#cards['Number of Offers'] = cards['Number of Offers'].astype(float)
cards['Sale Price (in cryptocurrency)'] = cards['Sale Price (in cryptocurrency)'].astype(float)

a = 1825

new_cards = cards.filter(['Number of Likes', 'Number of Offers', 'Sale Price (in cryptocurrency)'])
print (new_cards)

pd.isnull(cards).any()

plt.figure(figsize=(10, 6))
plt.hist(cards['Volume'], bins=10, ec='black', color ='#2196f3')
plt.xlabel('Volume cryptocurrency')
plt.ylabel('Likes')
plt.show()

plt.figure(figsize=(10, 6))
plt.hist(cards['Number of Offers'], ec='black', color ='#00796b')
plt.xlabel('Number of Offers')
plt.ylabel('Nr of assets')
plt.show()

plt.figure(figsize=(10, 6))
plt.hist(new_cards['Number of Likes'], ec='black', color ='#00776b')
plt.xlabel('Number of Likes')
plt.ylabel('Nr of assets')
plt.show()

cards.describe()

cards['Volume'].corr(cards['Likes'])

cards['Volume'].corr(cards['Offers'])

cards['Volume'].corr(cards['Twit'])

cards['Volume'].corr(cards['owners'])

cards['Volume'].corr(cards['sentiment'])

cards.corr()

plt.figure(figsize=(16,10))
sns.heatmap(cards.corr(), annot=True, annot_kws={"size": 14})
sns.set_style('white')
plt.xsticks(fontsize=14)
plt.ysticks(fontsize=14)
plt.show()

rm_tgt_corr = round(cards.corr(), 3)

plt.figure(figsize=(9, 6))

plt.title('correlation')
plt.xlabel('N', fontsize=14)
plt.ylabel('Volume', fontsize=14)
plt.show()

rm_tgt_corr = round(new_cards['Number of Likes'].corr(new_cards['Sale Price (in cryptocurrency)']), 3)

plt.figure(figsize=(9, 6))
plt.scatter(x=new_cards['Number of Likes'], y=new_cards['Sale Price (in cryptocurrency)'], alpha=0.6, s=80, color='blue')

plt.title(f'N of likes vs Price (Correlation {rm_tgt_corr})', fontsize=14)
plt.xlabel('N of likes - Median n of likes', fontsize=14)
plt.ylabel('Price', fontsize=14)
plt.show()

prices = new_cards['Sale Price (in cryptocurrency)']
features = new_cards.drop('Sale Price (in cryptocurrency)', axis =1)
X_train, X_test, y_train, y_test = train_test_split(features, prices, test_size=0.2, random_state=10)

regr = LinearRegression()
regr.fit(X_train, y_train)

print('Training data r-squared:', regr.score(X_train, y_train))
print('Test data r-squared:', regr.score(X_test, y_test))

print('Intercept', regr.intercept_)
pd.Dataframe(new_cards=regr.coef_, index=X_train.columns, columns=['coef'])

data = new_cards.drop(columns = ['Number of Twitter Followers', 'Number of Owners'],axis = 1)

print(data)

prices = data['Sale Price (in cryptocurrency)']
features = data.drop('Sale Price (in cryptocurrency)', axis =1)
X_train, X_test, y_train, y_test = train_test_split(features, prices, test_size=0.2, random_state=10)

prices = cards['Volume']
features = cards.drop('Volume', axis=1)

X_train, X_test, y_train, y_test = train_test_split(features, prices, test_size=0.2, random_state=10)

regr = LinearRegression()
regr.fit(X_train, y_train)

print('Training data r-squared:', regr.score(X_train, y_train))
print('Test data r-squared:', regr.score(X_test, y_test))

print('Intercept', regr.intercept_)

cards['Volume'].skew()

plt.figure(figsize=(10, 6))
plt.hist(cards['Volume'], bins=50, ec='black', color='#2196f3')
plt.xlabel('Volume')
plt.tlabel('Nr of assets')
plt.show()

cards['Volume'].min

prices = np.log(cards['Volume'])
features = cards.drop('Volume', axis=1)

X_train, X_test, y_train, y_test = train_test_split(features, prices, test_size=0.2, random_state=10)
regr = LinearRegression()
regr.fit(X_train, y_train)

print('Training data r-squared:', regr.score(X_train, y_train))
print('Test data r-squared:', regr.score(X_test, y_test))

print('Intercept', regr.intercept_)

X_incl_const = sm.add_constant(X_train)

model = sm.OLS(y_train, X_incl_const)
results = model.fit()

pd.DataFrame({'coef': results.params, 'p-value': round(results.pvalues, 3)})

cards.head()

variance_inflation_factor(exog=X_incl_const.values, exog_idx=1)

vif = [variance_inflation_factor(exog=X_incl_const.values, 
                          exog_idx=i) for i in range(X_incl_const.shape[1])]

pd.DataFrame({'coef_name': X_incl_const.columns, 'vif': np.around(vif, 2)})

X_incl_const = sm.add_constant(X_train)

model = sm.OLS(y_train, X_incl_const)
results = model.fit()

org_coef = pd.DataFrame({'coef': results.params, 'p-value': round(results.pvalues, 3)})

print('BIC is', results.bic)
print('r-squared is', results.rsquared)

prices = np.log(cards['Volume'])
features = cards.drop(['Volume', 'Twit', 'sentiment'], axis =1)

X_train, X_test, y_train, y_test = train_test_split(features, prices,
                                                    test_size=0.2, random_state=10)

X_incl_const = sm.add_constant(X_train)
model = sm.OLS(y_train, X_incl_const)
results = model.fit()

plt.scatter(x=results.fittedvalues, y=results.resid, c='navy', alpha=0.6)

plt.clabel('Predict log prices', fontsize=14)
plt.ylabel('Residuals', fontsize=14)

plt.show()

resid_mean = round(results.resid.mean(), 3)
resid_skew = round(results.resid.skew(), 3)

sns.displot(results.resid, color='navy')
plt.title(f'Log price model: residuals Skew ({resid_skew}) Mean ({resid_mean})')
plt.show()

reduced_log_mse = round(results.mse_resid, 3)

print('2 MSE in log', 2*np.sqrt(reduced_log_mse))

upper_bound = np.log(30) + 2*np.sqrt(reduced_log_mse)
print('The upper bound in normal volume is ', np.e**upper_bound * 1000)

lower_bound = np.log(30) - 2*np.sqrt(reduced_log_mse)
print('The lower bound in normal volume is ', np.e**lower_bound * 1000)

