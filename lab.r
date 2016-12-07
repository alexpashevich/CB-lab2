

EM <- function(p0, m00, m10, sigma){
  data <- read.table("data2.txt")
  
  p_old = p0
  m0_old = m00
  m1_old = m10
  sigma0_old = sigma
  sigma1_old = sigma
  p = 0
  m0 = 0
  m1 = 0
  sigma0 = 0
  sigma1 = 0
  
  for (t in 1:300){
  
    proba <- (exp(-((data[, 2] - m1_old)^2)/(2*sigma1_old)) * p_old) / (exp(-((data[, 2] - m0_old)^2)/(2*sigma0_old))*(1 - p_old)
                                                                + exp(-((data[, 2] - m1_old)^2)/(2 * sigma1_old)) * p_old)
    data[, 3] <- proba
  
    n0 <- 0
    n1 <- 0
    
    for (i in 1:200){
      n1 = n1 + data[i, 3]
    }
  
    n0 = 200 - n1
    
    m1 = sum(data[, 2] * data[, 3]) / n1
    m0 = sum(data[, 2] * (1 - data[, 3])) / n0
  
    sigma0 = sum((1 - data[, 3]) * (data[, 2] - m0_old)^2) / n0
    sigma1 = sum(data[, 3] * (data[, 2] - m1_old)^2) / n1
  
    p = sum(1 - data[, 3]) / 200
    
    sigma0_old = sigma0
    sigma1_old = sigma1
    m0_old = m0
    m1_old = m1
    p_old = p
      
  }
  
  a <- c(p, m0, m1, sigma0, sigma1)
  data[, 3] <- NULL
  
  return (a)
}

q <- EM(0.6, -1, 0.5, 1)
q

q <- c(0.35, -0.7, 2.2, 0.8, 1.7)

data <- read.table("data2.txt")

proba = (exp(-((data[, 2] - q[3])^2)/(2 * q[5])) * (q[1])) / (exp(-((data[, 2] - q[1])^2)/(2 * q[4])) * (q[1])  + exp(-((data[, 2] - q[3])^2)/(2 * q[5])) * (1 - q[1]))
data[, 3] <- proba
data[, 4] <- 1 - proba

head(data)

#barplot
data[, 1] <- data[, 3]
data[, 2] <- data[, 4]
head(data)
data[, 3] <- NULL
data[, 4] <- NULL
head(data)
data[, 3] <- NULL
ncol(data)
data <- as.matrix(data)
barplot(data, ylim = c(0, 150))

#MClust
library(mclust)
b <- Mclust(data[,2], G = c(1:9))
plot(b, what = "BIC")


#Challenge2---------------------------------------------------------------------------------
dat <- read.table("matrix.txt")
dim(dat)
svd.mod <- svd(scale(dat))
plot(1:15, svd.mod$d[1:15], type = 'l')

dim(diag(1./svd.mod$d))

U <- as.matrix(dat) %*%  as.matrix(svd.mod$v)  %*% as.matrix(diag(1./svd.mod$d))

U.reduced <- as.matrix(dat) %*% as.matrix(svd.mod$v[,1:7,drop=FALSE]) %*% as.matrix(diag((svd.mod$d)[1:7,drop=FALSE]))
dim(U.reduced)

Q.red <- as.matrix(svd.mod$u[,1:7, drop = FALSE]) %*% as.matrix(diag(svd.mod$d)[1:7, 1:7, drop = FALSE])

dim(Q.red)

library(mclust)
b <- densityMclust(Q.red, G = c(4:15))
plot(b, what = "BIC")

#Nclust = 9, VVE
fit <- Mclust(Q.red, G=9, modelNames = "VVE")
write(as.vector(fit$classification), ncolumns = 483, file = "out.txt")





