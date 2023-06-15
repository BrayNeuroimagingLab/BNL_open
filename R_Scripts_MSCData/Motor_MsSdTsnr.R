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


# Load Mean Signal dataset
data <- read_excel("/Users/shefalirai/Desktop/RegvsNoReg.xlsx", sheet='Motor Signal vs Reli')
data <- data[,c(1,2,3,4,5)]
data[,6] <- c(1:1000)
colnames(data) <- c("Reliability","MeanSignal", "SD","TSNR","Network", "HexValue")


# Color order
netcolors <- data.frame(c(unique(data$Network)), unique(data$Network))
colnames(netcolors) <- c('Net Names', 'Net Hex')
netcolors$`Net Hex`<- c('#EA3327','#0505A6','#FAF651','#B69C61','#62C04B','#C49EDD','#3B8787','#3A284C','#565DA4','#8ED2AD','#CE7377','#6A4EB8','#489F65','#4192AC','#9A99E0','#83BB72','#456044')

# Add hex color to data from netcolors 
for (name in data$Network){
  data$HexValue[which(data$Network==name)] <- netcolors$`Net Hex`[which(netcolors==name)]
}

# Mean signal vs. reliability scatter plot
legend_title <- "Network"
ms <- ggplot( data=data, aes(x = MeanSignal, 
                             y=Reliability, size=Network)) +
  theme(panel.background = element_rect(fill='white'),
        panel.border = element_blank(),
        axis.line = element_line(colour = "black"))+
  geom_point(aes(fill = factor(Network, levels = unique(Network))), size=2, shape=21) +
  geom_smooth(method="lm", formula = y ~ x, color = "black", size=0.5) +
  scale_size(range = c(.1, 24), name="Network") + 
  labs(x="Mean Signal", y="Test-Retest Correlation") +
  theme(legend.position = "none")

ms <- ms + scale_fill_manual(legend_title, values=c(unique(data$HexValue))) + stat_poly_eq(formula = y ~ x,
                                                                           aes(label = paste(..eq.label.., ..rr.label..,signif(..p.value.., digits = 4), sep = "~~~")), 
                                                                           parse=TRUE,label.x.npc = "right", label.y.npc = "bottom", size = 3.5)

plot(ms)

legend <- get_legend(ms)                    

# Create new plot window
grid.newpage()                              

# Draw Only legend 
grid.draw(legend) 

# Mean signal vs. reliability scatter plot with r>=0.7 and low reli network removed
data2 <- filter(data, Network!=8, Network!=11, Reliability>=0.7)

ms2 <- ggplot( data=data2, aes(x = MeanSignal, 
                               y=Reliability)) +
  theme(panel.background = element_rect(fill='white'),
        panel.border = element_blank(),
        axis.line = element_line(colour = "black"))+
  geom_point(aes(fill = factor(Network, levels = unique(Network))), size=2, shape=21) +
  geom_smooth(method="lm", formula = y ~ x, color = "black", size=0.5) +
  labs(x="Mean Signal", y="Test-Retest Correlation") + 
  theme(legend.position = "none")

ms2 <- ms2 + scale_fill_manual(values=c(unique(data2$HexValue))) + stat_poly_eq(formula = y ~ x,
                                                                                aes(label = paste(..eq.label.., ..rr.label..,signif(..p.value.., digits = 4), sep = "~~~")), 
                                                                                parse=TRUE,label.x.npc = "right", label.y.npc = "bottom", size = 3.5)

plot(ms2)


# Load dataset
data <- read_excel("/Users/shefalirai/Desktop/RegvsNoReg.xlsx", sheet='Motor Signal vs Reli')
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


# sd vs. reliability scatter plot with r>=0.7 and low reli network removed
data2 <- filter(data, Network!=8, Network!=11, Reliability>=0.7)

sd2 <- ggplot( data=data2, aes(x = SD, 
                               y=Reliability)) +
  theme(panel.background = element_rect(fill='white'),
        panel.border = element_blank(),
        axis.line = element_line(colour = "black"))+
  geom_point(aes(fill = factor(Network, levels = unique(Network))), size=2, shape=21) +
  geom_smooth(method="lm", formula = y ~ x, color = "black", size=0.5) +
  labs(x="SD", y="Test-Retest Correlation") + 
  theme(legend.position = "none")

sd2 <- sd2 + scale_fill_manual(values=c(unique(data2$HexValue))) + stat_poly_eq(formula = y ~ x,
                                                                                aes(label = paste(..eq.label.., ..rr.label..,signif(..p.value.., digits = 4), sep = "~~~")), 
                                                                                parse=TRUE,label.x.npc = "right", label.y.npc = "bottom", size = 3.5)

plot(sd2)




# Load Mean Signal dataset
data <- read_excel("/Users/shefalirai/Desktop/RegvsNoReg.xlsx", sheet='Motor Signal vs Reli')
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

# TSNR vs. reliability scatter plot
tr <- ggplot( data=data, aes(x = TSNR, 
                             y=Reliability)) +
  theme(panel.background = element_rect(fill='white'),
        panel.border = element_blank(),
        axis.line = element_line(colour = "black"))+
  geom_point(aes(fill = factor(Network, levels = unique(Network))), size=2, shape=21) +
  geom_smooth(method="lm", formula = y ~ x, color = "black", size=0.5) +
  labs(x="TSNR", y="Test-Retest Correlation") + 
  theme(legend.position = "none")

tr <- tr + scale_fill_manual(values=c(unique(data$HexValue)))  + stat_poly_eq(formula = y ~ x,
                                                                              aes(label = paste(..eq.label.., ..rr.label..,signif(..p.value.., digits = 4), sep = "~~~")), 
                                                                              parse=TRUE,label.x.npc = "right", label.y.npc = "bottom", size = 3.5)

plot(tr)


#tsnr vs. reliability scatter plot with r>=0.7 and low reli network removed
data2 <- filter(data, Network!=8, Network!=11, Reliability>=0.7)

tr2 <- ggplot( data=data2, aes(x = TSNR, 
                               y=Reliability)) +
  theme(panel.background = element_rect(fill='white'),
        panel.border = element_blank(),
        axis.line = element_line(colour = "black"))+
  geom_point(aes(fill = factor(Network, levels = unique(Network))), size=2, shape=21) +
  geom_smooth(method="lm", formula = y ~ x, color = "black", size=0.5) +
  labs(x="TSNR", y="Test-Retest Correlation") + 
  theme(legend.position = "none")

tr2 <- tr2 + scale_fill_manual(values=c(unique(data2$HexValue))) + stat_poly_eq(formula = y ~ x,
                                                                                aes(label = paste(..eq.label.., ..rr.label.., signif(..p.value.., digits = 4),sep = "~~~")), 
                                                                                parse=TRUE,label.x.npc = "right", label.y.npc = "bottom", size = 3.5)

plot(tr2)






