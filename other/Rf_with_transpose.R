library("randomForest")

# loen andmed sisse
data = read.csv("data.csv", header = FALSE, sep=";")
columns = read.csv("columns.csv", header = FALSE, sep=";")
rows = read.csv("rows.csv", header = FALSE, sep=";")

# transponeerin peptiidide counte sisaldava faili
train2 = as.data.frame(t(data))
row.names(train2) = NULL

# leian maksimaalse counti
train_max = max(train2)

# muudan peptiidide countid diskreetseteks muutujateks
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

# panen transponeeritud ja diskreetsete muutujatega asendatud tabelile kolonnide
# nimedeks vastavate peptiidide järjestused
rows2 = rows[-c(1, 2),]
rows2 = unlist(rows2)
rows2 = as.data.frame(rows2)
rows2 = unlist(rows2)
colnames(train2) = rows2

# liidan tabelile otsa neg. või pos. staatust indikeeriva kolonni
status = columns[2,-1]
row.names(status) = NULL
status = t(status)
row.names(status) = NULL
train = cbind(status, train2)

# teostan random foresti
rf = randomForest(status ~ .,
                   data=train,
                   ntree=5000,
                   importance=TRUE,
                   na.action=na.roughfix,
                   replace=FALSE)

# kirjutan välja faili
pep_weights = importance(rf, type =1)
write.csv(pep_weights, "peptide_weights.csv")

