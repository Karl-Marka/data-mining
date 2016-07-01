library(peplib)

#Kasutan blosum90 maatriksit, kuna raamatukogu on ainult subset
data(blosum90)
default.MetricParams = new("MetricParams", smatrix=blosum90, gapOpen=-10, gapExtension=-0.2)

#Loen peptiidid sisse
D = read.sequences("peptides.csv", header = FALSE, sep = "",
                   quote = "\"", dec = ".", fill = FALSE,
                   comment.char = "")

#Klasterdamine - 500 klastrit, kmeans, teine variant oleks "agglomerative"
clusters = aclust(dist(D), 50, type = "kmeans", knstart = 20) 

#Panen peptiidid ja klastrite nr. kokku üheks tabeliks
clusterlist = changeClusterFormat(clusters)
D = as.data.frame(D)
D.peptides = D[,0]
clust = data.frame(clusterlist, D.peptides)

#Kirjutan faili
write.csv(clust, "clusters_output.csv")
