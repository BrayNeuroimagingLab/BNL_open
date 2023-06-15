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
reldata <- read_excel("/Users/shefalirai/Desktop/RegvsNoReg.xlsx", sheet='Reg vs NoReg')
motor_noreg <- reldata[,c(5,6)]
motor_reg <- reldata[,c(9,10)]
colnames(motor_reg) <- c("Network", "Change")
colnames(motor_noreg) <- c("Network", "Change")
motor_noreg_change <- aggregate(. ~ Network, data=motor_noreg, mean)
motor_reg_change <- aggregate(. ~ Network, data=motor_reg, mean)

#motor_percentchange <- rbind(motor_noreg_change, motor_reg_change)
#motor_percentchange[,3] <- c(1:34)
#motor_percentchange[1:17,3] <- "No Regression"
#motor_percentchange[18:34,3] <- "Task Regressed"


# Color order
netcolors <- data.frame(c(unique(motor_noreg_change$Network)), unique(motor_noreg_change$Network))
colnames(netcolors) <- c('Net Names', 'Net Hex')
netcolors$`Net Hex`<- c('#EA3327','#0505A6','#FAF651','#B69C61','#62C04B','#C49EDD','#3B8787','#3A284C','#565DA4','#8ED2AD','#CE7377','#6A4EB8','#489F65','#4192AC','#9A99E0','#83BB72','#456044')
motor_noreg_change[,3] <- netcolors$`Net Hex`
motor_noreg_change[,1] <- unique(reldata[,2])
motor_reg_change[,3] <- netcolors$`Net Hex`
motor_reg_change[,1] <- unique(reldata[,2])


ascending_motor_reg_change <- motor_reg_change[order(motor_reg_change$Network),]
ascending_motor_noreg_change <- motor_noreg_change[order(motor_noreg_change$Network),]
colnames(motor_reg_change) <- c("Network", "Change", "Hex")
colnames(motor_noreg_change) <- c("Network", "Change", "Hex")


# No Regression Motor Bar plot
motor_noreg_change %>%
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


# Regression Motor Bar plot
ascending_motor_reg_change %>%
  ggplot(aes(x=Network, y = Change, fill=Hex)) +
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
  scale_y_continuous(limits = c(-15, 15)) +
  labs(
    x = "",
    y = "% Change",
    title = "Change in Relative Reliability between Motor task and Rest",
    subtitle = "Task Regressed"  )+
  theme(legend.position = "none")



#Glass data
# Load Relative data
reldata <- read_excel("/Users/shefalirai/Desktop/RegvsNoReg.xlsx", sheet='Reg vs NoReg')
glass_noreg <- reldata[,c(13,14)]
glass_reg <- reldata[,c(17,18)]
colnames(glass_reg) <- c("Network", "Change")
colnames(glass_noreg) <- c("Network", "Change")
glass_noreg_change <- aggregate(. ~ Network, data=glass_noreg, mean)
glass_reg_change <- aggregate(. ~ Network, data=glass_reg, mean)

#glass_percentchange <- rbind(glass_noreg_change, glass_reg_change)
#glass_percentchange[,3] <- c(1:34)
#glass_percentchange[1:17,3] <- "No Regression"
#glass_percentchange[18:34,3] <- "Task Regressed"


# Color order
netcolors <- data.frame(c(unique(glass_noreg_change$Network)), unique(glass_noreg_change$Network))
colnames(netcolors) <- c('Net Names', 'Net Hex')
netcolors$`Net Hex`<- c('#EA3327','#0505A6','#FAF651','#B69C61','#62C04B','#C49EDD','#3B8787','#3A284C','#565DA4','#8ED2AD','#CE7377','#6A4EB8','#489F65','#4192AC','#9A99E0','#83BB72','#456044')
glass_noreg_change[,3] <- netcolors$`Net Hex`
glass_noreg_change[,1] <- unique(reldata[,2])
glass_reg_change[,3] <- netcolors$`Net Hex`
glass_reg_change[,1] <- unique(reldata[,2])


ascending_glass_reg_change <- glass_reg_change[order(glass_reg_change$Network),]
ascending_glass_noreg_change <- glass_noreg_change[order(glass_noreg_change$Network),]
colnames(ascending_glass_reg_change) <- c("Network", "Change", "Hex")
colnames(ascending_glass_noreg_change) <- c("Network", "Change", "Hex")


# No Regression glass Bar plot
ascending_glass_noreg_change %>%
  ggplot(aes(reorder(Network, Change), y = Change*100, fill=Hex)) +
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
  theme(legend.position = "none")


# Regression glass Bar plot
ascending_glass_reg_change %>%
  ggplot(aes(x=Network, y = Change, fill=Hex)) +
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
  scale_y_continuous(limits = c(-15, 15)) +
  labs(
    x = "",
    y = "% Change",
    title = "Change in Relative Reliability between Language task and Rest",
    subtitle = "Task Regressed"  )+
  theme(legend.position = "none")

#Memory 
# Load Relative data
reldata <- read_excel("/Users/shefalirai/Desktop/RegvsNoReg.xlsx", sheet='Reg vs NoReg')
memory_noreg <- reldata[,c(25,26)]
memory_reg <- reldata[,c(21,22)]
colnames(memory_reg) <- c("Network", "Change")
colnames(memory_noreg) <- c("Network", "Change")
memory_noreg_change <- aggregate(. ~ Network, data=memory_noreg, mean)
memory_reg_change <- aggregate(. ~ Network, data=memory_reg, mean)

#memory_percentchange <- rbind(memory_noreg_change, memory_reg_change)
#memory_percentchange[,3] <- c(1:34)
#memory_percentchange[1:17,3] <- "No Regression"
#memory_percentchange[18:34,3] <- "Task Regressed"


# Color order
netcolors <- data.frame(c(unique(memory_noreg_change$Network)), unique(memory_noreg_change$Network))
colnames(netcolors) <- c('Net Names', 'Net Hex')
netcolors$`Net Hex`<- c('#EA3327','#0505A6','#FAF651','#B69C61','#62C04B','#C49EDD','#3B8787','#3A284C','#565DA4','#8ED2AD','#CE7377','#6A4EB8','#489F65','#4192AC','#9A99E0','#83BB72','#456044')
memory_noreg_change[,3] <- netcolors$`Net Hex`
memory_noreg_change[,1] <- unique(reldata[,2])
memory_reg_change[,3] <- netcolors$`Net Hex`
memory_reg_change[,1] <- unique(reldata[,2])


ascending_memory_reg_change <- memory_reg_change[order(memory_reg_change$Network),]
ascending_memory_noreg_change <- memory_noreg_change[order(memory_noreg_change$Network),]
colnames(ascending_memory_reg_change) <- c("Network", "Change", "Hex")
colnames(ascending_memory_noreg_change) <- c("Network", "Change", "Hex")


# No Regression memory Bar plot
ascending_memory_noreg_change %>%
  ggplot(aes(reorder(Network, Change), y = Change*100, fill=Hex)) +
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
  theme(legend.position = "none")


# Regression memory Bar plot
ascending_memory_reg_change %>%
  ggplot(aes(x=Network, y = Change, fill=Hex)) +
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
  scale_y_continuous(limits = c(-15, 18)) +
  labs(
    x = "",
    y = "% Change",
    title = "Change in Relative Reliability between Memory task and Rest",
    subtitle = "Task Regressed"  )+
  theme(legend.position = "none")




