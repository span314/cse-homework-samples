#!/usr/bin/Rscript
#Shawn Pan
#STAT 139

data <- read.csv("pres_poll_data_hw5.csv")

#part a
data_la <- data[data$poll == "LA Times/USC",]
gap_la <- data_la$clinton - data_la$trump

data_nbc <- data[data$poll == "NBC News/Wall St. Jrnl",]
gap_nbc <- data_nbc$clinton - data_nbc$trump

#perform unpooled t-test
results <- t.test(gap_la, gap_nbc)
results

#95% intervals
df <- unname(results$parameter)
diff <- mean(gap_la) - mean(gap_nbc)
se <- sqrt(var(gap_la) / length(gap_la) + var(gap_nbc) / length(gap_nbc))

"95% Uncorrected"
tstar <- qt(0.025, df)
tstar
diff + tstar * se
diff - tstar * se

"95% Bonferroni"
tstar <- qt(0.025 / 120, df)
tstar
diff + tstar * se
diff - tstar * se

#poll groups
"Unique Groups"
unique(data$poll)
"Total Polls"
length(data$poll)
"Total Not Other"
sum(data$poll != "Other")

"95% Tukey"
tstar <- qtukey(0.95, 16, 113 - 16) / sqrt(2)
tstar
diff + tstar * se
diff - tstar * se

"Variances"
gap <- data$clinton - data$trump
by(gap, data$poll, var)