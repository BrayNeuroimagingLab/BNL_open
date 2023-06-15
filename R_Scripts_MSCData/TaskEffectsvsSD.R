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

reldata <- read_excel("/Users/shefalirai/Desktop/MSCData.xlsx", sheet='ZSTAT_3rdLevel')
reldata[,10] <- c(1:998)
colnames(reldata) <- c("Rest Full Reliability","Motor ZSTAT", "Motor SD", "Glass ZSTAT", "Glass SD", "Memory ZSTAT", "Memory SD","Network", "Network Name", "HexValue")


data <- read_excel("/Users/shefalirai/Desktop/MSCData.xlsx", sheet='PEBetas_3rdLevel')
data[,9] <- c(1:998)
colnames(data) <- c("Motor Relative Reliability", "Motor PE", "Glass Relative Reliability", "Glass PE", "Memory Relative Reliability", "Memory PE","Network", "Network Name", "HexValue")

# Color order
netcolors <- data.frame(c(unique(reldata$Network)), unique(reldata$Network))
colnames(netcolors) <- c('Net Names', 'Net Hex')
netcolors$`Net Hex`<- c('#EA3327','#0505A6','#FAF651','#B69C61','#62C04B','#C49EDD','#3B8787','#3A284C','#565DA4','#8ED2AD','#CE7377','#6A4EB8','#489F65','#4192AC','#9A99E0','#83BB72','#456044')

# Add hex color to data from netcolors 
for (name in reldata$Network){
  reldata$HexValue[which(reldata$Network==name)] <- netcolors$`Net Hex`[which(netcolors==name)]
}


# MOTOR Relative Reli vs. PE scatter plot
newdata<-data
newdata[,10:16] <- reldata[,1:7]
tiff("Figure5G.tiff", units="in", width=5, height=5, res=1000)
motor_PE <- ggplot( data=newdata, aes(x = `Motor PE`, 
                                      y=`Motor SD`))+
  geom_rect(data=NULL,aes(xmin=-Inf,xmax=Inf,ymin=-Inf,ymax=0),
            fill="#ededed")+
  geom_rect(data=NULL,aes(xmin=-Inf,xmax=0,ymin=-Inf,ymax=Inf),
            fill="#ededed")+
  theme(panel.background = element_rect(fill='white'),
        panel.border = element_blank(),
        axis.line = element_line(colour = "black"))+
  geom_point(aes(fill = factor(Network, levels = unique(Network))), size=3, shape=21, stroke=NA) +
#  ggtitle("SD vs. Parameter Estimates (Betas)" , subtitle = "Motor Task relative to Rest") +
  geom_smooth(method="lm", formula = y ~ x, color = "black", size=0.5) +
  labs(x="Parameter Estimates", y=expression(~Delta * " tSD")) +
  theme(legend.position = "none")+
  geom_hline(yintercept = 0, color="red", linetype="dashed") +  # Add horizontal line at 0 
  geom_vline(xintercept =0, color="red", linetype="dashed")

motor_PE <- motor_PE + scale_fill_manual(values=c(unique(reldata$HexValue))) + stat_poly_eq(formula = y ~ x,
                                                                                            aes(label = paste(..eq.label.., ..rr.label.., ..p.value.label.., sep = "~~~")),
                                                                                            parse=TRUE,label.x.npc = 1, label.y.npc = -1, size = 3.5)

plot(motor_PE)
dev.off()

# Glass Relative Reli vs. PE scatter plot
tiff("Figure5H.tiff", units="in", width=5, height=5, res=1000)
glass_PE <- ggplot( data=newdata, aes(x = `Glass PE`, 
                                      y=`Glass SD`))+
  geom_rect(data=NULL,aes(xmin=-Inf,xmax=Inf,ymin=-Inf,ymax=0),
            fill="#ededed")+
  geom_rect(data=NULL,aes(xmin=-Inf,xmax=0,ymin=-Inf,ymax=Inf),
            fill="#ededed")+
  theme(panel.background = element_rect(fill='white'),
        panel.border = element_blank(),
        axis.line = element_line(colour = "black"))+
  geom_point(aes(fill = factor(Network, levels = unique(Network))), size=3, shape=21, stroke=NA) +
#  ggtitle("SD vs. Parameter Estimates (Betas)" , subtitle = "Language Task relative to Rest") +
  geom_smooth(method="lm", formula = y ~ x, color = "black", size=0.5) +
  #  scale_x_continuous(limits = c(0, 0.125)) +
  labs(x="Parameter Estimates", y=expression(~Delta* " tSD")) +
  theme(legend.position = "none")+
  geom_hline(yintercept = 0, color="red", linetype="dashed") +  # Add horizontal line at 0 
  geom_vline(xintercept =0, color="red", linetype="dashed")

glass_PE <- glass_PE + scale_fill_manual(values=c(unique(reldata$HexValue))) + stat_poly_eq(formula = y ~ x,
                                                                                            aes(label = paste(..eq.label.., ..rr.label.., ..p.value.label.., sep = "~~~")),
                                                                                            parse=TRUE,label.x.npc = 1, label.y.npc = -1, size = 3.5)

plot(glass_PE)
dev.off()

# Memory Relative Reli vs. PE scatter plot
tiff("Figure5I.tiff", units="in", width=5, height=5, res=1000)
memory_PE <- ggplot( data=newdata, aes(x = `Memory PE`, 
                                       y=`Memory SD`))+
  geom_rect(data=NULL,aes(xmin=-Inf,xmax=Inf,ymin=-Inf,ymax=0),
            fill="#ededed")+
  geom_rect(data=NULL,aes(xmin=-Inf,xmax=0,ymin=-Inf,ymax=Inf),
            fill="#ededed")+
  theme(panel.background = element_rect(fill='white'),
        panel.border = element_blank(),
        axis.line = element_line(colour = "black"))+
  geom_point(aes(fill = factor(Network, levels = unique(Network))), size=3, shape=21, stroke=NA) +
#  ggtitle("SD vs. Parameter Estimates (Betas)" , subtitle = "Memory Task relative to Rest") +
  geom_smooth(method="lm", formula = y ~ x, color = "black", size=0.5) +
  #  scale_x_continuous(limits = c(0, 0.125)) +
  labs(x="Parameter Estimates", y=expression(~Delta* " tSD")) +
  theme(legend.position = "none")+
  geom_hline(yintercept = 0, color="red", linetype="dashed") +  # Add horizontal line at 0 
  geom_vline(xintercept =0, color="red", linetype="dashed")

memory_PE <- memory_PE + scale_fill_manual(values=c(unique(reldata$HexValue))) + stat_poly_eq(formula = y ~ x,
                                                                                              aes(label = paste(..eq.label.., ..rr.label.., ..p.value.label.., sep = "~~~")),
                                                                                              parse=TRUE,label.x.npc = 1, label.y.npc = -1, size = 3.5)

plot(memory_PE)
dev.off()

