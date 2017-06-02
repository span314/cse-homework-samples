#!/usr/bin/Rscript
#Shawn Pan
#STAT 139

data <- read.csv("pres_poll_data_hw5.csv")

#anova model
gap <- data$clinton - data$trump
model <- aov(gap~data$month)
anova(model)

#tukey
TukeyHSD(model)

#contrast test
"Contrast Test"
l <- c(32, 25, 35, 25)
a <- c(32/92, 25/92, 35/92, -1)
m <- by(gap, data$month, mean)
m <- c(unname(m["7-Jul"]), unname(m["8-Aug"]), unname(m["9-Sep"]), unname(m["10-Oct"]))
ms <- summary(model)[[1]][["Mean Sq"]][2] #14.16
t <- sum(a * m) / (sqrt(ms) * sqrt(sum(a * a / l)))
"t statistic"
t
"2-sided p-value"
2 * pt(t, 113)

#2 way
"2 way no interactions"
model <- aov(gap~data$month+data$poll)
anova(model)

#2 way with interactions
"2 way with interactions"
model <- aov(gap~data$month*data$poll)
anova(model)

#plots
png("boxplotmonth.png", width=360, height=360)
plot(gap~data$month, xlab="Month", ylab="Gap", main="Voter Gap by Month")
dev.off()

png("interactions.png", width=480, height=360)
interaction.plot(data$poll, data$month, gap, xlab="Poll", ylab="Gap", main="Interaction", xaxt="n", type="o")
dev.off()

png("boxplotpoll.png", width=480, height=360)
par(las=2)
par(mar=c(10,4,1,1))
plot(gap~data$poll, xlab="", ylab="Gap", main="Voter Gap by Pollster")
dev.off()