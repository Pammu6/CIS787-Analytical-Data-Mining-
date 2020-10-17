# -*- coding: utf-8 -*-
"""
Created on Tue Dec 10 11:34:09 2019

@author: KARTHEEK
"""

import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)



import pandas as pd
import numpy as np
import matplotlib.pyplot as plot
import seaborn as sns
%matplotlib inline
sns.set(style="ticks")


from sklearn import tree
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import BaggingClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import GaussianNB
from sklearn.ensemble import BaggingClassifier, RandomForestClassifier

from sklearn import model_selection
from scipy.stats import zscore



data = pd.read_excel('C:/Users/KARTHEEK SP/Desktop/ADM/Bank_Personal_Loan_Modelling.xlsx',sheet_name=1)
data.columns = ["ID","Age","Experience","Income","ZIPCode","Family","CCAvg","Education","Mortgage","PersonalLoan","SecuritiesAccount","CDAccount","Online","CreditCard"]



data.head()

data.columns

data.shape

data.info()

# No columns have null data in the file
data.apply(lambda x : sum(x.isnull()))


# Eye balling the data
data.describe().transpose()



#finding unique data
data.apply(lambda x: len(x.unique()))

sns.pairplot(data.iloc[:,1:])

# there are 52 records with negative experience. Before proceeding any further we need to clean the same
data[data['Experience'] < 0]['Experience'].count()


#clean the negative variable
dfExp = data.loc[data['Experience'] >0]
negExp = data.Experience < 0
column_name = 'Experience'
mylist = data.loc[negExp]['ID'].tolist() # getting the customer ID who has negative experience


# there are 52 records with negative experience
negExp.value_counts()


for id in mylist:
    age = data.loc[np.where(data['ID']==id)]["Age"].tolist()[0]
    education = data.loc[np.where(data['ID']==id)]["Education"].tolist()[0]
    df_filtered = dfExp[(dfExp.Age == age) & (dfExp.Education == education)]
    exp = df_filtered['Experience'].median()
    data.loc[data.loc[np.where(data['ID']==id)].index, 'Experience'] = exp

"""The ABOVE code does the below steps:

For the record with the ID, get the value of Age column
For the record with the ID, get the value of Education column
Filter the records matching the above criteria from the data frame which has records with positive experience and take the median
Apply the median back to the location which had negative experience"""

# checking if there are records with negative experience
data[data['Experience'] < 0]['Experience'].count()

data.describe().transpose()


sns.boxplot(x='Education',y='Income',hue='PersonalLoan',data=data)
#Observation : It seems the customers whose education level is 1 is having more income. However customers who has taken the personal loan have the same income levels

sns.boxplot(x="Education", y='Mortgage', hue="PersonalLoan", data=data,color='yellow')
#Observation : It seems the customers whose education level is 1 is having more income. However customers who has taken the personal loan have the same income levels

sns.countplot(x="SecuritiesAccount", data=data,hue="PersonalLoan")
#Majority of customers who does not have loan have securities account

sns.countplot(x='Family',data=data,hue='PersonalLoan',palette='Set1')
# Family size does not have any impact in personal loan. But it seems families with size of 3 are more likely to take loan. When considering future campaign this might be good association.

sns.countplot(x='CDAccount',data=data,hue='PersonalLoan')
#Customers who does not have CD account , does not have loan as well. This seems to be majority. But almost all customers who has CD account has loan as well

sns.distplot( data[data.PersonalLoan == 0]['CCAvg'], color = 'r')
sns.distplot( data[data.PersonalLoan == 1]['CCAvg'], color = 'g')

#The graph show persons who have personal loan have a 
#higher credit card average. 

print('Credit card spending of Non-Loan customers: ',data[data.PersonalLoan == 0]['CCAvg'].median()*1000)
print('Credit card spending of Loan customers    : ', data[data.PersonalLoan == 1]['CCAvg'].median()*1000)

#The average credit card spending with a median of 3800 dollar indicates a 
#Also, higher probability of personal loan. Lower credit card spending with a median of 1400 dollars is
#less likely to take a loan. This could be useful information.

fig, ax = plot.subplots()
colors = {1:'red',2:'yellow',3:'green'}
ax.scatter(data['Experience'],data['Age'],c=data['Education'].apply(lambda x:colors[x]))
plot.xlabel('Experience')
plot.ylabel('Age')

# The above plot show with experience and age have a positive correlation. As experience increase age also increases. Also the colors show the education level. There is gap in the mid 
#forties of age and also more people in the under graduate level

# Correlation with heat map
import matplotlib.pyplot as plt
import seaborn as sns
corr = data.corr()
sns.set_context("notebook", font_scale=1.0, rc={"lines.linewidth": 2.5})
plt.figure(figsize=(13,7))
# create a mask so we only see the correlation values once
mask = np.zeros_like(corr)
mask[np.triu_indices_from(mask, 1)] = True
a = sns.heatmap(corr,mask=mask, annot=True, fmt='.2f')
rotx = a.set_xticklabels(a.get_xticklabels(), rotation=90)
roty = a.set_yticklabels(a.get_yticklabels(), rotation=30)

#Income and CCAvg is moderately correlated.
#Age and Experience is highly correlated

sns.boxplot(x=data.Family,y=data.Income,hue=data.PersonalLoan)


"""Models"""

from sklearn.model_selection import train_test_split
train_set, test_set = train_test_split(data.drop(['ID','Experience'], axis=1), test_size=0.3 , random_state=100)

train_labels = train_set.pop('PersonalLoan')
test_labels = test_set.pop('PersonalLoan')

"DECISION TREE CLASSIFIER"

from sklearn.naive_bayes import GaussianNB

from sklearn.ensemble import RandomForestClassifier

dt_model=DecisionTreeClassifier(criterion = 'entropy',max_depth=3)
dt_model.fit(train_set, train_labels)


dt_model.score(test_set , test_labels)

y_predict = dt_model.predict(test_set)
y_predict[:5]


test_set.head(5)


"""NAIVE BAYES"""


naive_model = GaussianNB()
naive_model.fit(train_set, train_labels)

prediction = naive_model.predict(test_set)
naive_model.score(test_set,test_labels)


"""RANDOM FOREST CLASSIFIER"""

randomforest_model = RandomForestClassifier(max_depth=2, random_state=0)
randomforest_model.fit(train_set, train_labels)


Importance = pd.DataFrame({'Importance':randomforest_model.feature_importances_*100}, index=train_set.columns)
Importance.sort_values('Importance', axis=0, ascending=True).plot(kind='barh', color='r', )

predicted_random=randomforest_model.predict(test_set)
randomforest_model.score(test_set,test_labels)


"""KNN ( K - Nearest Neighbour ) """

train_set_indep = data.drop(['Experience' ,'ID'] , axis = 1).drop(labels= "PersonalLoan" , axis = 1)
train_set_dep = data["PersonalLoan"]
X = np.array(train_set_indep)
Y = np.array(train_set_dep)
X_Train = X[ :3500, :]
X_Test = X[3501: , :]
Y_Train = Y[:3500, ]
Y_Test = Y[3501:, ]


knn = KNeighborsClassifier(n_neighbors= 21 , weights = 'uniform', metric='euclidean')
knn.fit(X_Train, Y_Train)    
predicted = knn.predict(X_Test)
from sklearn.metrics import accuracy_score
acc = accuracy_score(Y_Test, predicted)
print(acc)


"""Model comparison"""

X=data.drop(['PersonalLoan','Experience','ID'],axis=1)
y=data.pop('PersonalLoan')
models = []
models.append(('KNN', KNeighborsClassifier()))
models.append(('CART', DecisionTreeClassifier()))
models.append(('NB', GaussianNB()))
models.append(('RF', RandomForestClassifier()))
# evaluate each model in turn
results = []
names = []
scoring = 'accuracy'
for name, model in models:
	kfold = model_selection.KFold(n_splits=10, random_state=12345)
	cv_results = model_selection.cross_val_score(model, X, y, cv=kfold, scoring=scoring)
	results.append(cv_results)
	names.append(name)
	msg = "%s: %f (%f)" % (name, cv_results.mean(), cv_results.std())
	print(msg)
# boxplot algorithm comparison
fig = plt.figure()
fig.suptitle('Algorithm Comparison')
ax = fig.add_subplot(111)
plt.boxplot(results)
ax.set_xticklabels(names)
plt.show()


#CONCLUSION: The aim of the universal bank is to convert there liability customers into loan customers. 
#They want to set up a new marketing campaign; hence, they need information about the 
#connection between the 
#variables given in the data. Four classification algorithms were used in this study. From the above 
#graph , it seems like Decision Tree algorithm have the highest accuracy and we can choose that as 
#our final model

#SOURCES:
"""
https://machinelearningmastery.com/
https://dataminingworld.wordpress.com/
"""