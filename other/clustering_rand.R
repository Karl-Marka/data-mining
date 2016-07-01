library(peplib)

PMBEC = read.csv("RAND.csv", sep=";")
rownames(PMBEC) = PMBEC[,1]
PMBEC = PMBEC[,-1]
PMBEC = data.matrix(PMBEC, rownames.force = TRUE)
default.MetricParams = new("MetricParams", smatrix=PMBEC, gapOpen=-10, gapExtension=-0.2)

#Loen peptiidid sisse
D = read.sequences("peptides.csv", header = FALSE, sep = "",
                   quote = "\"", dec = ".", fill = FALSE,
                   comment.char = "")

#Klasterdamine - 100 klastrit, aglomeratiivne, teine variant oleks "kmeans"
clusters = aclust(dist(D), 3, type = "agglomerative") 

#Panen peptiidid ja klastrite nr. kokku üheks tabeliks
clusterlist = changeClusterFormat(clusters)
D = as.data.frame(D)
D.peptides = D[,0]
clust = data.frame(clusterlist, D.peptides)

#Kirjutan faili
write.csv(clust, "clusters_output_rand.csv")
