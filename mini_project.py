# -*- coding: utf-8 -*-
"""mini-project.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1FPp56iCe5j_4mP5Rz4UMHX3Z2pSLB_Yx
"""

import numpy as np 
import pandas as pd 
import seaborn as sns 
import gc
import matplotlib.pyplot as plt

# Commented out IPython magic to ensure Python compatibility.
# %%time
# df_train_data = pd.read_parquet('/kaggle/input/amex-parquet/train_data.parquet')

df_train_data.shape

"""# After feature engineering, requied preprocessing done directly on dataset

Categorical data to separate columns, but only some of the categories are dropped
"""

temp = pd.get_dummies(df_train_data["D_64"], prefix='D_64')
for i in ['O', 'R', 'U']:
    df_train_data["D_64"+i] = temp["D_64_"+i]
temp = pd.get_dummies(df_train_data["D_63"], prefix='D_63')
for i in ['CL', 'CO', 'CR']:
    df_train_data["D_63"+i] = temp["D_63_"+i]

"""drop identified columns during feature engineering"""

drop_cols = ['R_26', 'D_132', 'D_134', 'D_141', 'R_9', 'D_75', 'D_119', 'B_14', 'D_104', 
             'D_110', 'D_108', 'S_24', 'D_49', 'B_39', 'B_42', 'D_77', 'S_7', 'B_15', 
             'D_42', 'B_33', 'S_22', 'D_58', 'D_87', 'B_23', 'B_7', 'D_118', 'S_2', 
             'D_137', 'D_111', 'D_106', 'B_37', 'B_11', 'D_66', 'D_76', 'B_1', 'B_29', 
             'D_138', 'D_64', 'D_143', 'D_136', 'D_139', 'B_2', 'customer_ID', 'D_74', 
             'D_142', 'D_135', 'D_62', 'D_63', 'D_73', 'S_3', 'D_88', 'D_103']

df_train_data = df_train_data.drop(drop_cols,axis=1)

df_train_data.shape

"""fill missing values with median"""

for column in df_train_data.columns:
    median = df_train_data[column].median()
    df_train_data[column] = df_train_data[column].fillna(median)
df_train_data.head()

"""<a id='section1'></a>
# Feature Engineering

# Categorical data
1. only columns which does not have numerical values are considered.
2. unique values are checked and graphed, graphed with target as well
3. values with low count and original columns are dropped
"""

num_cols = dgf_train_data._get_numeric_data().columns
cate_cols = list(set(df_train_data.columns) - set(num_cols))

cate_cols

df_train_data['D_64'].unique()

df_train_data.groupby('D_64')['customer_ID'].nunique()

# no need
# S_2 column split to year, month,day
# impact of year, month, day was unnoticable, were not added to dataset
date = pd.to_datetime(df_train_data['S_2'])

df_train_data['year'] = date.dt.year
df_train_data['month'] = date.dt.month
df_train_data['day'] = date.dt.day

plt.figure(figsize=(20, 30))
for i, k in enumerate(["D_63","D_64","S_2"]):
    plt.subplot(6, 2, i+1)
    temp_val = pd.DataFrame(df_train_data[k].value_counts(dropna=False, normalize=True).sort_index().rename('count'))
    temp_val.index.name = 'value'
    temp_val.reset_index(inplace=True)
    plt.bar(temp_val.index, temp_val['count'], alpha=0.5)
    plt.xlabel(k)
    plt.ylabel('frequency')
    plt.xticks(temp_val.index, temp_val.value)
plt.show()

plt.figure(figsize=(20, 30))
for i, f in enumerate(["D_63","D_64", "year","month","day"]):
    plt.subplot(6, 2, i+1)
    temp = pd.DataFrame(df_train_data[f][df_train_data.target == 0].value_counts(dropna=False, normalize=True).sort_index().rename('count'))
    temp.index.name = 'value'
    temp.reset_index(inplace=True)
    plt.bar(temp.index, temp['count'], alpha=0.5, label='target=0')
    temp = pd.DataFrame(df_train_data[f][df_train_data.target == 1].value_counts(dropna=False, normalize=True).sort_index().rename('count'))
    temp.index.name = 'value'
    temp.reset_index(inplace=True)
    plt.bar(temp.index, temp['count'], alpha=0.5, label='target=1')
    plt.xlabel(f)
    plt.ylabel('frequency')
    plt.legend()
    plt.xticks(temp.index, temp.value)
plt.show()

temp = pd.get_dummies(df_train_data["D_64"], prefix='D_64')
for i in ['O', 'R', 'U']:
    df_train_data["D_64"+i] = temp["D_64_"+i]
temp = pd.get_dummies(df_train_data["D_63"], prefix='D_63')
for i in ['CL', 'CO', 'CR']:
    df_train_data["D_63"+i] = temp["D_63_"+i]

df_train_data = df_train_data.drop(cate_cols, axis=1)
del temp
gc.collect()

"""# Handling missing values
1. Columns with more than 80% missing values are dropped
2. Other missing values are filled with median
"""

missing_data = pd.DataFrame(df_train_data.isnull().sum()/len(df_train_data))
need_drop = missing_data.loc[missing_data[0] >= 0.8]
print('number of column w/ >= 80% missing value = ', len(need_drop))

cols_need_drop = list(need_drop.T.columns)
df_train_data = df_train_data.drop(cols_need_drop, axis=1)
del need_drop,missing_data
gc.collect()

for column in df_train_data.columns:
    median = df_train_data[column].median()
    df_train_data[column] = df_train_data[column].fillna(median)
df_train_data.head()
del median
gc.collect()

"""# Class imbalance
1. Target values with 0, resampled to the count of target with 1 value.
2. Did not applied to some of the models
3. Helped with kaggle RAM exceeding issue
"""

draw_chart = pd.DataFrame(df_train_data['target'].value_counts()).T
print('percentage of target value 0 / 1 = ', draw_chart[1]/draw_chart[0], '\n\n\n');
draw_chart.plot.barh(align='edge', width=0.5);
del draw_chart
gc.collect()

df_train_data.shape

target_0 = df_train_data[df_train_data['target']==0]
target_1 = df_train_data[df_train_data['target']==1]
del df_train_data
gc.collect()

target_0.shape

target_1.shape

df_sample = target_0.sample(n=1377869, random_state=42)

df_train_data = pd.concat([df_sample, target_1])

del target_0,target_1,df_sample
gc.collect()
df_train_data.shape



"""**Tried do PCA, was not possible due to not availability of enough memory**"""

# cannot run. not enough memory available
from sklearn.decomposition import PCA
import seaborn as sns
# Create principal components
pca = PCA()
X_pca = pca.fit_transform(df_train_data.drop(['target'],axis=1))

# Convert to dataframe
component_names = [f"PC{i+1}" for i in range(df_train_data.shape[1]-1)]
X_pca = pd.DataFrame(X_pca, columns=component_names)

#X_pca.head()
df = pd.DataFrame({'var':pca.explained_variance_ratio_,
             'PC':component_names})
sns.barplot(x='PC',y="var", 
           data=df, color="c");
df[df['var']>0.15]

"""**Columns with more than 90% correlation are dropped**"""

correlation_mat = df_train_data.corr()
correlation_mat["target"]
correlated_columns = correlation_mat.where(abs(correlation_mat) > 0.9).stack().index.tolist()

# remove correlated columns >90%
drop_correlated_columns = []
for col1, col2 in correlated_columns:
    if col1 != col2:
        drop_correlated_columns.append(col2)
drop_correlated_columns

df_train_data = df_train_data.drop(drop_correlated_columns, axis=1)

"""**Tried removing columns with less correlation with target**

**Only for some models**
"""

#no need to run, relationship might not be linear
# drop columns with less correlation with target
cols_corr_drop = correlation_mat[(correlation_mat["target"]<0.05) & (correlation_mat["target"]>-0.05)].T.columns
for col in cols_corr_drop:
    if col in df_train_data.columns:
        df_train_data = df_train_data.drop(col, axis=1)

del correlation_mat,correlated_columns
gc.collect()

df_train_data.shape

# all dropped columns are saved in a list, posiible to drop without running above cells again
drop_cols = cate_cols
drop_cols.extend(cols_need_drop)
drop_cols.extend(drop_correlated_columns)
drop_cols = list(set(drop_cols))
len(drop_cols)

print(drop_cols)

df_train_data.shape

"""**Separating target from features and**

**MIN MAX scaling features**
"""

X = df_train_data.drop('target',axis=1)
y = df_train_data['target']
del df_train_data
gc.collect()

from sklearn.preprocessing import MinMaxScaler


scaler = MinMaxScaler()
X = scaler.fit_transform(X)

import pickle

# Save the scaler to a file
with open('scaler.pickle', 'wb') as f:
    pickle.dump(scaler, f)

"""**Splitting data train = 80%, test = 20%**"""

from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

x_train,x_test,y_train,y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)
del X,y
gc.collect()

def amex_metric(y_true: pd.DataFrame, y_pred: pd.DataFrame) -> float:

    def top_four_percent_captured(y_true: pd.DataFrame, y_pred: pd.DataFrame) -> float:
        df = (pd.concat([y_true, y_pred], axis='columns')
              .sort_values('prediction', ascending=False))
        df['weight'] = df['target'].apply(lambda x: 20 if x==0 else 1)
        four_pct_cutoff = int(0.04 * df['weight'].sum())
        df['weight_cumsum'] = df['weight'].cumsum()
        df_cutoff = df.loc[df['weight_cumsum'] <= four_pct_cutoff]
        return (df_cutoff['target'] == 1).sum() / (df['target'] == 1).sum()
        
    def weighted_gini(y_true: pd.DataFrame, y_pred: pd.DataFrame) -> float:
        df = (pd.concat([y_true, y_pred], axis='columns')
              .sort_values('prediction', ascending=False))
        df['weight'] = df['target'].apply(lambda x: 20 if x==0 else 1)
        df['random'] = (df['weight'] / df['weight'].sum()).cumsum()
        total_pos = (df['target'] * df['weight']).sum()
        df['cum_pos_found'] = (df['target'] * df['weight']).cumsum()
        df['lorentz'] = df['cum_pos_found'] / total_pos
        df['gini'] = (df['lorentz'] - df['random']) * df['weight']
        return df['gini'].sum()

    def normalized_weighted_gini(y_true: pd.DataFrame, y_pred: pd.DataFrame) -> float:
        y_true_pred = y_true.rename(columns={'target': 'prediction'})
        return weighted_gini(y_true, y_pred) / weighted_gini(y_true, y_true_pred)

    g = normalized_weighted_gini(y_true, y_pred)
    d = top_four_percent_captured(y_true, y_pred)

    return 0.5 * (g + d)

"""# Model training

**Methods tried**
"""

from sklearn.naive_bayes import GaussianNB
from sklearn.ensemble import RandomForestClassifier
from sklearn import svm
from sklearn.neighbors import KNeighborsClassifier
from xgboost import XGBClassifier
from sklearn.linear_model import LogisticRegression
import lightgbm as lgb

from sklearn import metrics



"""**GaussianNB**"""

classifier = GaussianNB()
classifier.fit(x_train, y_train)

print(f'Training accuracy: {classifier.score(x_test, y_test)}')

y_pred  =  classifier.predict(x_test)
print(amex_metric(pd.DataFrame(y_test,columns=['target']), pd.DataFrame(y_pred,columns=["prediction"]))) 
print("Accuracy:",metrics.accuracy_score(y_test, y_pred))

# Save the model to a file
with open('/kaggle/working/gaussianNB.pkl', 'wb') as f:
  pickle.dump(classifier, f)

del classifier
gc.collect()

"""**SVM**"""

SVM = svm.SVC(kernel='linear',C=1.3,degree=8,cache_size=300) 
SVM.fit(x_train, y_train)

y_pred=SVM.predict(x_test)
print(amex_metric(pd.DataFrame(y_test,columns=['target']), pd.DataFrame(y_pred,columns=["prediction"]))) 
print("Accuracy:",metrics.accuracy_score(y_test, y_pred))

# Save the model to a file
with open('/kaggle/working/gaussianNB.pkl', 'wb') as f:
  pickle.dump(classifier, f)

"""**KNN**"""

model = KNeighborsClassifier(n_neighbors=20,n_jobs=-1)
model.fit(X,y)

y_pred=model.predict(test_X)
print(amex_metric(pd.DataFrame(y_test,columns=['target']), pd.DataFrame(y_pred,columns=["prediction"]))) # 0.572773
print("Accuracy:",metrics.accuracy_score(y_test, y_pred))

# Save the model to a file
with open('/kaggle/working/knn.pkl', 'wb') as f:
  pickle.dump(model, f)

del model
gc.collect()

"""**Logistic regrassion**"""

logistic_reg = LogisticRegression()
logistic_reg.fit(x_train, y_train)

y_pred=logistic_reg.predict(x_test)
print(amex_metric(pd.DataFrame(y_test,columns=['target']), pd.DataFrame(y_pred,columns=["prediction"])))
print("Accuracy:",metrics.accuracy_score(y_test, y_pred))

# Save the model to a file
with open('/kaggle/working/logistic_reg.pkl', 'wb') as f:
  pickle.dump(logistic_reg, f)

del logistic_reg
gc.collect()

"""**XGBoost**"""

xgb = XGBClassifier(
            learning_rate=0.02,
            n_estimators=20,
            objective="binary:logistic",
            nthread=4
        )
xgb.fit(x_train, y_train)

y_pred  =  xgb.predict(x_test)
print(amex_metric(pd.DataFrame(y_test,columns=['target']), pd.DataFrame(y_pred,columns=["prediction"]))) # 0.572773
print(f'Accuracy: {xgb.score(x_test, y_test)}')

with open('/kaggle/working/xgb_model2.pkl', 'wb') as f:
  pickle.dump(xgb, f)

"""**LightGBM**"""

d_train = lgb.Dataset(x_train, label=y_train)
params = {'objective': 'binary','metric': 'binary_logloss','boosting': 'gbdt','num_leaves': 100,'reg_lambda' : 60,'colsample_bytree': 0.2,'learning_rate': 0.02,'min_child_samples': 2400,'max_bins': 600,'seed': 42,'verbose': -1}
lgb_model = lgb.train(params, d_train, 300)

y_pred  =  lgb_model.predict(x_test)
y_pred[y_pred>=0.5] = 1
y_pred[y_pred <0.5] = 0
print(amex_metric(pd.DataFrame(y_test,columns=['target']), pd.DataFrame(y_pred,columns=["prediction"]))) # 0.572773
print("Accuracy:",metrics.accuracy_score(y_test, y_pred))

with open('/kaggle/working/lgb_model2.pkl', 'wb') as f:
  pickle.dump(lgb_model, f)

del lgb_model #x_train,x_test,y_train,y_test
gc.collect()

del x_train,x_test,y_train,y_test
gc.collect()

drop_cols

test_dataset = pd.read_parquet('/kaggle/input/amex-parquet/test_data.parquet')
test_dataset.head()

test_dataset = test_dataset.groupby('customer_ID').tail(1).set_index('customer_ID', drop=True).sort_index()

"""**Adding created columns**"""

temp = pd.get_dummies(test_dataset["D_64"], prefix='D_64')
for i in ['O', 'R', 'U']:
    test_dataset["D_64"+i] = temp["D_64_"+i]
temp = pd.get_dummies(test_dataset["D_63"], prefix='D_63')
for i in ['CL', 'CO', 'CR']:
    test_dataset["D_63"+i] = temp["D_63_"+i]

"""**Drop columns**"""

test_dataset = test_dataset.drop(col,axis=1)

test_dataset.shape



"""**Fill missing with median**"""

for column in test_dataset.columns:
    if column=='customer_ID': continue
    median = test_dataset[column].median()
    test_dataset[column] = test_dataset[column].fillna(median)
test_dataset.head()

"""**Load same scaler function and scale test dataset**"""

with open('scaler.pickle', 'rb') as f:
    scaler = pickle.load(f)
test_X = scaler.fit_transform(test_dataset)

"""**Load saved model**"""

with open('/kaggle/working/xgb_model2.pkl', 'rb') as f:
  model = pickle.load(f)

y_pred  =  model.predict(X)

# only for lightgbm
y_pred[y_pred>=0.5] = 1
y_pred[y_pred <0.5] = 0

y_pred.shape

sample_dataset = pd.read_csv('/kaggle/input/amex-default-prediction/sample_submission.csv')

output = pd.DataFrame({'customer_ID': sample_dataset.customer_ID, 'prediction': y_pred.astype(int)})

output.head()

"""**Save submissions as a csv**"""

output.to_csv('submission_lgb5.csv', index=False)

