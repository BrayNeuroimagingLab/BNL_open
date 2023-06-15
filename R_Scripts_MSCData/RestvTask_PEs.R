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
netcolors$`Net Hex`<- c('#EA3327','#0505A6','#FAF651','#B69C61','#62C04B','#C49EDD','#3B8787','#3A284C','#565DA4','#8ED2AD','#CE7377','#6A4EB8','#489F65','#4192AC','#9A99E0','#83BB72','#456044')

# Add hex color to data from netcolors 
for (name in reldata$Network){
  reldata$HexValue[which(reldata$Network==name)] <- netcolors$`Net Hex`[which(netcolors==name)]
}


# MOTOR Relative Reli vs. PE scatter plot

motor_pe <- ggplot( data=reldata, aes(x = `Motor PE`, 
                                y=`Motor Relative Reliability`))+
  theme(panel.background = element_rect(fill='white'),
        panel.border = element_blank(),
        axis.line = element_line(colour = "black"))+
  geom_point(aes(fill = factor(Network, levels = unique(Network))), size=2, shape=21) +
  ggtitle("Relative Reliability vs. Parameter Estimates" , subtitle = "Motor Task relative to Rest") +
  geom_smooth(method="lm", formula = y ~ x, color = "black", size=0.5) +
  labs(x="Parameter Estimates (Betas)", y=expression(~Delta * " Test-Retest Correlation")) +
  theme(legend.position = "none")

motor_pe <- motor_pe + scale_fill_manual(values=c(unique(reldata$HexValue))) + stat_poly_eq(formula = y ~ x,
                                                                                aes(label = paste(..eq.label.., ..rr.label..,signif(..p.value.., digits = 4), sep = "~~~")),
                                                                                parse=TRUE,label.x.npc = "right", label.y.npc = "bottom", size = 3.5)

plot(motor_pe)


# Glass Relative Reli vs. PE scatter plot

glass_pe <- ggplot( data=reldata, aes(x = `Glass PE`, 
                                      y=`Glass Relative Reliability`))+
  theme(panel.background = element_rect(fill='white'),
        panel.border = element_blank(),
        axis.line = element_line(colour = "black"))+
  geom_point(aes(fill = factor(Network, levels = unique(Network))), size=2, shape=21) +
  ggtitle("Relative Reliability vs. Parameter Estimates" , subtitle = "Language Task relative to Rest") +
  geom_smooth(method="lm", formula = y ~ x, color = "black", size=0.5) +
  labs(x="PE (Beta)", y=expression(~Delta* " Test-Retest Correlation")) +
  theme(legend.position = "none")

glass_pe <- glass_pe + scale_fill_manual(values=c(unique(reldata$HexValue))) + stat_poly_eq(formula = y ~ x,
                                                                                            aes(label = paste(..eq.label.., ..rr.label..,signif(..p.value.., digits = 4), sep = "~~~")),
                                                                                            parse=TRUE,label.x.npc = "right", label.y.npc = "bottom", size = 3.5)

plot(glass_pe)


# Memory Relative Reli vs. PE scatter plot

memory_pe <- ggplot( data=reldata, aes(x = `Memory PE`, 
                                      y=`Memory Relative Reliability`))+
  theme(panel.background = element_rect(fill='white'),
        panel.border = element_blank(),
        axis.line = element_line(colour = "black"))+
  geom_point(aes(fill = factor(Network, levels = unique(Network))), size=2, shape=21) +
  ggtitle("Relative Reliability vs. Parameter Estimates" , subtitle = "Memory Task relative to Rest") +
  geom_smooth(method="lm", formula = y ~ x, color = "black", size=0.5) +
  labs(x="PE (Beta)", y=expression(~Delta* " Test-Retest Correlation")) +
  theme(legend.position = "none")

memory_pe <- memory_pe + scale_fill_manual(values=c(unique(reldata$HexValue))) + stat_poly_eq(formula = y ~ x,
                                                                                            aes(label = paste(..eq.label.., ..rr.label..,signif(..p.value.., digits = 4), sep = "~~~")),
                                                                                            parse=TRUE,label.x.npc = "right", label.y.npc = "bottom", size = 3.5)

plot(memory_pe)


