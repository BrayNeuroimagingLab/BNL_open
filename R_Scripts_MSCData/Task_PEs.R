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
#Non-regressed relative reliability vs. PEs from 3rd level fsl feat

reldata <- read_excel("/Users/shefalirai/Desktop/MSCData.xlsx", sheet='PEBetas_3rdLevel')
reldata[,9] <- c(1:998)
colnames(reldata) <- c("Motor Relative Reliability", "Motor PE", "Glass Relative Reliability", "Glass PE", "Memory Relative Reliability", "Memory PE","Network", "Network Name", "HexValue")

# Color order
netcolors <- data.frame(c(unique(reldata$Network)), unique(reldata$Network))
colnames(netcolors) <- c('Net Names', 'Net Hex')
netcolors$`Net Hex`<- c('#EA3327','#0505A6','#DEDB54','#B69C61','#62C04B','#C49EDD','#3B8787','#3A284C','#565DA4','#8ED2AD','#CE7377','#6A4EB8','#489F65','#4192AC','#9A99E0','#83BB72','#456044')

# Add hex color to data from netcolors 
for (name in reldata$Network){
  reldata$HexValue[which(reldata$Network==name)] <- netcolors$`Net Hex`[which(netcolors==name)]
}


# MOTOR Relative Reli vs. PE scatter plot
tiff("Figure5D.tiff", units="in", width=5, height=5, res=1000)
motor_pe <- ggplot( data=reldata, aes(x = `Motor PE`, 
                                y=`Motor Relative Reliability`))+
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
#  ggtitle("Relative Reliability vs. Parameter Estimates" , subtitle = "Motor Task relative to Rest") +
  geom_smooth(method="lm", formula = y ~ x, color = "black", size=0.5) +
  labs(x="PEs", y=expression(~Delta * " FC-TRC")) +
  theme(legend.position = "none")+
  geom_hline(yintercept = 0, color="red", linetype="dashed") +  # Add horizontal line at 0 
  geom_vline(xintercept =0, color="red", linetype="dashed")
  
  
motor_pe <- motor_pe + scale_fill_manual(values=c(unique(reldata$HexValue))) + stat_poly_eq(formula = y ~ x,
                                                                                aes(label = paste(..eq.label.., ..rr.label.., ..p.value.label.., sep = "~~~")),
                                                                                parse=TRUE,label.x.npc = 1, label.y.npc = -1, size = 3.8)

plot(motor_pe)
dev.off()

# Glass Relative Reli vs. PE scatter plot
tiff("Figure5E.tiff", units="in", width=5, height=5, res=1000)
glass_pe <- ggplot( data=reldata, aes(x = `Glass PE`, 
                                      y=`Glass Relative Reliability`))+
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
#  ggtitle("Relative Reliability vs. Parameter Estimates" , subtitle = "Language Task relative to Rest") +
  geom_smooth(method="lm", formula = y ~ x, color = "black", size=0.5) +
#  scale_x_continuous(limits = c(0, 0.125)) +
  labs(x="PEs", y=expression(~Delta * " FC-TRC")) +
  theme(legend.position = "none")+
  geom_hline(yintercept = 0, color="red", linetype="dashed") +  # Add horizontal line at 0 
  geom_vline(xintercept =0, color="red", linetype="dashed")


glass_pe <- glass_pe + scale_fill_manual(values=c(unique(reldata$HexValue))) + stat_poly_eq(formula = y ~ x,
                                                                                           aes(label = paste(..eq.label.., ..rr.label.., ..p.value.label.., sep = "~~~")),
                                                                                         parse=TRUE,label.x.npc = 1, label.y.npc = -1, size = 3.8)

plot(glass_pe)
dev.off()

# Memory Relative Reli vs. PE scatter plot
tiff("Figure5F.tiff", units="in", width=5, height=5, res=1000)
memory_pe <- ggplot( data=reldata, aes(x = `Memory PE`, 
                                      y=`Memory Relative Reliability`))+
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
#  ggtitle("Relative Reliability vs. Parameter Estimates" , subtitle = "Memory Task relative to Rest") +
  geom_smooth(method="lm", formula = y ~ x, color = "black", size=0.5) +
#  scale_x_continuous(limits = c(0, 0.125)) +
  labs(x="PEs", y=expression(~Delta * " FC-TRC")) +
  theme(legend.position = "none")+
  geom_hline(yintercept = 0, color="red", linetype="dashed") +  # Add horizontal line at 0 
  geom_vline(xintercept =0, color="red", linetype="dashed")

memory_pe <- memory_pe + scale_fill_manual(values=c(unique(reldata$HexValue))) + stat_poly_eq(formula = y ~ x,
                                                                                            aes(label = paste(..eq.label.., ..rr.label.., ..p.value.label.., sep = "~~~")),
                                                                                            parse=TRUE,label.x.npc = 1, label.y.npc = -1, size = 3.8)

plot(memory_pe)
dev.off()

