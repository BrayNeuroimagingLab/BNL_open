# Libraries
options(knitr.table.format = "html")
library(tidyverse)
library(hrbrthemes)
library(kableExtra)
library(readxl)
library(ggplot2)
library(plyr)
library(dplyr)
library(ggprism)
library(patchwork)
library(ggpmisc)
library(cowplot)
library(ggpubr)
library("RColorBrewer")  
library("plotrix")
library(ggsignif)
library(rstatix)
library(reshape)
library(datarium)


rm(list=ls())

# Load dataset
data <- read_excel("/Users/shefalirai/Desktop/NetworknameandnumberID.xlsx", sheet='Sheet1')
data <- data[,1:4]
colnames(data) <- c("Reliability","Network", "NetworkNames","HexValue")

# Color order
netcolors <- data.frame(c(unique(data$NetworkNames)), unique(data$Network))
colnames(netcolors) <- c('Net Names', 'Net Hex')
netcolors$`Net Hex`<- c('#EA3327','#0505A6','#DEDB54','#B69C61','#62C04B','#C49EDD','#3B8787','#3A284C','#565DA4','#8ED2AD','#CE7377','#6A4EB8','#489F65','#4192AC','#9A99E0','#83BB72','#456044')

# Add hex color to data from netcolors 
for (name in data$NetworkNames){
  data$HexValue[which(data$NetworkNames==name)] <- netcolors$`Net Hex`[which(netcolors==name)]
}


# Reliability plot
tiff("Figure1C.tiff", units="in", width=5, height=5, res=1000)
reli <- ggplot(data=data, aes(x=reorder(NetworkNames, Reliability), y = Reliability)) +
  geom_point(aes(fill = NetworkNames), size=3, shape=21, stroke=NA)+
  coord_flip()+
  theme(panel.background = element_rect(fill='white'),
        panel.border = element_blank(),
        axis.line = element_line(colour = "black"),
        plot.title = element_text(hjust = 0.5),
        plot.subtitle = element_text(hjust = 0.5),
        axis.text.x = element_text(colour = "black"),
        axis.text.y = element_text(colour = "black"),
        axis.ticks = element_line(color = "black"),
        plot.caption = element_text(size = 8, 
                                    face = "italic",
                                    color = "#5F6375",
                                    margin = margin(t = 15))) +
  ylim(0.3,0.95)+
  stat_summary(fun=mean, size=0.4, color="black", geom="crossbar")+
  labs(x="Network", y="fc-TRC") + 
  theme(legend.position = "none")+
  scale_fill_manual(values=c(
    "#83BB72",
    "#9A99E0",
    "#C49EDD",
    "#EA3327",
    "#3B8787",
    "#DEDB54",
    "#6A4EB8",
    "#8ED2AD",
    "#B69C61",
    "#62C04B",
    "#456044",
    "#CE7377",
    "#3A284C",
    "#489F65",
    "#565DA4",
    "#4192AC",
    "#0505A6"))
plot(reli)
dev.off()

# # Load dataset
# relidata <- read_excel("/Users/shefalirai/Desktop/NetworknameandnumberID.xlsx", sheet='Reli Fig NOMSC08')
# relidata <- relidata[,-3]
# colnames(relidata) <- c("Reliability","NetworkNames", "Network")
# 
# # Reliability Barplot
# relidata %>%
#   ggplot( aes(x = reorder(NetworkNames, +Reliability), y = Reliability, fill=NetworkNames) ) +
#   geom_bar(stat="identity") +
#   coord_flip() +
#   theme_ipsum() +
#   theme(
#     panel.grid.minor.y = element_blank(),
#     panel.grid.major.y = element_blank(),
#     legend.position="none"
#   ) +
#   xlab("") +
#   ylab("Test-Retest Correlation")
# 
# Load dataset
iccdata <- read_excel("/Users/shefalirai/Desktop/NetworknameandnumberID.xlsx", sheet='ICC21 Fig NOMSC08')
iccdata <- iccdata[1:1000,1:3]
iccdata[,4] <- data[,4]
colnames(iccdata) <- c("ICC","Network", "NetworkNames",'HexValue')


# ICC plot
tiff("Figure1D.tiff", units="in", width=5, height=5, res=1000)
ICC <- ggplot(data=iccdata, aes(x=reorder(NetworkNames, ICC), y = ICC)) +
  geom_point(aes(fill = NetworkNames), size=3, shape=21, stroke=NA)+
  coord_flip()+
  theme(panel.background = element_rect(fill='white'),
        panel.border = element_blank(),
        axis.line = element_line(colour = "black"),
        plot.title = element_text(hjust = 0.5),
        plot.subtitle = element_text(hjust = 0.5),
        axis.text.x = element_text(colour = "black"),
        axis.text.y = element_text(colour = "black"),
        axis.ticks = element_line(color = "black"),
        plot.caption = element_text(size = 8, 
                                    face = "italic",
                                    color = "#5F6375",
                                    margin = margin(t = 15))) +
  ylim(0.3,0.95)+
  stat_summary(fun=mean, size=0.4, color="black", geom="crossbar")+
  geom_hline(yintercept = 0.4, color="darkred", linetype="dashed") +  
  geom_hline(yintercept = 0.59, color="darkorange", linetype="dashed") +  
  geom_hline(yintercept = 0.74, color="darkgreen", linetype="dashed") +  
  labs(x="Network", y="ICC") + 
  theme(legend.position = "none")+
  scale_fill_manual(values=c(
    "#83BB72",
    "#9A99E0",
    "#C49EDD",
    "#EA3327",
    "#3B8787",
    "#DEDB54",
    "#6A4EB8",
    "#8ED2AD",
    "#B69C61",
    "#62C04B",
    "#456044",
    "#CE7377",
    "#3A284C",
    "#489F65",
    "#565DA4",
    "#4192AC",
    "#0505A6"))
plot(ICC)
dev.off()



