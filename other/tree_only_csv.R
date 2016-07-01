library("randomForest")

train = read.csv("training.csv", sep=";")

train2 = as.data.frame(train[,-(1:2)])
lapply(train2, as.numeric)
train_max = max(train2)

train2[train2<10] = 0
train2[train2 == 1000] = 999
train2[train2 == 500] = 499
train2[train2 == 400] = 399
train2[train2 == 300] = 299
train2[train2 == 200] = 199
train2[train2 == 100] = 99
train2[train2 == 75] = 74
train2[train2 == 50] = 49
train2[train2 == 25] = 24
train2[train2 == 12] = 11
train2[train2>19999] = 1000
train2[train2>(0.5*train_max) & train2 != 1000] = 500
train2[train2>(0.4*train_max) & train2 != 500] = 400
train2[train2>(0.3*train_max) & train2 != 400 & train2 != 500] = 300
train2[train2>(0.2*train_max) & train2 != 300 & train2 != 400 & train2 != 500] = 200
train2[train2>(0.1*train_max) & train2 != 200 & train2 != 300 & train2 != 400 & train2 != 500] = 100
train2[train2>(0.075*train_max) & train2 != 100 & train2 != 200 & train2 != 300 & train2 != 400 & train2 != 500] = 75
train2[train2>(0.05*train_max) & train2 != 75 & train2 != 100 & train2 != 200 & train2 != 300 & train2 != 400 & train2 != 500] = 50
train2[train2>(0.025*train_max) & train2 != 50 & train2 != 75 & train2 != 100 & train2 != 200 & train2 != 300 & train2 != 400 & train2 != 500] = 25
train2[train2>(0.012*train_max) & train2 != 25 & train2 != 50 & train2 != 75 & train2 != 100 & train2 != 200 & train2 != 300 & train2 != 400 & train2 != 500] = 12
train2[train2>(0.005*train_max) & train2 != 12 & train2 != 25 & train2 != 50 & train2 != 75 & train2 != 100 & train2 != 200 & train2 != 300 & train2 != 400 & train2 != 500] = 5
train2[train2>(0.002*train_max) & train2 != 5 & train2 != 12 & train2 != 25 & train2 != 50 & train2 != 75 & train2 != 100 & train2 != 200 & train2 != 300 & train2 != 400 & train2 != 500] = 3
train2[train2>(0.001*train_max) & train2 != 2 & train2 != 5 & train2 != 12 & train2 != 25 & train2 != 50 & train2 != 75 & train2 != 100 & train2 != 200 & train2 != 300 & train2 != 400 & train2 != 500] = 2
train2[train2>(0.0005*train_max) & train2 != 1 & train2 != 2 & train2 != 5 & train2 != 12 & train2 != 25 & train2 != 50 & train2 != 75 & train2 != 100 & train2 != 200 & train2 != 300 & train2 != 400 & train2 != 500 ] = 1

train_frows = train[1:2]
train = cbind(train_frows, train2)

rf = randomForest(status ~ .,
                   data=train,
                   ntree=5000,
                   importance=TRUE,
                   na.action=na.roughfix,
                   replace=FALSE)

pep_weights = importance(rf, type =1)
write.csv(pep_weights, "peptide_weights.csv")

