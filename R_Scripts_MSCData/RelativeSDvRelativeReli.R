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

# Load Relative data
#All variables are relative (task-rest), except column 1 which is full rest reliability
reldata <- read_excel("/Users/shefalirai/Desktop/MSCData.xlsx", sheet='RelativeSD_NoRregression')
reldata[,10] <- c(1:998)
colnames(reldata) <- c("Rest Reliability", "Motor Reliability", "Motor tSD", "Language Reliability", "Language tSD", "Memory Reliability", "Memory tSD", "Network", "Network Name", "HexValue")

# Color order
netcolors <- data.frame(c(unique(reldata$Network)), unique(reldata$Network))
colnames(netcolors) <- c('Net Names', 'Net Hex')
netcolors$`Net Hex`<- c('#EA3327','#0505A6','#DEDB54','#B69C61','#62C04B','#C49EDD','#3B8787','#3A284C','#565DA4','#8ED2AD','#CE7377','#6A4EB8','#489F65','#4192AC','#9A99E0','#83BB72','#456044')

# Add hex color to data from netcolors 
for (name in reldata$Network){
  reldata$HexValue[which(reldata$Network==name)] <- netcolors$`Net Hex`[which(netcolors==name)]
}


# MOTOR Relative tSD vs. reliability scatter plot
tiff("Figure5A.tiff", units="in", width=5, height=5, res=1000)
tSD <- ggplot( data=reldata, aes(x = `Motor tSD`, 
                                y=`Motor Reliability`)) +
  geom_rect(data=NULL,aes(xmin=-Inf,xmax=Inf,ymin=-Inf,ymax=0),
            fill="#ededed")+
  geom_rect(data=NULL,aes(xmin=-Inf,xmax=0,ymin=-Inf,ymax=Inf),
            fill="#ededed")+
  theme(panel.background = element_rect(fill='white'),
        panel.border = element_blank(),
        axis.line = element_line(colour = "black"),
        axis.ticks = element_line(color = "black"),
        axis.text.x = element_text(color = "black"),
        axis.text.y = element_text(color = "black"))+
  geom_point(aes(fill = factor(Network, levels = unique(Network))), size=3, shape=21,stroke=NA) +
#  ggtitle("Relative Motor Reliability vs. Relative tSD" , subtitle = "No Task Regression") +
#  geom_smooth(method="lm", formula = y ~ x, color = "black", size=0.5) +
  labs(x=expression(~Delta * " tSD"), y=expression(~Delta * " FC-TRC")) + 
  theme(legend.position = "none")+
  geom_hline(yintercept = 0, color="red", linetype="dashed") +  # Add horizontal line at 0 
  geom_vline(xintercept =0, color="red", linetype="dashed")

tSD <- tSD + scale_fill_manual(values=c(unique(reldata$HexValue))) 


#+ stat_poly_eq(formula = y ~ x,aes(label = paste(..eq.label.., ..rr.label..,signif(..p.value.., digits = 4), sep = "~~~")), 
#parse=TRUE,label.x.npc = "right", label.y.npc = "bottom", size = 3.5)

plot(tSD)
dev.off()

# # Motor tSD vs. reliability scatter plot with tSD>0
# reldata2 <- filter(reldata, `Motor tSD`>0)
# 
# motortSD2 <- ggplot( data=reldata2, aes(x = `Motor tSD`,
#                                y=`Motor Reliability`)) +
#   theme(panel.background = element_rect(fill='white'),
#         panel.border = element_blank(),
#         axis.line = element_line(colour = "black"))+
#   geom_point(aes(fill = factor(Network, levels = unique(Network))), size=2, shape=21) +
#   geom_smooth(method="lm", formula = y ~ x, color = "black", size=0.5) +
#   labs(x=expression(~Delta * " Standard Deviation"), y=expression(~Delta * " FC-TRC")) + 
#   theme(legend.position = "none")
# 
# motortSD2 <- motortSD2  + 
#   scale_fill_manual(values=c(unique(reldata2$HexValue))) +
#   stat_poly_eq(formula = y ~ x, aes(label = paste(..eq.label.., ..rr.label..,signif(..p.value.., digits = 1), sep = "~~~")),
#                                                                                 label.x.npc = "right", label.y.npc = "bottom", size = 3.5)
# 
# plot(motortSD2)




#Language Relative tSD vs. reliability scatter plot (RelativeRelivsRelativetSD_Language_NoRegression)
tiff("Figure5B.tiff", units="in", width=5, height=5, res=1000)
tSD2 <- ggplot( data=reldata, aes(x = `Language tSD`, 
                                y=`Language Reliability`)) +
  geom_rect(data=NULL,aes(xmin=-Inf,xmax=Inf,ymin=-Inf,ymax=0),
            fill="#ededed")+
  geom_rect(data=NULL,aes(xmin=-Inf,xmax=0,ymin=-Inf,ymax=Inf),
            fill="#ededed")+
  theme(panel.background = element_rect(fill='white'),
        panel.border = element_blank(),
        axis.line = element_line(colour = "black"),
        axis.ticks = element_line(color = "black"),
        axis.text.x = element_text(color = "black"),
        axis.text.y = element_text(color = "black"))+
  geom_point(aes(fill = factor(Network, levels = unique(Network))), size=3, shape=21,stroke=NA) +
#  ggtitle("Relative Language Reliability vs. Relative tSD" , subtitle = "No Task Regression") +
#  geom_smooth(method="lm", formula = y ~ x, color = "black", size=0.5) +
  labs(x=expression(~Delta * " tSD"), y=expression(~Delta * " FC-TRC")) + 
  theme(legend.position = "none")+
  geom_hline(yintercept = 0, color="red", linetype="dashed") +  # Add horizontal line at 0 
  geom_vline(xintercept =0, color="red", linetype="dashed")

tSD2 <- tSD2 + scale_fill_manual(values=c(unique(reldata$HexValue))) #+ stat_poly_eq(formula = y ~ x,
                                                                                #aes(label = paste(..eq.label.., ..rr.label..,signif(..p.value.., digits = 4), sep = "~~~")), 
                                                                                #parse=TRUE,label.x.npc = "right", label.y.npc = "bottom", size = 3.5)

plot(tSD2)
dev.off()


# 
# # Language tSD vs. reliability scatter plot with tSD>0
# reldata2 <- filter(reldata, `Language tSD`>0)
# 
# langtSD2 <- ggplot( data=reldata2, aes(x = `Language tSD`,
#                                   y=`Language Reliability`)) +
#   theme(panel.background = element_rect(fill='white'),
#         panel.border = element_blank(),
#         axis.line = element_line(colour = "black"))+
#   geom_point(aes(fill = factor(Network, levels = unique(Network))), size=2, shape=21) +
#   geom_smooth(method="lm", formula = y ~ x, color = "black", size=0.5) +
#   labs(x=expression(~Delta * " Standard Deviation"), y=expression(~Delta * " FC-TRC")) + 
#   theme(legend.position = "none")
# 
# langtSD2 <- langtSD2  + 
#   scale_fill_manual(values=c(unique(reldata2$HexValue))) +
#   stat_poly_eq(formula = y ~ x, aes(label = paste(..eq.label.., ..rr.label..,signif(..p.value.., digits = 1), sep = "~~~")),
#                label.x.npc = "right", label.y.npc = "bottom", size = 3.5)
# 
# plot(langtSD2)



#Memory Relative tSD vs. reliability scatter plot
tiff("Figure5C.tiff", units="in", width=5, height=5, res=1000)
tSD3 <- ggplot( data=reldata, aes(x = `Memory tSD`, 
                                y=`Memory Reliability`)) +
  geom_rect(data=NULL,aes(xmin=-Inf,xmax=Inf,ymin=-Inf,ymax=0),
            fill="#ededed")+
  geom_rect(data=NULL,aes(xmin=-Inf,xmax=0,ymin=-Inf,ymax=Inf),
            fill="#ededed")+
  theme(panel.background = element_rect(fill='white'),
        panel.border = element_blank(),
        axis.line = element_line(colour = "black"),
        axis.ticks = element_line(color = "black"),
        axis.text.x = element_text(color = "black"),
        axis.text.y = element_text(color = "black"))+
  geom_point(aes(fill = factor(Network, levels = unique(Network))), size=3, shape=21, stroke=NA) +
#  ggtitle("Relative Memory Reliability vs. Relative tSD" , subtitle = "No Task Regression") +
#  geom_smooth(method="lm", formula = y ~ x, color = "black", size=0.5) +
  labs(x=expression(~Delta * " tSD"), y=expression(~Delta * " FC-TRC")) + 
#  scale_x_continuous(limits = c(-1.2, 0.8)) +
  theme(legend.position = "none")+
  geom_hline(yintercept = 0, color="red", linetype="dashed") +  # Add horizontal line at 0 
  geom_vline(xintercept =0, color="red", linetype="dashed")

tSD3 <- tSD3 + scale_fill_manual(values=c(unique(reldata$HexValue))) #+ stat_poly_eq(formula = y ~ x,
                                                                                #aes(label = paste(..eq.label.., ..rr.label..,signif(..p.value.., digits = 4), sep = "~~~")), 
                                                                                #parse=TRUE,label.x.npc = "right", label.y.npc = "bottom", size = 3.5)

plot(tSD3)
dev.off()
# # Memory tSD vs. reliability scatter plot with tSD>0
# reldata2 <- filter(reldata, `Memory tSD`>0)
# memtSD2 <- ggplot( data=reldata2, aes(x = `Memory tSD`,
#                                       y=`Memory Reliability`)) +
#   theme(panel.background = element_rect(fill='white'),
#         panel.border = element_blank(),
#         axis.line = element_line(colour = "black"))+
#   geom_point(aes(fill = factor(Network, levels = unique(Network))), size=2, shape=21) +
#   geom_smooth(method="lm", formula = y ~ x, color = "black", size=0.5) +
#   labs(x=expression(~Delta * " Standard Deviation"), y=expression(~Delta * " FC-TRC")) + 
#   theme(legend.position = "none")
# 
# memtSD2 <- memtSD2  + 
#   scale_fill_manual(values=c(unique(reldata2$HexValue))) +
#   stat_poly_eq(formula = y ~ x, aes(label = paste(..eq.label.., ..rr.label..,signif(..p.value.., digits = 1), sep = "~~~")),
#                label.x.npc = "right", label.y.npc = "bottom", size = 3.5)
# 
# plot(memtSD2)



