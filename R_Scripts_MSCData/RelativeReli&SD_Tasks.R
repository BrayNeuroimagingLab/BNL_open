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
reldata <- read_excel("/Users/shefalirai/Desktop/Rest_NoMSC08_MotorMatched_copy.xlsx", sheet='RestSD-TaskSD')
reldata[,10] <- c(1:1000)
colnames(reldata) <- c("Rest SD", "Motor SD", "Language SD", "Memory SD", "Rest Reliability", "Motor Reliability", "Language Reliability", "Memory Reliability", "Network", "HexValue")

# Color order
netcolors <- data.frame(c(unique(reldata$Network)), unique(reldata$Network))
colnames(netcolors) <- c('Net Names', 'Net Hex')
netcolors$`Net Hex`<- c('#EA3327','#0505A6','#FAF651','#B69C61','#62C04B','#C49EDD','#3B8787','#3A284C','#565DA4','#8ED2AD','#CE7377','#6A4EB8','#489F65','#4192AC','#9A99E0','#83BB72','#456044')

# Add hex color to data from netcolors 
for (name in reldata$Network){
  reldata$HexValue[which(reldata$Network==name)] <- netcolors$`Net Hex`[which(netcolors==name)]
}

# MOTOR Relative SD vs. reliability scatter plot

sd <- ggplot( data=reldata, aes(x = `Motor SD`-`Rest SD`, 
                             y=`Motor Reliability`-`Rest Reliability`)) +
  theme(panel.background = element_rect(fill='white'),
        panel.border = element_blank(),
        axis.line = element_line(colour = "black"))+
  geom_point(aes(fill = factor(Network, levels = unique(Network))), size=2, shape=21) +
  ggtitle("Relative Reliability vs. Relative SD" , subtitle = "Motor Task relative to Rest") +
  geom_smooth(method="lm", formula = y ~ x, color = "black", size=0.5) +
  labs(x="Standard Deviation", y="Test-Retest Correlation") + 
  theme(legend.position = "none")

sd <- sd + scale_fill_manual(values=c(unique(reldata$HexValue))) + stat_poly_eq(formula = y ~ x,
                                                                             aes(label = paste(..eq.label.., ..rr.label..,signif(..p.value.., digits = 4), sep = "~~~")), 
                                                                             parse=TRUE,label.x.npc = "right", label.y.npc = "bottom", size = 3.5)

plot(sd)



#Language Relative SD vs. reliability scatter plot

sd2 <- ggplot( data=reldata, aes(x = `Language SD`-`Rest SD`, 
                                y=`Language Reliability`-`Rest Reliability`)) +
  theme(panel.background = element_rect(fill='white'),
        panel.border = element_blank(),
        axis.line = element_line(colour = "black"))+
  geom_point(aes(fill = factor(Network, levels = unique(Network))), size=2, shape=21) +
  ggtitle("Relative Reliability vs. Relative SD" , subtitle = "Language Task relative to Rest") +
  geom_smooth(method="lm", formula = y ~ x, color = "black", size=0.5) +
  labs(x="Standard Deviation", y="Test-Retest Correlation") + 
  theme(legend.position = "none")

sd2 <- sd2 + scale_fill_manual(values=c(unique(reldata$HexValue))) + stat_poly_eq(formula = y ~ x,
                                                                                aes(label = paste(..eq.label.., ..rr.label..,signif(..p.value.., digits = 4), sep = "~~~")), 
                                                                                parse=TRUE,label.x.npc = "right", label.y.npc = "bottom", size = 3.5)

plot(sd2)


#Memory Relative SD vs. reliability scatter plot

sd3 <- ggplot( data=reldata, aes(x = `Memory SD`-`Rest SD`, 
                                 y=`Memory Reliability`-`Rest Reliability`)) +
  theme(panel.background = element_rect(fill='white'),
        panel.border = element_blank(),
        axis.line = element_line(colour = "black"))+
  geom_point(aes(fill = factor(Network, levels = unique(Network))), size=2, shape=21) +
  ggtitle("Relative Reliability vs. Relative SD" , subtitle = "Memory Task relative to Rest") +
  geom_smooth(method="lm", formula = y ~ x, color = "black", size=0.5) +
  labs(x="Standard Deviation", y="Test-Retest Correlation") + 
  theme(legend.position = "none")

sd3 <- sd3 + scale_fill_manual(values=c(unique(reldata$HexValue))) + stat_poly_eq(formula = y ~ x,
                                                                                  aes(label = paste(..eq.label.., ..rr.label..,signif(..p.value.., digits = 4), sep = "~~~")), 
                                                                                  parse=TRUE,label.x.npc = "right", label.y.npc = "bottom", size = 3.5)

plot(sd3)


