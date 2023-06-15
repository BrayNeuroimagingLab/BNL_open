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
data <- read_excel("/Users/shefalirai/Desktop/MSCData.xlsx", sheet='Task_FullSignalProperties')
data[,11] <- c(1:998)
colnames(data) <- c("GlassMS","GlassSD","MotorMS","MotorSD", "MemoryMS", "MemorySD", "Network" ,"MotorFullReli","MemoryFullReli","GlassFullReli","HexValue")

# Color order
netcolors <- data.frame(c(unique(data$Network)), unique(data$Network))
colnames(netcolors) <- c('Net Names', 'Net Hex')
netcolors$`Net Hex`<- c('#EA3327','#0505A6','#DEDB54','#B69C61','#62C04B','#C49EDD','#3B8787','#3A284C','#565DA4','#8ED2AD','#CE7377','#6A4EB8','#489F65','#4192AC','#9A99E0','#83BB72','#456044')

# Add hex color to data from netcolors 
for (name in data$Network){
  data$HexValue[which(data$Network==name)] <- netcolors$`Net Hex`[which(netcolors==name)]
}

# Mean signal vs. reliability scatter plot
tiff("SuppFigure_GlassSig.tiff", units="in", width=5, height=5, res=1000)
gms <- ggplot( data=data, aes(x = GlassMS, 
                             y=GlassFullReli)) +
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

gms <- gms + scale_fill_manual(values=c(unique(data$HexValue))) + stat_poly_eq(formula = y ~ x,
                                                                             aes(label = paste(..eq.label.., ..rr.label.., ..p.value.label.., sep = "~~~")),
                                                                             parse=TRUE,label.x.npc = 1, label.y.npc = -1, size = 3.8)
plot(gms)
dev.off()

# Mean signal vs. reliability scatter plot
tiff("SuppFigure_MotorSig.tiff", units="in", width=5, height=5, res=1000)
mms <- ggplot( data=data, aes(x = MotorMS, 
                              y=MotorFullReli)) +
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

mms <- mms + scale_fill_manual(values=c(unique(data$HexValue))) + stat_poly_eq(formula = y ~ x,
                                                                               aes(label = paste(..eq.label.., ..rr.label.., ..p.value.label.., sep = "~~~")),
                                                                               parse=TRUE,label.x.npc = 1, label.y.npc = -1, size = 3.8)
plot(mms)
dev.off()

# Mean signal vs. reliability scatter plot
tiff("SuppFigure_MemSig.tiff", units="in", width=5, height=5, res=1000)
ms <- ggplot( data=data, aes(x = MemoryMS, 
                              y=MemoryFullReli)) +
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


##################################################################################################################
# SD vs. reliability scatter plot
tiff("SuppFigure_MotorSD.tiff", units="in", width=5, height=5, res=1000)
sd <- ggplot( data=data, aes(x = MotorSD, 
                             y=MotorFullReli)) +
  theme(panel.background = element_rect(fill='white'),
        panel.border = element_blank(),
        axis.line = element_line(colour = "black"),
        axis.ticks = element_line(color = "black"),
        axis.text.x = element_text(color = "black"),
        axis.text.y = element_text(color = "black"))+
  geom_point(aes(fill = factor(Network, levels = unique(Network))), size=3, shape=21, stroke=NA) +
  geom_smooth(method="lm", formula = y ~ x, color = "black", size=0.5) +
  labs(x="tSD", y="FC-TRC") + 
  theme(legend.position = "none") 

sd <- sd + scale_fill_manual(values=c(unique(data$HexValue))) + stat_poly_eq(formula = y ~ x,
                                                                             aes(label = paste(..eq.label.., ..rr.label.., ..p.value.label.., sep = "~~~")),
                                                                             parse=TRUE,label.x.npc = 1, label.y.npc = -1, size = 3.8)
plot(sd)
dev.off()

# SD vs. reliability scatter plot
tiff("SuppFigure_GlassSD.tiff", units="in", width=5, height=5, res=1000)
gsd <- ggplot( data=data, aes(x = GlassSD, 
                             y=GlassFullReli)) +
  theme(panel.background = element_rect(fill='white'),
        panel.border = element_blank(),
        axis.line = element_line(colour = "black"),
        axis.ticks = element_line(color = "black"),
        axis.text.x = element_text(color = "black"),
        axis.text.y = element_text(color = "black"))+
  geom_point(aes(fill = factor(Network, levels = unique(Network))), size=3, shape=21, stroke=NA) +
  geom_smooth(method="lm", formula = y ~ x, color = "black", size=0.5) +
  labs(x="tSD", y="FC-TRC") + 
  theme(legend.position = "none") 

gsd <- gsd + scale_fill_manual(values=c(unique(data$HexValue))) + stat_poly_eq(formula = y ~ x,
                                                                             aes(label = paste(..eq.label.., ..rr.label.., ..p.value.label.., sep = "~~~")),
                                                                             parse=TRUE,label.x.npc = 1, label.y.npc = -1, size = 3.8)
plot(gsd)
dev.off()

# SD vs. reliability scatter plot
tiff("SuppFigure_MemSD.tiff", units="in", width=5, height=5, res=1000)
msd <- ggplot( data=data, aes(x = MemorySD, 
                              y=MemoryFullReli)) +
  theme(panel.background = element_rect(fill='white'),
        panel.border = element_blank(),
        axis.line = element_line(colour = "black"),
        axis.ticks = element_line(color = "black"),
        axis.text.x = element_text(color = "black"),
        axis.text.y = element_text(color = "black"))+
  geom_point(aes(fill = factor(Network, levels = unique(Network))), size=3, shape=21, stroke=NA) +
  geom_smooth(method="lm", formula = y ~ x, color = "black", size=0.5) +
  labs(x="tSD", y="FC-TRC") + 
  theme(legend.position = "none") 

msd <- msd + scale_fill_manual(values=c(unique(data$HexValue))) + stat_poly_eq(formula = y ~ x,
                                                                               aes(label = paste(..eq.label.., ..rr.label.., ..p.value.label.., sep = "~~~")),
                                                                               parse=TRUE,label.x.npc = 1, label.y.npc = -1, size = 3.8)
plot(msd)
dev.off()


