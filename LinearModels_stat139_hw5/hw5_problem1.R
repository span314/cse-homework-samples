#!/usr/bin/Rscript
#Shawn Pan
#STAT 139

set.seed(0)

data <- read.csv("textmessages.csv")

under_texts <- data$texts[data$underclassman == 1]
upper_texts <- data$texts[data$underclassman == 0]
all_texts <- data$texts

observed_mean <- mean(under_texts) - mean(upper_texts)

#sample permutations
nsims <- 100000
resample_mean <- numeric(nsims)
for (i in 1:nsims) {
  resample <- sample(all_texts)
  resample_mean[i] <- mean(resample[data$underclassman == 1]) - mean(resample[data$underclassman == 0])
}

#plot distribution
png("permutations.png", width=360, height=360)
hist(resample_mean, col="blue", main="Permutation Distribution", xlab="Resampled Mean")
abline(v=observed_mean, col="red")
dev.off()

"p-value"
2 * mean(resample_mean >= observed_mean)