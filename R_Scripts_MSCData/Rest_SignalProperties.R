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

rm(list=ls())


# Load Mean Signal dataset
data <- read_excel("/Users/shefalirai/Desktop/MSCData.xlsx", sheet='Rest_SignalProperties')
data[,6] <- c(1:998)
colnames(data) <- c("Network","NetworkName","Reliability","MeanSignal", "SD", "HexValue")

# Color order
netcolors <- data.frame(c(unique(data$Network)), unique(data$Network))
colnames(netcolors) <- c('Net Names', 'Net Hex')
netcolors$`Net Hex`<- c('#EA3327','#0505A6','#DEDB54','#B69C61','#62C04B','#C49EDD','#3B8787','#3A284C','#565DA4','#8ED2AD','#CE7377','#6A4EB8','#489F65','#4192AC','#9A99E0','#83BB72','#456044')

# Add hex color to data from netcolors 
tiff("Figure3B.tiff", units="in", width=5, height=5, res=1000)
for (name in data$Network){
  data$HexValue[which(data$Network==name)] <- netcolors$`Net Hex`[which(netcolors==name)]
}

# Mean signal vs. reliability scatter plot
ms <- ggplot( data=data, aes(x = MeanSignal, 
                              y=Reliability)) +
  theme(panel.background = element_rect(fill='white'),
        panel.border = element_blank(),
        axis.line = element_line(colour = "black"),
        axis.ticks = element_line(color = "black"),
        axis.text.x = element_text(color = "black"),
        axis.text.y = element_text(color = "black"))+
  geom_point(aes(fill = factor(Network, levels = unique(Network))), size=3, shape=21, stroke=NA) +
  geom_smooth(method="lm", formula = y ~ x, color = "black", size=0.5) +
  labs(x="tMean", y="FC-TRC") + 
  theme(legend.position = "none") 

ms <- ms + scale_fill_manual(values=c(unique(data$HexValue))) + stat_poly_eq(formula = y ~ x,
                                                                           aes(label = paste(..eq.label.., ..rr.label.., ..p.value.label.., sep = "~~~")),
                                                                           parse=TRUE,label.x.npc = 1, label.y.npc = -1, size = 3.8)
plot(ms)
dev.off()
# Correlation coefficient
result = cor.test(data$MeanSignal, data$Reliability, method = "spearman")



# Mean signal vs. reliability scatter plot with low reli network removed
data2 <- filter(data, Network!=8, Network!=11, Network!=17)

tiff("Figure3C.tiff", units="in", width=5, height=5, res=1000)
ms2 <- ggplot( data=data2, aes(x = MeanSignal,
              y=Reliability)) +
  theme(panel.background = element_rect(fill='white'),
        panel.border = element_blank(),
        axis.line = element_line(colour = "black"),
        axis.ticks = element_line(color = "black"),
        axis.text.x = element_text(color = "black"),
        axis.text.y = element_text(color = "black"))+
  geom_point(aes(fill = factor(Network, levels = unique(Network))), size=3, shape=21, stroke=NA) +
  geom_smooth(method="lm", formula = y ~ x, color = "black", size=0.5) +
  labs(x="tMean", y="FC-TRC") +
  theme(legend.position = "none")

ms2 <- ms2 + scale_fill_manual(values=c(unique(data2$HexValue))) + stat_poly_eq(formula = y ~ x,
                                                                                aes(label = paste(..eq.label.., ..rr.label.., ..p.value.label.., sep = "~~~")),
                                                                                parse=TRUE,label.x.npc = 1, label.y.npc = -1, size = 3.8)

plot(ms2)
dev.off()

# Correlation coefficient
result = cor.test(data2$MeanSignal, data2$Reliability, method = "spearman")


########################################################################################################################################################################################################

# SD vs. reliability scatter plot
tiff("Figure3E.tiff", units="in", width=5, height=5, res=1000)
sd <- ggplot( data=data, aes(x = SD, 
                             y=Reliability)) +
  theme(panel.background = element_rect(fill='white'),
        panel.border = element_blank(),
        axis.line = element_line(colour = "black"),
        axis.ticks = element_line(color = "black"),
        axis.text.x = element_text(color = "black"),
        axis.text.y = element_text(color = "black"))+
  geom_point(aes(fill = factor(Network, levels = unique(Network))), size=3, shape=21, stroke=NA) +
  geom_smooth(method="lm", formula = y ~ x, color = "black", size=0.5) +
  labs(x="tSD",  y="FC-TRC") +
  theme(legend.position = "none")

sd <- sd + scale_fill_manual(values=c(unique(data$HexValue))) + stat_poly_eq(formula = y ~ x,
                                                                             aes(label = paste(..eq.label.., ..rr.label.., ..p.value.label.., sep = "~~~")),
                                                                             parse=TRUE,label.x.npc = 1, label.y.npc = -1, size = 3.8)
plot(sd)
dev.off()

# Correlation coefficient
result = cor.test(data$SD, data$Reliability, method = "spearman")




# SD vs. reliability scatter plot with low reli network removed
data2 <- filter(data, Network!=8, Network!=11, Network!=17)

tiff("Figure3F.tiff", units="in", width=5, height=5, res=1000)
sd2 <- ggplot( data=data2, aes(x = SD,
                               y=Reliability)) +
  theme(panel.background = element_rect(fill='white'),
        panel.border = element_blank(),
        axis.line = element_line(colour = "black"),
        axis.ticks = element_line(color = "black"),
        axis.text.x = element_text(color = "black"),
        axis.text.y = element_text(color = "black"))+
  geom_point(aes(fill = factor(Network, levels = unique(Network))), size=3, shape=21, stroke=NA) +
  geom_smooth(method="lm", formula = y ~ x, color = "black", size=0.5) +
  labs(x="tSD",  y="FC-TRC") +
  theme(legend.position = "none")

sd2 <- sd2 + scale_fill_manual(values=c(unique(data2$HexValue))) + stat_poly_eq(formula = y ~ x,
                                                                                aes(label = paste(..eq.label.., ..rr.label.., ..p.value.label.., sep = "~~~")),
                                                                                parse=TRUE,label.x.npc = 1, label.y.npc = -1, size = 3.8)
plot(sd2)
dev.off()

# Correlation coefficient
result = cor.test(data2$SD, data2$Reliability, method = "spearman")



########################################################################################################################################################################################################
#TSNR


#Load tsnr data
data <- read_excel("/Users/shefalirai/Desktop/MSCData.xlsx", sheet='Rest_SignalProperties')
data[,7] <- c(1:998)
colnames(data) <- c("Network","NetworkName","Reliability","MeanSignal", "SD", "TSNR", "HexValue")

# Color order
netcolors <- data.frame(c(unique(data$Network)), unique(data$Network))
colnames(netcolors) <- c('Net Names', 'Net Hex')
netcolors$`Net Hex`<- c('#EA3327','#0505A6','#DEDB54','#B69C61','#62C04B','#C49EDD','#3B8787','#3A284C','#565DA4','#8ED2AD','#CE7377','#6A4EB8','#489F65','#4192AC','#9A99E0','#83BB72','#456044')

# Add hex color to data from netcolors 
tiff("Figure3B.tiff", units="in", width=5, height=5, res=1000)
for (name in data$Network){
  data$HexValue[which(data$Network==name)] <- netcolors$`Net Hex`[which(netcolors==name)]
}


# TSNR vs. reliability scatter plot
tiff("SuppFigure4B.tiff", units="in", width=5, height=5, res=1000)
tr <- ggplot( data=data, aes(x = TSNR, 
                             y=Reliability)) +
  theme(panel.background = element_rect(fill='white'),
        panel.border = element_blank(),
        axis.line = element_line(colour = "black"),
        axis.ticks = element_line(color = "black"),
        axis.text.x = element_text(color = "black"),
        axis.text.y = element_text(color = "black"))+
  geom_point(aes(fill = factor(Network, levels = unique(Network))), size=3, shape=21, stroke=NA) +
#  geom_smooth(method="lm", formula = y ~ x, color = "black", size=0.5) +
  labs(x="tSNR",  y="FC-TRC") +
  theme(legend.position = "none")

tr <- tr + scale_fill_manual(values=c(unique(data$HexValue))) #+ stat_poly_eq(formula = y ~ x,
                                                               #              aes(label = paste(..eq.label.., ..rr.label.., ..p.value.label.., sep = "~~~")),
                                                                #             parse=TRUE,label.x.npc = 1, label.y.npc = -1, size = 3.8)
plot(tr)
dev.off()

 
#tsnr filtered
data2 <- filter(data, Network!=8, Network!=11, Network!=17)

tiff("SuppFigure4C.tiff", units="in", width=5, height=5, res=1000)
tr2 <- ggplot( data=data2, aes(x = TSNR, 
                             y=Reliability)) +
  theme(panel.background = element_rect(fill='white'),
        panel.border = element_blank(),
        axis.line = element_line(colour = "black"),
        axis.ticks = element_line(color = "black"),
        axis.text.x = element_text(color = "black"),
        axis.text.y = element_text(color = "black"))+
  geom_point(aes(fill = factor(Network, levels = unique(Network))), size=3, shape=21, stroke=NA) +
  geom_smooth(method="lm", formula = y ~ x, color = "black", size=0.5) +
  labs(x="tSNR",  y="FC-TRC") +
  theme(legend.position = "none")

tr2 <- tr2 + scale_fill_manual(values=c(unique(data$HexValue))) + stat_poly_eq(formula = y ~ x,
                                                                             aes(label = paste(..eq.label.., ..rr.label.., ..p.value.label.., sep = "~~~")),
                                                                             parse=TRUE,label.x.npc = 1, label.y.npc = -1, size = 3.8)
plot(tr2)
dev.off()






