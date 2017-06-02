# Question 1
library(Matrix)

file.snp = "/n/stat115/hws/5/population/1000genomes.SNP.parse.result"
file.pop = "/n/stat115/hws/5/population/Popinfo.1000.Genomes.txt"
file.lung.snp = "/n/stat115/hws/5/population/lungcancer.SNP.parse.result"
file.lung.pop = "/n/stat115/hws/5/population/Popinfo.lung.cancer.txt"
file.lung.pheno = "/n/stat115/hws/5/population/lungcancer.pheno"

#Read Chr8 SNP info
x = read.table(file.snp, colClasses=c("integer","integer"), fill=TRUE, row.names=NULL)

# Convert to a sparse matrix of people (rows) x variant (columns)
chr8 = sparseMatrix(i=x[,2], j=x[,1], x=1.0)

# Inspect the dimensions of this matrix - people (rows) x variant (columns)
print(dim(chr8))

# install.packages("irlba")
library(irlba)
cm = colMeans(chr8)
p = irlba(chr8, nv=3, nu=3, tol=0.1, du=rep(1,nrow(chr8)), ds=1, dv=cm)

# Read race information for 1000 Genomes
popinfo = read.table(file.pop, sep="\t",header=TRUE,colClasses=c("character","factor"))

# Plot with colors corresponding to super populations
N = length(levels(popinfo$Population))


#Plot all individuals by first two principal components (color each individual according to their race/ancestry)
png(filename="pc2race.png")
plot(p$u[,1],p$u[,2],col=rainbow(N)[popinfo$Population],xlab="Component 1", ylab="Component 2")
legend("topright",levels(popinfo$Population),col=rainbow(N),pch = 1)
dev.off()

# Question 2
# Read lung cancer samples
y = read.table(file.lung.snp, colClasses=c("integer","integer"), fill=TRUE, row.names=NULL)

# Convert to a sparse matrix of people (rows) x variant (columns)
chr8_ = sparseMatrix(i=y[,2], j=y[,1], x=1.0)

# Inspect the dimensions of this matrix - people (rows) x variant (columns)
# In order to make you can finish the HW in time. We provide the GWAS file have the same dimensions as 1000 Genomes. Please be aware it is not normally happen in the real project.
print(dim(chr8_))

# Read race information for sample in 1000 Genomes
popinfo_ = read.table(file.lung.pop,sep="\t",header=TRUE,colClasses=c("character","factor"))

# Plot with colors corresponding to super populations
N = length(levels(popinfo_$Population))

#Use the eigenvector from PCA in question 1 as project directions lung-cancer files
################You code here###########################
pheno = read.table(file.lung.pheno,sep="\t",header=FALSE,colClasses=c("character","character","factor"))

alpha1 = chr8_%*%p$v[,1]
alpha2 = chr8_%*%p$v[,2]

#Plot all individuals by first two principal components (color each individual according to their race/ancestry)
png(filename="pc2lungrace.png")
plot(alpha1,alpha2,col=rainbow(N)[popinfo_$Population],xlab="Component 1", ylab="Component 2")
legend("topright",levels(popinfo$Population),col=rainbow(N),pch = 1)
dev.off()

#Plot all individuals by first two principal components (color each individual according to their phenotype)
png(filename="pc2lungpheno.png")
plot(alpha1,alpha2,col=rainbow(N)[pheno[,3]],xlab="Component 1", ylab="Component 2")
legend("topright",c("control", "case"),col=rainbow(N),pch = 1)
dev.off()