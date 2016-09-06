import pandas as pd
from sklearn.preprocessing import StandardScaler
import numpy as np

train = pd.read_csv("train.txt", header = 0, index_col = 0, sep = "\t")
train.fillna(value=0)
index_train = train.index

columns_categorical = ['Private_appartment','Private_house','Dormitory','Rented','Other','With_parents','Higher_education','Vocational_education','Primary_education','Secondary_education','Basic_education','Male','Female','Widow','Living_with_partner','Divorced','Single','Married','Separated','Unspecified','Labourer','Retired','Public_servant','Self_employed','Other_work','Conscript','Salary_exists','Business_exists','Rent_exists','Pension_only','FOR_OTHER_PERSON','RENOVATION_OF_LIVING_PLACE','FOR_BUYING_GOODS_OR_SERVICES','FOR_TRAVELLING','FOR_OTHER_PURPOSE','FOR_STUDYING','FOR_BUYING_OTHER_REAL_ESTATE','BUSINESS','ACQUISITION_OF_SECURITIES','COMMENCING_COMMERCIAL_ACTIVITY','ACQ_OF_OTHER_FIXED_ASSETS','EXPANDING_COMMERCIAL_ACTIVITY','refin']
columns_numerical = ['age','dependants_num','work_experience','monthly_incomes','Income_sources_count','Applicant_owned_incomes_ratio','monthly_obligations','monthly_obligations_inc_refin','No_monthly_obligations','monthly_payments_to_bigbank','payment_disturbances']
train_categorical = train[columns_categorical]
train_numerical = train[columns_numerical]
header = train_numerical.columns

stds = StandardScaler()
stds = stds.fit(train_numerical)
train_numerical = stds.transform(train_numerical)

train_numerical = pd.DataFrame(data = train_numerical, columns = header, index = index_train)
train = pd.concat([train_categorical, train_numerical], axis = 1)

train.to_csv('train_transformed.txt', sep = '\t')
print('Script finished')