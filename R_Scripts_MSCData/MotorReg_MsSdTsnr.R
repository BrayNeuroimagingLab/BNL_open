# Libraries
options(knitr.table.format = "html")
library(tidyverse)
library(hrbrthemes)
library(kableExtra)
library(readxl)
library(ggplot2)
library(dplyr)
library(ggprism)
library(patchwork)
library(ggpmisc)
library(cowplot)
library(ggpubr)
library(gplots)
library(grid)
library(gridExtra) 

#Run this code is plot window is not displaying plots, otherwise skip
rm(list=ls())
while (!is.null(dev.list()))  dev.off()
plot(rnorm(50), rnorm(50))


# Load dataset
data <- read_excel("/Users/shefalirai/Desktop/Signal_Reg.xlsx", sheet='Motor Signal vs Reli Reg')
data <- data[,1:5]
data[,6] <- c(1:1000)
colnames(data) <- c("Reliability","MeanSignal", "SD","TSNR","Network","HexValue")

# Color order
netcolors <- data.frame(c(unique(data$Network)), unique(data$Network))
colnames(netcolors) <- c('Net Names', 'Net Hex')
netcolors$`Net Hex`<- c('#EA3327','#0505A6','#FAF651','#B69C61','#62C04B','#C49EDD','#3B8787','#3A284C','#565DA4','#8ED2AD','#CE7377','#6A4EB8','#489F65','#4192AC','#9A99E0','#83BB72','#456044')

# Add hex color to data from netcolors 
for (name in data$Network){
  data$HexValue[which(data$Network==name)] <- netcolors$`Net Hex`[which(netcolors==name)]
}

# SD vs. reliability scatter plot
sd <- ggplot( data=data, aes(x = SD, 
                             y=Reliability)) +
  theme(panel.background = element_rect(fill='white'),
        panel.border = element_blank(),
        axis.line = element_line(colour = "black"))+
  geom_point(aes(fill = factor(Network, levels = unique(Network))), size=2, shape=21) +
  geom_smooth(method="lm", formula = y ~ x, color = "black", size=0.5) +
  labs(x="Standard Deviation", y="Test-Retest Correlation") + 
  theme(legend.position = "none")

sd <- sd + scale_fill_manual(values=c(unique(data$HexValue))) + stat_poly_eq(formula = y ~ x,
                                                                             aes(label = paste(..eq.label.., ..rr.label..,signif(..p.value.., digits = 4), sep = "~~~")), 
                                                                             parse=TRUE,label.x.npc = "right", label.y.npc = "bottom", size = 3.5)

plot(sd)


# Load dataset
data <- read_excel("/Users/shefalirai/Desktop/Signal_Reg.xlsx", sheet='Glass Signal vs Reli Reg')
data <- data[,1:5]
data[,6] <- c(1:1000)
colnames(data) <- c("Reliability","MeanSignal", "SD","TSNR","Network","HexValue")

# Color order
netcolors <- data.frame(c(unique(data$Network)), unique(data$Network))
colnames(netcolors) <- c('Net Names', 'Net Hex')
netcolors$`Net Hex`<- c('#EA3327','#0505A6','#FAF651','#B69C61','#62C04B','#C49EDD','#3B8787','#3A284C','#565DA4','#8ED2AD','#CE7377','#6A4EB8','#489F65','#4192AC','#9A99E0','#83BB72','#456044')

# Add hex color to data from netcolors 
for (name in data$Network){
  data$HexValue[which(data$Network==name)] <- netcolors$`Net Hex`[which(netcolors==name)]
}

# SD vs. reliability scatter plot
sd2 <- ggplot( data=data, aes(x = SD, 
                             y=Reliability)) +
  theme(panel.background = element_rect(fill='white'),
        panel.border = element_blank(),
        axis.line = element_line(colour = "black"))+
  geom_point(aes(fill = factor(Network, levels = unique(Network))), size=2, shape=21) +
  geom_smooth(method="lm", formula = y ~ x, color = "black", size=0.5) +
  labs(x="Standard Deviation", y="Test-Retest Correlation") + 
  theme(legend.position = "none")

sd2 <- sd2 + scale_fill_manual(values=c(unique(data$HexValue))) + stat_poly_eq(formula = y ~ x,
                                                                             aes(label = paste(..eq.label.., ..rr.label..,signif(..p.value.., digits = 4), sep = "~~~")), 
                                                                             parse=TRUE,label.x.npc = "right", label.y.npc = "bottom", size = 3.5)

plot(sd2)


# Load dataset
data <- read_excel("/Users/shefalirai/Desktop/Signal_Reg.xlsx", sheet='Memory Signal vs Reli Reg')
data <- data[,1:5]
data[,6] <- c(1:1000)
colnames(data) <- c("Reliability","MeanSignal", "SD","TSNR","Network","HexValue")

# Color order
netcolors <- data.frame(c(unique(data$Network)), unique(data$Network))
colnames(netcolors) <- c('Net Names', 'Net Hex')
netcolors$`Net Hex`<- c('#EA3327','#0505A6','#FAF651','#B69C61','#62C04B','#C49EDD','#3B8787','#3A284C','#565DA4','#8ED2AD','#CE7377','#6A4EB8','#489F65','#4192AC','#9A99E0','#83BB72','#456044')

# Add hex color to data from netcolors 
for (name in data$Network){
  data$HexValue[which(data$Network==name)] <- netcolors$`Net Hex`[which(netcolors==name)]
}

# SD vs. reliability scatter plot
sd3 <- ggplot( data=data, aes(x = SD, 
                             y=Reliability)) +
  theme(panel.background = element_rect(fill='white'),
        panel.border = element_blank(),
        axis.line = element_line(colour = "black"))+
  geom_point(aes(fill = factor(Network, levels = unique(Network))), size=2, shape=21) +
  geom_smooth(method="lm", formula = y ~ x, color = "black", size=0.5) +
  labs(x="Standard Deviation", y="Test-Retest Correlation") + 
  theme(legend.position = "none")

sd3 <- sd3 + scale_fill_manual(values=c(unique(data$HexValue))) + stat_poly_eq(formula = y ~ x,
                                                                             aes(label = paste(..eq.label.., ..rr.label..,signif(..p.value.., digits = 4), sep = "~~~")), 
                                                                             parse=TRUE,label.x.npc = "right", label.y.npc = "bottom", size = 3.5)

plot(sd3)


# Load dataset
data <- read_excel("/Users/shefalirai/Desktop/Signal_Reg.xlsx", sheet='Motor Signal vs Reli Reg')
data <- data[,1:5]
data[,6] <- c(1:1000)
colnames(data) <- c("Reliability","MeanSignal", "SD","TSNR","Network","HexValue")

# Color order
netcolors <- data.frame(c(unique(data$Network)), unique(data$Network))
colnames(netcolors) <- c('Net Names', 'Net Hex')
netcolors$`Net Hex`<- c('#EA3327','#0505A6','#FAF651','#B69C61','#62C04B','#C49EDD','#3B8787','#3A284C','#565DA4','#8ED2AD','#CE7377','#6A4EB8','#489F65','#4192AC','#9A99E0','#83BB72','#456044')

# Add hex color to data from netcolors 
for (name in data$Network){
  data$HexValue[which(data$Network==name)] <- netcolors$`Net Hex`[which(netcolors==name)]
}

# SD vs. reliability scatter plot
tsnr <- ggplot( data=data, aes(x = TSNR, 
                             y=Reliability)) +
  theme(panel.background = element_rect(fill='white'),
        panel.border = element_blank(),
        axis.line = element_line(colour = "black"))+
  geom_point(aes(fill = factor(Network, levels = unique(Network))), size=2, shape=21) +
  geom_smooth(method="lm", formula = y ~ x, color = "black", size=0.5) +
  labs(x="TSNR", y="Test-Retest Correlation") + 
  theme(legend.position = "none")

tsnr <- tsnr + scale_fill_manual(values=c(unique(data$HexValue))) + stat_poly_eq(formula = y ~ x,
                                                                             aes(label = paste(..eq.label.., ..rr.label..,signif(..p.value.., digits = 4), sep = "~~~")), 
                                                                             parse=TRUE,label.x.npc = "right", label.y.npc = "bottom", size = 3.5)

plot(tsnr)


# Load dataset
data <- read_excel("/Users/shefalirai/Desktop/Signal_Reg.xlsx", sheet='Glass Signal vs Reli Reg')
data <- data[,1:5]
data[,6] <- c(1:1000)
colnames(data) <- c("Reliability","MeanSignal", "SD","TSNR","Network","HexValue")

# Color order
netcolors <- data.frame(c(unique(data$Network)), unique(data$Network))
colnames(netcolors) <- c('Net Names', 'Net Hex')
netcolors$`Net Hex`<- c('#EA3327','#0505A6','#FAF651','#B69C61','#62C04B','#C49EDD','#3B8787','#3A284C','#565DA4','#8ED2AD','#CE7377','#6A4EB8','#489F65','#4192AC','#9A99E0','#83BB72','#456044')

# Add hex color to data from netcolors 
for (name in data$Network){
  data$HexValue[which(data$Network==name)] <- netcolors$`Net Hex`[which(netcolors==name)]
}

# SD vs. reliability scatter plot
tsnr2 <- ggplot( data=data, aes(x = TSNR, 
                              y=Reliability)) +
  theme(panel.background = element_rect(fill='white'),
        panel.border = element_blank(),
        axis.line = element_line(colour = "black"))+
  geom_point(aes(fill = factor(Network, levels = unique(Network))), size=2, shape=21) +
  geom_smooth(method="lm", formula = y ~ x, color = "black", size=0.5) +
  labs(x="TSNR", y="Test-Retest Correlation") + 
  theme(legend.position = "none")

tsnr2 <- tsnr2 + scale_fill_manual(values=c(unique(data$HexValue))) + stat_poly_eq(formula = y ~ x,
                                                                               aes(label = paste(..eq.label.., ..rr.label..,signif(..p.value.., digits = 4), sep = "~~~")), 
                                                                               parse=TRUE,label.x.npc = "right", label.y.npc = "bottom", size = 3.5)

plot(tsnr2)


# Load dataset
data <- read_excel("/Users/shefalirai/Desktop/Signal_Reg.xlsx", sheet='Memory Signal vs Reli Reg')
data <- data[,1:5]
data[,6] <- c(1:1000)
colnames(data) <- c("Reliability","MeanSignal", "SD","TSNR","Network","HexValue")

# Color order
netcolors <- data.frame(c(unique(data$Network)), unique(data$Network))
colnames(netcolors) <- c('Net Names', 'Net Hex')
netcolors$`Net Hex`<- c('#EA3327','#0505A6','#FAF651','#B69C61','#62C04B','#C49EDD','#3B8787','#3A284C','#565DA4','#8ED2AD','#CE7377','#6A4EB8','#489F65','#4192AC','#9A99E0','#83BB72','#456044')

# Add hex color to data from netcolors 
for (name in data$Network){
  data$HexValue[which(data$Network==name)] <- netcolors$`Net Hex`[which(netcolors==name)]
}

# SD vs. reliability scatter plot
tsnr3 <- ggplot( data=data, aes(x = TSNR, 
                              y=Reliability)) +
  theme(panel.background = element_rect(fill='white'),
        panel.border = element_blank(),
        axis.line = element_line(colour = "black"))+
  geom_point(aes(fill = factor(Network, levels = unique(Network))), size=2, shape=21) +
  geom_smooth(method="lm", formula = y ~ x, color = "black", size=0.5) +
  labs(x="TSNR", y="Test-Retest Correlation") + 
  theme(legend.position = "none")

tsnr3 <- tsnr3 + scale_fill_manual(values=c(unique(data$HexValue))) + stat_poly_eq(formula = y ~ x,
                                                                               aes(label = paste(..eq.label.., ..rr.label..,signif(..p.value.., digits = 4), sep = "~~~")), 
                                                                               parse=TRUE,label.x.npc = "right", label.y.npc = "bottom", size = 3.5)

plot(tsnr3)




