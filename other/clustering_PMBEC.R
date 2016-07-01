library(peplib)

PMBEC = read.csv("PMBEC.csv", sep=";")
rownames(PMBEC) = PMBEC[,1]
PMBEC = PMBEC[,-1]
PMBEC = data.matrix(PMBEC, rownames.force = TRUE)
PMBEC = new("MetricParams", smatrix=PMBEC, gapOpen=-10, gapExtension=-0.2)

D = read.sequences("peptides.csv", header = FALSE, sep = "",
                   quote = "\"", dec = ".", fill = FALSE,
                   comment.char = "")

PepM = dist(D, method="substitution", params=PMBEC)
  
clusters = aclust(PepM, 3, type = "agglomerative") 

clusterlist = changeClusterFormat(clusters)
D = as.data.frame(D)
D.peptides = D[,0]
clust = data.frame(clusterlist, D.peptides)

write.csv(clust, "clusters_output.csv")
