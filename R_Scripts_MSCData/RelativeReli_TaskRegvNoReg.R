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
motor_reldata <- reldata[c(2:6,8:12),28:31]
motor_reldata[1:5,4] <- "No Regression"
motor_reldata[6:10,4] <- "Task Regression"
colnames(motor_reldata) <- c("Values","Percent","Network","Regressed")

#Motor Relative reliability all data
motor_rel_all_noreg <- reldata[,3:6]
motor_rel_all_noreg[,5] <- motor_rel_all_noreg[,4]*100
colnames(motor_rel_all_noreg) <- c("Motor Reliability", "Rest Reliability", "Network", "Change","Percent Change")

motor_rel_all_reg <- reldata[,7:10]
motor_rel_all_reg[,5] <- motor_rel_all_reg[,4]*100
colnames(motor_rel_all_reg) <- c("Motor Reliability", "Rest Reliability", "Network", "Change","Percent Change")


#calculate se of motor networks
data_summary <- function(data, varname, groupnames){
  require(plyr)
  summary_func <- function(x, col){
    c(mean = mean(x[[col]], na.rm=TRUE),
      ster = std.error((x[[col]])))
  }
  data_sum<-ddply(data, groupnames, .fun=summary_func,
                  varname)
  data_sum <- rename(data_sum, c("mean" = varname))
  return(data_sum)
}
motor_se_noreg <- data_summary(motor_rel_all_noreg, varname="Percent Change", 
                    groupnames="Network")
motor_se_reg <- data_summary(motor_rel_all_reg, varname="Percent Change", 
                               groupnames="Network")

motor_se <- rbind(motor_se_noreg, motor_se_reg)

motor_reldata[,5] <- motor_se[c(5,10,2,3,4,22,27,19,20,21),3]
colnames(motor_reldata) <- c("Values","Percent","Network","Regressed","SE")

# Motor Bar plot
motor_reldata %>%
  ggplot(aes(x = Network, y = Percent, fill =Regressed)) +
  geom_bar(stat="identity", position=position_dodge())+
  ggtitle("Percent Change in Relative Reliability" , subtitle = "Motor Task relative to Rest") +
  geom_errorbar(aes(ymin=Percent-SE, ymax=Percent+SE), width=.2,
                position=position_dodge(.9)) + 
  theme(panel.background = element_rect(fill='white'),
      panel.border = element_blank(),
      axis.line = element_line(colour = "black"),
      plot.title = element_text(hjust = 0.5),
      plot.subtitle = element_text(hjust = 0.5),
      legend.title = element_blank(),
      plot.caption = element_text(size = 8, 
                                  face = "italic",
                                  color = "#5F6375",
                                  margin = margin(t = 15))) +
  labs(
    x = "",
    y = "% Change",
    title = "Percent Change in Relative Reliability",
    subtitle = "Motor Task relative to Rest",
    caption = "Error bars indicate standard error"
  )+
  scale_fill_manual(values=c("lightgray","#5F6369"))






#Glass data
reldata <- read_excel("/Users/shefalirai/Desktop/RegvsNoReg.xlsx", sheet='Reg vs NoReg')
glass_reldata <- reldata[c(16:20,22:26),28:31]
glass_reldata[1:5,4] <- "No Regression"
glass_reldata[6:10,4] <- "Task Regression"
colnames(glass_reldata) <- c("Values","Percent","Network","Regressed")

#Glass Relative reliability all data
glass_rel_all_noreg <- reldata[,11:14]
glass_rel_all_noreg[,5] <- glass_rel_all_noreg[,4]*100
colnames(glass_rel_all_noreg) <- c("Glass Reliability", "Rest Reliability", "Network", "Change","Percent Change")

glass_rel_all_reg <- reldata[,15:18]
glass_rel_all_reg[,5] <- glass_rel_all_reg[,4]*100
colnames(glass_rel_all_reg) <- c("Glass Reliability", "Rest Reliability", "Network", "Change","Percent Change")


#calculate se of glass networks
data_summary <- function(data, varname, groupnames){
  require(plyr)
  summary_func <- function(x, col){
    c(mean = mean(x[[col]], na.rm=TRUE),
      ster = std.error((x[[col]])))
  }
  data_sum<-ddply(data, groupnames, .fun=summary_func,
                  varname)
  data_sum <- rename(data_sum, c("mean" = varname))
  return(data_sum)
}
glass_se_noreg <- data_summary(glass_rel_all_noreg, varname="Percent Change", 
                               groupnames="Network")
glass_se_reg <- data_summary(glass_rel_all_reg, varname="Percent Change", 
                             groupnames="Network")

glass_se <- rbind(glass_se_noreg, glass_se_reg)

glass_reldata[,5] <- glass_se[c(5,10,2,3,4,22,27,19,20,21),3]
colnames(glass_reldata) <- c("Values","Percent","Network","Regressed","SE")


#Glass Bar plot
glass_reldata %>%
  group_by(Regressed) %>%
  arrange(desc(Percent)) %>%
  ggplot(aes(x = Network, y = Percent, fill = Regressed)) +
  geom_bar(stat="identity", position=position_dodge())+
  ggtitle("Percent Change in Relative Reliability" , subtitle = "Language Task relative to Rest") +
  geom_errorbar(aes(ymin=Percent-SE, ymax=Percent+SE), width=.2,
                position=position_dodge(.9)) + 
  theme(panel.background = element_rect(fill='white'),
        panel.border = element_blank(),
        axis.line = element_line(colour = "black"),
        plot.title = element_text(hjust = 0.5),
        plot.subtitle = element_text(hjust = 0.5),
        legend.title = element_blank(),
        plot.caption = element_text(size = 8, 
                                    face = "italic",
                                    color = "#5F6375",
                                    margin = margin(t = 15))) +
  labs(
    x = "",
    y = "% Change",
    title = "Percent Change in Relative Reliability",
    subtitle = "Language Task relative to Rest",
    caption = "Error bars indicate standard error"
  )+
  scale_fill_manual(values=c("lightgray","#5F6369"))


#Memory data
reldata <- read_excel("/Users/shefalirai/Desktop/RegvsNoReg.xlsx", sheet='Reg vs NoReg')
memory_reldata <- reldata[c(30:34,36:40),28:31]
memory_reldata[1:5,4] <- "No Regression"
memory_reldata[6:10,4] <- "Task Regression"
colnames(memory_reldata) <- c("Values","Percent","Network","Regressed")


#Memory Relative reliability all data
memory_rel_all_noreg <- reldata[,23:26]
memory_rel_all_noreg[,5] <- memory_rel_all_noreg[,4]*100
colnames(memory_rel_all_noreg) <- c("Memory Reliability", "Rest Reliability", "Network", "Change","Percent Change")

memory_rel_all_reg <- reldata[,19:22]
memory_rel_all_reg[,5] <- memory_rel_all_reg[,4]*100
colnames(memory_rel_all_reg) <- c("Memory Reliability", "Rest Reliability", "Network", "Change","Percent Change")


#calculate se of memory networks
data_summary <- function(data, varname, groupnames){
  require(plyr)
  summary_func <- function(x, col){
    c(mean = mean(x[[col]], na.rm=TRUE),
      ster = std.error((x[[col]])))
  }
  data_sum<-ddply(data, groupnames, .fun=summary_func,
                  varname)
  data_sum <- rename(data_sum, c("mean" = varname))
  return(data_sum)
}
memory_se_noreg <- data_summary(memory_rel_all_noreg, varname="Percent Change", 
                               groupnames="Network")
memory_se_reg <- data_summary(memory_rel_all_reg, varname="Percent Change", 
                             groupnames="Network")

memory_se <- rbind(memory_se_noreg, memory_se_reg)

memory_reldata[,5] <- memory_se[c(5,10,2,3,4,22,27,19,20,21),3]
colnames(memory_reldata) <- c("Values","Percent","Network","Regressed","SE")


#memory Bar plot
memory_reldata %>%
  group_by(Regressed) %>%
  arrange(desc(Percent)) %>%
  ggplot(aes(x = Network, y = Percent, fill = Regressed)) +
  geom_bar(stat="identity", position=position_dodge())+
  ggtitle("Percent Change in Relative Reliability" , subtitle = "Language Task relative to Rest") +
  geom_errorbar(aes(ymin=Percent-SE, ymax=Percent+SE), width=.2,
                position=position_dodge(.9)) + 
  theme(panel.background = element_rect(fill='white'),
        panel.border = element_blank(),
        axis.line = element_line(colour = "black"),
        plot.title = element_text(hjust = 0.5),
        plot.subtitle = element_text(hjust = 0.5),
        legend.title = element_blank(),
        plot.caption = element_text(size = 8, 
                                    face = "italic",
                                    color = "#5F6375",
                                    margin = margin(t = 15))) +
  labs(
    x = "",
    y = "% Change",
    title = "Percent Change in Relative Reliability",
    subtitle = "Memory Task relative to Rest",
    caption = "Error bars indicate standard error"
  )+
  scale_fill_manual(values=c("lightgray","#5F6369"))


# #Alternative to bar plot, using dot plots
# right_label <- motor_reldata %>%
#   group_by(Network) %>%
#   arrange(desc(Percent)) %>%
#   top_n(1)
# 
# left_label <- motor_reldata %>%
#   group_by(Network) %>%
#   arrange(desc(Percent)) %>%
#   slice(2)
# 
# ggplot(motor_reldata, aes(Percent, Network)) +
#   geom_line(aes(group = Network)) +
#   geom_point(aes(color = Regressed), size = 1.5) +
#   geom_text(data = right_label, aes(color = Regressed, label = round(Percent, 0)),
#             size = 3, hjust = -.5) +
#   geom_text(data = left_label, aes(color = Regressed, label = round(Percent, 0)),
#             size = 3, hjust = 1.5) +
#   scale_x_continuous(limits = c(0, 100))








