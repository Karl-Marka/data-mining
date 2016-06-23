args <- commandArgs(trailingOnly = TRUE)
study<-"test"
#beta.use<-args[1]
#patientID<-args[2]
#patientAge<-args[3]
#patientW<-args[4]
#duration<-args[5]
#type<-args[6]

beta.use<-"all"
patientID<-"T1"
patientAge<-50
patientW<-1
duration<-6
type<-0
SP5<- -3.033409916
CTGF<- 1.06301696
COL4A2<- 1.76062184
COL4A1<- 2.29213032
GPX1<- -0.19931568

#SP5<- as.character(SP5)
#CTGF<- as.character(CTGF)
#COL4A2<- as.character(COL4A2)
#COL4A1<- as.character(COL4A1)
#GPX1<- as.character(GPX1)

print("Running algorithm", quote = FALSE)


if(beta.use!="gene"){
	beta.use<-"all"
}

hk<-"hk_ssp_5.txt"

if(beta.use=="all"){
	beta<-"beta.txt"
}
if(beta.use=="gene"){
	beta<-"beta_gene.txt"
}

data<-"data.pcl"


set.seed(123)

dir<-"."

dir.study<-file.path(dir,study)

#dir.out<-file.path(dir,study,"out")
dir.out<-dir.study

if (file.exists(file.path(dir.out))){
} else {
	dir.create(file.path(dir.out))
}


beta.all<-read.table(file.path(dir,beta),sep="\t",header=TRUE,check.names=FALSE)
rownames(beta.all)<-beta.all[,1]
beta.all<-beta.all[,-1,drop=FALSE]


#expr.ori<-read.csv(file.path(dir.study,data),sep="\t",header=TRUE,check.names=FALSE)

genes = c("EWEIGHT", "AGI_HUM1_OLIGO_A_23_P135381", "AGI_HUM1_OLIGO_A_23_P19663", "AGI_HUM1_OLIGO_A_23_P205031", "AGI_HUM1_OLIGO_A_23_P65240", "A_33_P3239849")
names = c(" ", "SP5", "CTGF", "COL4A2", "COL4A1", "GPX1")
gweight = c(1,1,1,1,1,1)
exprData = c(1, SP5, CTGF, COL4A2, COL4A1, GPX1)
nameslist = c("CLID", "NAME", "GWEIGHT", patientID)
expr.ori = cbind(genes, names, gweight, exprData)
colnames(expr.ori) = nameslist
expr.ori = as.data.frame(expr.ori, stringsAsFactors = FALSE)
#expr.ori[,1]<-as.character(expr.ori[,1])
expr.ori[,4] = as.numeric(expr.ori[,4])

str(expr.ori)

expr<-expr.ori[-1,]
rownames(expr)<-expr[,1]

array.name<-"NAME"
ID<-"CLID"

expr<-expr[,-(1:3),drop=FALSE]


str(expr)

clinic.dat = data.frame(patientID, 6, as.numeric(patientAge), as.numeric(duration), as.numeric(patientW), as.numeric(type))
colnames(clinic.dat) = c("NAME", "Biopsy.Time", "Age", "Disease.Duration", "EthnicityW", "SSc.TypelcSSc")


arraynames<-colnames(expr)
common<-which((arraynames %in% clinic.dat[,array.name]))
expr<-expr[,common,drop=FALSE]
arraynames<-arraynames[common]
clinic.dat<-clinic.dat[match(arraynames,clinic.dat[,array.name]),]


rownames(beta.all)[which(rownames(beta.all) %in% expr.ori$NAME)]<-as.character(expr.ori[,ID][match(rownames(beta.all)[which(rownames(beta.all) %in% expr.ori$NAME)],expr.ori$NAME)])


#if(hk=="no"){
	#expr.adj<-normalizeQuantiles(expr)

	#scale.m<-scale(t(expr.adj),center=TRUE, scale=TRUE)
	#expr.adj<-t(scale.m)
#}else{
	hk.gene<-read.table(file.path(dir,hk),sep="\t",header=FALSE)
	scale.ref<-read.csv(file.path(dir,"reference_hk_ssp_5.txt"),sep="\t",header=TRUE)
	scale.ref$NAME<-do.call("rbind",strsplit(as.character(scale.ref$NAME),"\\^"))[,1]
	scale.ref$NAME<-sub(" ","",scale.ref$NAME)

	scale.ref<-scale.ref[match(expr.ori$NAME,scale.ref$NAME),]
	rownames(scale.ref)<-rownames(expr.ori)

	hk.gene[,1]<-as.character(expr.ori[match(hk.gene[,2],expr.ori$NAME),ID])
	scale.ref[,1]<-as.character(expr.ori[match(scale.ref[,2],expr.ori$NAME),ID])

	common<-which(rownames(expr) %in% scale.ref[,1])
	expr<-expr[common,,drop=FALSE]
	scale.ref<-scale.ref[match(rownames(expr),scale.ref[,1]),]
	

	expr.adj<-matrix(rep(scale.ref$reference[1]-colMeans(expr,na.rm=TRUE),nrow(expr)),nrow=nrow(expr),byrow=TRUE)+expr

	expr.adj<-(expr.adj-matrix(rep(scale.ref$center,ncol(expr.adj)),nrow=nrow(expr),byrow=FALSE))/matrix(rep(scale.ref$scale,ncol(expr.adj)),nrow=nrow(expr),byrow=FALSE)
#}

#expr.out<-expr.adj
#expr.out<-cbind(name.mat[match(rownames(expr.out),name.mat[,1]),],expr.out)
#write.table(expr.out,file=file.path(dir.out.s, "data_scaled.txt"),sep="\t",row.names=FALSE,col.names=TRUE,quote=FALSE)

expr.adj<-expr.adj[which(rownames(expr.adj) %in% rownames(beta.all)),,drop=FALSE]

x.vec<-t(as.matrix(expr.adj))

aa.vec<-rownames(expr.adj)[which(rownames(expr.adj) %in% rownames(beta.all))]

var.vec<-rownames(beta.all)
dat.lm<-clinic.dat[,which(colnames(clinic.dat) %in% c(var.vec))]
dat.lm<-cbind(dat.lm,x.vec)
rownames(dat.lm)<-clinic.dat$NAME


#2nd step, risk score

if(beta.use=="all"){
	beta.all<-beta.all[c(1,which(rownames(beta.all) %in% colnames(dat.lm))),,drop=FALSE]
}
if(beta.use=="gene"){
	beta.all<-beta.all[c(1,which(rownames(beta.all) %in% aa.vec)),,drop=FALSE]
}

pred_validation<-as.matrix(cbind(rep(1,nrow(dat.lm)),dat.lm[,match(rownames(beta.all)[-1],colnames(dat.lm))])) %*% as.matrix(beta.all)
names(pred_validation)<-rownames(dat.lm)

useroutput = data.frame(pred_validation)
useroutput = useroutput[,1]
printout = paste("Disease score for patient", patientID, ":", useroutput, sep = " ")
print(printout, quote = FALSE)
printout2 = paste("Disease score value was also written to: test/", patientID, "_", beta.use, ".txt", sep = "")
print(printout2, quote = FALSE)



names(pred_validation)<-rownames(dat.lm)

header = c("Patient ID:", "Patient age:", "Disease duration:", "Disease score:")
datarow = c(patientID, patientAge, duration, useroutput)
emptyrow = c("    ","    ")
disclaimer = c("Hither shall be a disclaimer...", "    ")
tableout = rbind((cbind(header, datarow)), emptyrow, emptyrow, disclaimer)

write.table(tableout,file=file.path(dir.out, paste(patientID,"_",beta.use,".txt",sep="")),sep="\t",row.names=FALSE,col.names=FALSE,quote=FALSE)
