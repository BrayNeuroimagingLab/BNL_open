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
library("plotrix")

rm(list=ls())

# Load Relative data
# This is using relative change formula
# Non regressed data
reldata <- read_excel("/Users/shefalirai/Desktop/New_RelativeChangeReli_Tasks.xlsx", sheet='Sheet1')
motor_noreg <- reldata[,c(2,6)]
motor_noreg <- aggregate(. ~ `Network Name`, data=motor_noreg, mean)



# Color order
netcolors <- data.frame(c(unique(motor_noreg$Network)), unique(motor_noreg$Network))
colnames(netcolors) <- c('Net Names', 'Net Hex')
netcolors$`Net Hex`<- c('#EA3327','#0505A6','#FAF651','#B69C61','#62C04B','#C49EDD','#3B8787','#3A284C','#565DA4','#8ED2AD','#CE7377','#6A4EB8','#489F65','#4192AC','#9A99E0','#83BB72','#456044')
motor_noreg[,3] <- netcolors$`Net Hex`
colnames(motor_noreg) <- c("Network", "Change", "Hex")



# No Regression Motor Bar plot
motor_noreg %>%
  ggplot(aes(x=reorder(Network, Change), y = Change*100, fill=Hex)) +
  geom_bar(stat="identity")+
  ggtitle("Percent Change in Relative Reliability" , subtitle = "Motor Task relative to Rest") +
  coord_flip()+
  theme(panel.background = element_rect(fill='white'),
        panel.border = element_blank(),
        axis.line = element_line(colour = "black"),
        plot.title = element_text(hjust = 0.5),
        plot.subtitle = element_text(hjust = 0.5),
        plot.caption = element_text(size = 8, 
                                    face = "italic",
                                    color = "#5F6375",
                                    margin = margin(t = 15))) +
  labs(
    x = "",
    y = "% Change",
    title = "Change in Relative Reliability between Motor task and Rest",
    subtitle = "No Task Regression"  )+
  theme(legend.position = "none") +  
  scale_fill_manual(values=c("#0505A6","#B69C61","#EA3327", "#FAF651", "#62C04B","#3B8787","#C49EDD","#565DA4","#83BB72","#9A99E0","#4192AC","#6A4EB8","#489F65","#456044","#CE7377","#8ED2AD","#3A284C"))




#Glass data
reldata <- read_excel("/Users/shefalirai/Desktop/New_RelativeChangeReli_Tasks.xlsx", sheet='Sheet1')
glass_noreg <- reldata[,c(3,6)]
glass_noreg <- aggregate(. ~ `Network Name`, data=glass_noreg, mean)



# Color order
netcolors <- data.frame(c(unique(glass_noreg$Network)), unique(glass_noreg$Network))
colnames(netcolors) <- c('Net Names', 'Net Hex')
netcolors$`Net Hex`<- c('#EA3327','#0505A6','#FAF651','#B69C61','#62C04B','#C49EDD','#3B8787','#3A284C','#565DA4','#8ED2AD','#CE7377','#6A4EB8','#489F65','#4192AC','#9A99E0','#83BB72','#456044')
glass_noreg[,3] <- netcolors$`Net Hex`
colnames(glass_noreg) <- c("Network", "Change", "Hex")



# No Regression glass Bar plot
glass_noreg %>%
  ggplot(aes(x=reorder(Network, Change), y = Change*100, fill=Hex)) +
  geom_bar(stat="identity")+
  ggtitle("Percent Change in Relative Reliability" , subtitle = "Language Task relative to Rest") +
  coord_flip()+
  theme(panel.background = element_rect(fill='white'),
        panel.border = element_blank(),
        axis.line = element_line(colour = "black"),
        plot.title = element_text(hjust = 0.5),
        plot.subtitle = element_text(hjust = 0.5),
        plot.caption = element_text(size = 8, 
                                    face = "italic",
                                    color = "#5F6375",
                                    margin = margin(t = 15))) +
  labs(
    x = "",
    y = "% Change",
    title = "Change in Relative Reliability between Language task and Rest",
    subtitle = "No Task Regression"  )+
  theme(legend.position = "none") +  
  scale_fill_manual(values=c("#0505A6","#B69C61","#EA3327", "#FAF651", "#62C04B","#3B8787","#C49EDD","#565DA4","#83BB72","#9A99E0","#4192AC","#6A4EB8","#489F65","#456044","#CE7377","#8ED2AD","#3A284C"))


#Memory data
reldata <- read_excel("/Users/shefalirai/Desktop/New_RelativeChangeReli_Tasks.xlsx", sheet='Sheet1')
memory_noreg <- reldata[,c(4,6)]
memory_noreg <- aggregate(. ~ `Network Name`, data=memory_noreg, mean)



# Color order
netcolors <- data.frame(c(unique(memory_noreg$Network)), unique(memory_noreg$Network))
colnames(netcolors) <- c('Net Names', 'Net Hex')
netcolors$`Net Hex`<- c('#EA3327','#0505A6','#FAF651','#B69C61','#62C04B','#C49EDD','#3B8787','#3A284C','#565DA4','#8ED2AD','#CE7377','#6A4EB8','#489F65','#4192AC','#9A99E0','#83BB72','#456044')
memory_noreg[,3] <- netcolors$`Net Hex`
colnames(memory_noreg) <- c("Network", "Change", "Hex")



# No Regression memory Bar plot
memory_noreg %>%
  ggplot(aes(x=reorder(Network, Change), y = Change*100, fill=Hex)) +
  geom_bar(stat="identity")+
  ggtitle("Percent Change in Relative Reliability" , subtitle = "Memory Task relative to Rest") +
  coord_flip()+
  theme(panel.background = element_rect(fill='white'),
        panel.border = element_blank(),
        axis.line = element_line(colour = "black"),
        plot.title = element_text(hjust = 0.5),
        plot.subtitle = element_text(hjust = 0.5),
        plot.caption = element_text(size = 8, 
                                    face = "italic",
                                    color = "#5F6375",
                                    margin = margin(t = 15))) +
  labs(
    x = "",
    y = "% Change",
    title = "Change in Relative Reliability between Memory task and Rest",
    subtitle = "No Task Regression"  )+
  theme(legend.position = "none") +  
  scale_fill_manual(values=c("#0505A6","#B69C61","#EA3327", "#FAF651", "#62C04B","#3B8787","#C49EDD","#565DA4","#83BB72","#9A99E0","#4192AC","#6A4EB8","#489F65","#456044","#CE7377","#8ED2AD","#3A284C"))






