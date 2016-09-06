import pandas as pd
from sklearn.preprocessing import StandardScaler
import xgboost as xgb
from sklearn.metrics import confusion_matrix
import numpy as np

train = pd.read_csv("train.txt", header = 0, index_col = 0, sep = "\t")
labels_train = pd.read_csv("labels_train.txt", header = None, index_col = None, sep = "\t")
labels_train = labels_train.unstack().tolist()
labels_test = pd.read_csv("labels_test.txt", header = None, index_col = None, sep = "\t")
labels_test = labels_test.unstack().tolist()
test = pd.read_csv("test.txt", header = 0, index_col = 0, sep = "\t")
train.fillna(value=0)
test.fillna(value=0)
index_train = train.index
index_test = test.index

columns_categorical = ['Private_appartment','Private_house','Dormitory','Rented','Other','With_parents','Higher_education','Vocational_education','Primary_education','Secondary_education','Basic_education','Male','Female','Widow','Living_with_partner','Divorced','Single','Married','Separated','Unspecified','Labourer','Retired','Public_servant','Self_employed','Other_work','Conscript','Salary_exists','Business_exists','Rent_exists','Pension_only','FOR_OTHER_PERSON','RENOVATION_OF_LIVING_PLACE','FOR_BUYING_GOODS_OR_SERVICES','FOR_TRAVELLING','FOR_OTHER_PURPOSE','FOR_STUDYING','FOR_BUYING_OTHER_REAL_ESTATE','BUSINESS','ACQUISITION_OF_SECURITIES','COMMENCING_COMMERCIAL_ACTIVITY','ACQ_OF_OTHER_FIXED_ASSETS','EXPANDING_COMMERCIAL_ACTIVITY','refin']
columns_numerical = ['age','dependants_num','work_experience','monthly_incomes','Income_sources_count','Applicant_owned_incomes_ratio','monthly_obligations','monthly_obligations_inc_refin','No_monthly_obligations','monthly_payments_to_bigbank','payment_disturbances']
train_categorical = train[columns_categorical]
train_numerical = train[columns_numerical]
test_categorical = test[columns_categorical]
test_numerical = test[columns_numerical]
header = train_numerical.columns

stds = StandardScaler()
stds = stds.fit(train_numerical)
train_numerical = stds.transform(train_numerical)
test_numerical = stds.transform(test_numerical)
train_numerical = pd.DataFrame(data = train_numerical, columns = header, index = index_train)
test_numerical = pd.DataFrame(data = test_numerical, columns = header, index = index_test)
train = pd.concat([train_categorical, train_numerical], axis = 1)
test = pd.concat([test_categorical, test_numerical], axis = 1)

# F-score in 99th percentile
params = ['Single','monthly_obligations','refin','BUSINESS','Male','Conscript','Dormitory','ACQUISITION_OF_SECURITIES','FOR_BUYING_GOODS_OR_SERVICES','monthly_obligations_inc_refin','Income_sources_count','payment_disturbances','Female','Applicant_owned_incomes_ratio','monthly_payments_to_bigbank','Other_work','Married','Other','Separated','EXPANDING_COMMERCIAL_ACTIVITY','Vocational_education','COMMENCING_COMMERCIAL_ACTIVITY','No_monthly_obligations','Pension_only','Rented','work_experience','Labourer','Business_exists','dependants_num']
train = train[params]
test = test[params]

clr = xgb.XGBClassifier(max_depth = 3, n_estimators = 100, objective = 'reg:linear')
xgb_model = clr.fit(train,labels_train)
predictions_train = xgb_model.predict(train)
predictions_test = xgb_model.predict(test)
predictions_train_proba = xgb_model.predict_proba(train)
predictions_test_proba = xgb_model.predict_proba(test)

predictions_train_proba = list(predictions_train_proba)
predictions_test_proba = list(predictions_test_proba)
print(predictions_train_proba)
print(predictions_test_proba)

MSE_train = np.mean((predictions_train - labels_train)**2)
MSE_test = np.mean((predictions_test - labels_test)**2)

print('MSE on the training set:',MSE_train)
print('MSE on the testing set:',MSE_test)

f = open('predictions_train_proba_xgboost.txt', 'w')
for i in predictions_train_proba:
  f.write("%s\n" % i)
f.close()

f = open('predictions_test_proba_xgboost.txt', 'w')
for i in predictions_test_proba:
  f.write("%s\n" % i)
f.close()

predictions_train = list(predictions_train)
f = open('predictions_train_xgboost.txt', 'w')
for i in predictions_train:
  f.write("%s\n" % i)
f.close()

predictions_test = list(predictions_test)
f = open('predictions_test_xgboost.txt', 'w')
for i in predictions_test:
  f.write("%s\n" % i)
f.close()





