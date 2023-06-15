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
library("RColorBrewer")  

rm(list=ls())

# Load Relative data for REGRESSED tasks
#All variables are relative (task-rest), except column 1 which is full rest reliability
reldata <- read_excel("/Users/shefalirai/Desktop/MSCData.xlsx", sheet='RelativeSD_Regressed')
reldata[,10] <- c(1:998)
colnames(reldata) <- c("Rest Reliability", "Motor Reliability", "Motor SD", "Language Reliability", "Language SD", "Memory Reliability", "Memory SD", "Network", "Network Name", "HexValue")

# Color order
netcolors <- data.frame(c(unique(reldata$Network)), unique(reldata$Network))
colnames(netcolors) <- c('Net Names', 'Net Hex')
netcolors$`Net Hex`<- c('#EA3327','#0505A6','#DEDB54','#B69C61','#62C04B','#C49EDD','#3B8787','#3A284C','#565DA4','#8ED2AD','#CE7377','#6A4EB8','#489F65','#4192AC','#9A99E0','#83BB72','#456044')

# Add hex color to data from netcolors 
for (name in reldata$Network){
  reldata$HexValue[which(reldata$Network==name)] <- netcolors$`Net Hex`[which(netcolors==name)]
}


# MOTOR Relative SD vs. reliability scatter plot
tiff("SuppFigure6D.tiff", units="in", width=5, height=5, res=1000)
sd <- ggplot( data=reldata, aes(x = `Motor SD`, 
                                y=`Motor Reliability`)) +
  theme(panel.background = element_rect(fill='white'),
        panel.border = element_blank(),
        axis.line = element_line(colour = "black"),
        axis.ticks = element_line(color = "black"),
        axis.text.x = element_text(color = "black"),
        axis.text.y = element_text(color = "black"))+
  geom_point(aes(fill = factor(Network, levels = unique(Network))), size=3, shape=21, stroke=NA) +
#  ggtitle("Relative Motor Reliability vs. Relative SD" , subtitle = "Task Regressed") +
#  geom_smooth(method="lm", formula = y ~ x, color = "black", size=0.5) +
  labs(x=expression(~Delta * " tSD"), y=expression(~Delta * " FC-TRC")) + 
  theme(legend.position = "none")+
  geom_hline(yintercept = 0, color="red", linetype="dashed") +  # Add horizontal line at 0 
  geom_vline(xintercept =0, color="red", linetype="dashed")

sd <- sd + scale_fill_manual(values=c(unique(reldata$HexValue))) #+ stat_poly_eq(formula = y ~ x,
                                                                                #aes(label = paste(..eq.label.., ..rr.label..,signif(..p.value.., digits = 4), sep = "~~~")), 
                                                                                #parse=TRUE,label.x.npc = "right", label.y.npc = "bottom", size = 3.5)

plot(sd)
dev.off()


#Language Relative SD vs. reliability scatter plot
tiff("SuppFigure6E.tiff", units="in", width=5, height=5, res=1000)
sd2 <- ggplot( data=reldata, aes(x = `Language SD`, 
                                 y=`Language Reliability`)) +
  theme(panel.background = element_rect(fill='white'),
        panel.border = element_blank(),
        axis.line = element_line(colour = "black"),
        axis.ticks = element_line(color = "black"),
        axis.text.x = element_text(color = "black"),
        axis.text.y = element_text(color = "black"))+
  geom_point(aes(fill = factor(Network, levels = unique(Network))), size=3, shape=21, stroke=NA) +
#  ggtitle("Relative Language Reliability vs. Relative SD" , subtitle = "Task Regressed") +
#  geom_smooth(method="lm", formula = y ~ x, color = "black", size=0.5) +
  labs(x=expression(~Delta * " tSD"), y=expression(~Delta * " FC-TRC")) + 
  theme(legend.position = "none")+
  geom_hline(yintercept = 0, color="red", linetype="dashed") +  # Add horizontal line at 0 
  geom_vline(xintercept =0, color="red", linetype="dashed")

sd2 <- sd2 + scale_fill_manual(values=c(unique(reldata$HexValue))) #+ stat_poly_eq(formula = y ~ x,
                                                                                  #aes(label = paste(..eq.label.., ..rr.label..,signif(..p.value.., digits = 4), sep = "~~~")), 
                                                                                  #parse=TRUE,label.x.npc = "right", label.y.npc = "bottom", size = 3.5)

plot(sd2)
dev.off()

#Memory Relative SD vs. reliability scatter plot
tiff("SuppFigure6F.tiff", units="in", width=5, height=5, res=1000)
sd3 <- ggplot( data=reldata, aes(x = `Memory SD`, 
                                 y=`Memory Reliability`)) +
  theme(panel.background = element_rect(fill='white'),
        panel.border = element_blank(),
        axis.line = element_line(colour = "black"),
        axis.ticks = element_line(color = "black"),
        axis.text.x = element_text(color = "black"),
        axis.text.y = element_text(color = "black"))+
  geom_point(aes(fill = factor(Network, levels = unique(Network))), size=3, shape=21, stroke=NA) +
#  ggtitle("Relative Memory Reliability vs. Relative SD" , subtitle = "Task Regressed") +
#  geom_smooth(method="lm", formula = y ~ x, color = "black", size=0.5) +
  labs(x=expression(~Delta * " tSD"), y=expression(~Delta * " FC-TRC")) + 
  theme(legend.position = "none")+
  geom_hline(yintercept = 0, color="red", linetype="dashed") +  # Add horizontal line at 0 
  geom_vline(xintercept =0, color="red", linetype="dashed")

sd3 <- sd3 + scale_fill_manual(values=c(unique(reldata$HexValue))) #+ stat_poly_eq(formula = y ~ x,
                                                                                 # aes(label = paste(..eq.label.., ..rr.label..,signif(..p.value.., digits = 4), sep = "~~~")), 
                                                                                #  parse=TRUE,label.x.npc = "right", label.y.npc = "bottom", size = 3.5)

plot(sd3)
dev.off()



