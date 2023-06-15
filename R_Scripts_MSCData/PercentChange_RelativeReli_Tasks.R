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

# Load Relative data
reldata <- read_excel("/Users/shefalirai/Desktop/MSCData.xlsx", sheet='RelativeReli_NoRegression')

#Calculate Percent change for motor task
change_reldata_motor <- (aggregate(reldata$`Motor Relative Reliability`~reldata$Network,reldata,sum))/(aggregate(reldata$`Motor Relative Reliability`~reldata$Network,reldata,length))
percentchange_reldata_motor <- change_reldata_motor*100
percentchange_reldata_motor[,1] <- unique(reldata$`Network Name`)
colnames(percentchange_reldata_motor) <- c("Network", "Motor_RelativeReli")

# Color order
netcolors <- data.frame(c(percentchange_reldata_motor$Network), percentchange_reldata_motor$Network)
colnames(netcolors) <- c('Net Names', 'Net Hex')
netcolors$`Net Hex`<- c('#EA3327','#0505A6','#DEDB54','#B69C61','#62C04B','#C49EDD','#3B8787','#3A284C','#565DA4','#8ED2AD','#CE7377','#6A4EB8','#489F65','#4192AC','#9A99E0','#83BB72','#456044')
percentchange_reldata_motor[,3] <- netcolors$`Net Hex`
colnames(percentchange_reldata_motor) <- c("Network", "Change", "Hex")


# # Motor Percent Change No Regression Bar plot
# percentchange_reldata_motor %>%
#   ggplot(aes(x=reorder(Network, Change), y = Change, fill=Hex)) +
#   geom_bar(stat="identity")+
#   ggtitle("Percent Change in Relative Reliability between Motor Task and Rest" , subtitle = "No Task Regression") +
#   coord_flip()+
#   geom_signif(comparisons = list(c("Face Somatomotor", "Cingulo-Opercular B")), 
#               map_signif_level=TRUE) + 
#   theme(panel.background = element_rect(fill='white'),
#         panel.border = element_blank(),
#         axis.line = element_line(colour = "black"),
#         plot.title = element_text(hjust = 0.5),
#         plot.subtitle = element_text(hjust = 0.5),
#         plot.caption = element_text(size = 8, 
#                                     face = "italic",
#                                     color = "#5F6375",
#                                     margin = margin(t = 15))) +
#   labs(
#     x = "",
#     y = "% Change")+
#   theme(legend.position = "none") +  
#   scale_fill_manual(values=c("#0505A6","#B69C61","#EA3327", "#DEDB54", "#62C04B","#3B8787","#C49EDD","#565DA4","#83BB72","#9A99E0","#4192AC","#6A4EB8","#489F65","#456044","#CE7377","#8ED2AD","#3A284C"))
# 


# # Motor Relative Absolute Values No Regression Box plot
# # boxplot with anova against base mean
# ggboxplot(reldata, x = "Network Name", y = "Motor Relative Reliability", color="Network",
#           palette= ,add = "jitter", legend = "none") +
#   ggtitle("Relative Reliability between motor task and rest" , subtitle = "No Task Regression") +
#   coord_flip() + 
#   geom_hline(yintercept = mean(reldata$`Motor Relative Reliability`), linetype = 2)+ # Add horizontal line at base mean
#   stat_compare_means(label = "p.signif", method = "t.test",
#                      ref.group = ".all.", hide.ns = TRUE)      # Pairwise comparison against all

#Motor scatterplot for relative reliablity 
tiff("Figure2D.tiff", units="in", width=5, height=5, res=1000)
motor <- ggplot(data=reldata, aes(x=reorder(`Network Name`, desc(`Network Name`)), y = `Motor Relative Reliability`)) +
  geom_point(aes(fill = `Network Name`), size=3, shape=21, stroke=NA)+
  coord_flip()+
#  geom_violin()+
#  geom_jitter(color="black" , width=0.15, height=0.05, alpha=0.75, size=0.5)+
  geom_hline(yintercept = 0, color="red", linetype="dashed") +  # Add horizontal line at 0 
#  ggtitle("Relative Reliability between Motor Task and Rest" , subtitle = "No Task Regression") +
#  scale_x_discrete(guide = guide_axis(angle = 60)=) +
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
  ylim(-0.25,0.25)+
  labs(
    y = expression(~Delta * " FC-TRC"),
    x = "")+
  theme(legend.position = "none") +
  stat_summary(fun=mean, size=0.4, color="black", geom="crossbar")+
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

plot(motor)
dev.off()

#mean values for all networks
df<- data.frame(c(aggregate(`Motor Relative Reliability`~`Network Name`, reldata, FUN=mean)), 
                c(aggregate(`Language Relative Reliability`~`Network Name`, reldata, FUN=mean)),
                c(aggregate(`Memory Relative Reliability`~`Network Name`, reldata, FUN=mean)))
df <- df[,c(1,2,4,6)]
df[,5] <- c(df[,2]-df[,3])
df[,6] <- c(df[,2]-df[,4])
df[,7] <- c(df[,3]-df[,4])

#Calculate Percent change for language
change_reldata_language <- (aggregate(reldata$`Language Relative Reliability`~reldata$Network,reldata,sum))/(aggregate(reldata$`Language Relative Reliability`~reldata$Network,reldata,length))
percentchange_reldata_language <- change_reldata_language*100
percentchange_reldata_language[,1] <- unique(reldata$`Network Name`)
colnames(percentchange_reldata_language) <- c("Network", "Language_RelativeReli")

# Color order
netcolors <- data.frame(c(percentchange_reldata_language$Network), percentchange_reldata_language$Network)
colnames(netcolors) <- c('Net Names', 'Net Hex')
netcolors$`Net Hex`<- c('#EA3327','#0505A6','#DEDB54','#B69C61','#62C04B','#C49EDD','#3B8787','#3A284C','#565DA4','#8ED2AD','#CE7377','#6A4EB8','#489F65','#4192AC','#9A99E0','#83BB72','#456044')
percentchange_reldata_language[,3] <- netcolors$`Net Hex`
colnames(percentchange_reldata_language) <- c("Network", "Change", "Hex")


# Language Percent Change No Regression Bar plot
percentchange_reldata_language %>%
  ggplot(aes(x=reorder(Network, Change), y = Change, fill=Hex)) +
  geom_bar(stat="identity")+
  ggtitle("Percent Change in Relative Reliability between Language Task and Rest" , subtitle = "No Task Regression") +
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
  labs(
    x = "",
    y = "% Change")+
  theme(legend.position = "none") +  
  scale_fill_manual(values=c("#0505A6","#B69C61","#EA3327", "#DEDB54", "#62C04B","#3B8787","#C49EDD","#565DA4","#83BB72","#9A99E0","#4192AC","#6A4EB8","#489F65","#456044","#CE7377","#8ED2AD","#3A284C"))


# # Language Relative Absolute Values No Regression Box plot
# # boxplot with anova against base mean
# ggboxplot(reldata, x = "Network Name", y = "Language Relative Reliability", color="Network",
#           palette= ,add = "jitter", legend = "none") +
#   ggtitle("Relative Reliability between language task and rest" , subtitle = "No Task Regression") +
#   coord_flip() + 
#   geom_hline(yintercept = mean(reldata$`Language Relative Reliability`), linetype = 2)+ # Add horizontal line at base mean
#   stat_compare_means(label = "p.signif", method = "t.test",
#                      ref.group = ".all.", hide.ns = TRUE)      # Pairwise comparison against all
# 
# 
# #Violin - Language plus jitter plot for relative reliablity 
# reldata %>%
#   ggplot(aes(x=reorder(`Network Name`, desc(`Language Relative Reliability`)), y = `Language Relative Reliability`, 
#              color=`Network Name`, fill=reorder(`Network Name`, desc(`Language Relative Reliability`)))) +
#   geom_violin()+
#   geom_jitter(color="black" , width=0.15, height=0.05, alpha=0.75, size=0.5)+
#   geom_hline(yintercept = 0, color="red", linetype="dashed") +  # Add horizontal line at 0 
#   ggtitle("Relative Reliability between Language Task and Rest" , subtitle = "No Task Regression") +
#   scale_x_discrete(guide = guide_axis(angle = 60)) +
#   theme(panel.background = element_rect(fill='white'),
#         panel.border = element_blank(),
#         axis.line = element_line(colour = "black"),
#         plot.title = element_text(hjust = 0.5),
#         plot.subtitle = element_text(hjust = 0.5),
#         plot.caption = element_text(size = 8, 
#                                     face = "italic",
#                                     color = "#5F6375",
#                                     margin = margin(t = 15))) +
#   labs(
#     y = expression(~Delta * " FC-TRC"),
#     x = "")+
#   theme(legend.position = "none") +  
#   stat_summary(fun.y=mean, geom="point", size=1, color="red")+
#   ylim(-0.3, 0.3)+
#   scale_color_manual(values=c("black","black","black", "black","black","black","black","black","black","black","black","black","black","black","black","black","black"))+
#   scale_fill_manual(values=c("#0505A6","#62C04B","grey", "grey","grey","grey","grey","grey","grey","grey","grey","grey","grey","grey","grey","grey","grey"))


#Language scatterplot for relative reliablity 
tiff("Figure2E.tiff", units="in", width=5, height=5, res=1000)
language <- ggplot(data=reldata, aes(x=reorder(`Network Name`, desc(`Network Name`)), y = `Language Relative Reliability`)) +
  geom_point(aes(fill = `Network Name`), size=3, shape=21, stroke=NA)+
  coord_flip()+
  #  geom_violin()+
  #  geom_jitter(color="black" , width=0.15, height=0.05, alpha=0.75, size=0.5)+
  geom_hline(yintercept = 0, color="red", linetype="dashed") +  # Add horizontal line at 0 
#  ggtitle("Relative Reliability between Language Task and Rest" , subtitle = "No Task Regression") +
  #  scale_x_discrete(guide = guide_axis(angle = 60)=) +
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
  ylim(-0.25,0.25)+
  labs(
    y = expression(~Delta * " FC-TRC"),
    x = "")+
  theme(legend.position = "none") +
  stat_summary(fun.y=mean, size=0.4, color="black", geom="crossbar")+
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

plot(language)
dev.off()


#Memory Task 
#Calculate Percent change for memory
change_reldata_memory <- (aggregate(reldata$`Memory Relative Reliability`~reldata$Network,reldata,sum))/(aggregate(reldata$`Memory Relative Reliability`~reldata$Network,reldata,length))
percentchange_reldata_memory <- change_reldata_memory*100
percentchange_reldata_memory[,1] <- unique(reldata$`Network Name`)
colnames(percentchange_reldata_memory) <- c("Network", "Memory_RelativeReli")

# Color order
netcolors <- data.frame(c(percentchange_reldata_memory$Network), percentchange_reldata_memory$Network)
colnames(netcolors) <- c('Net Names', 'Net Hex')
netcolors$`Net Hex`<- c('#EA3327','#0505A6','#DEDB54','#B69C61','#62C04B','#C49EDD','#3B8787','#3A284C','#565DA4','#8ED2AD','#CE7377','#6A4EB8','#489F65','#4192AC','#9A99E0','#83BB72','#456044')
percentchange_reldata_memory[,3] <- netcolors$`Net Hex`
colnames(percentchange_reldata_memory) <- c("Network", "Change", "Hex")


# Memory Percent Change No Regression Bar plot
percentchange_reldata_memory %>%
  ggplot(aes(x=reorder(Network, Change), y = Change, fill=Hex)) +
  geom_bar(stat="identity")+
  ggtitle("Percent Change in Relative Reliability between Memory Task and Rest" , subtitle = "No Task Regression") +
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
    y = "% Change")+
  theme(legend.position = "none") +  
  scale_fill_manual(values=c("#0505A6","#B69C61","#EA3327", "#DEDB54", "#62C04B","#3B8787","#C49EDD","#565DA4","#83BB72","#9A99E0","#4192AC","#6A4EB8","#489F65","#456044","#CE7377","#8ED2AD","#3A284C"))


# # Memory Relative Absolute Values No Regression Box plot
# # boxplot with anova against base mean
# ggboxplot(reldata, x = "Network Name", y = "Memory Relative Reliability", color="Network",
#           palette= ,add = "jitter", legend = "none") +
#   ggtitle("Relative Reliability between memory task and rest" , subtitle = "No Task Regression") +
#   coord_flip() + 
#   geom_hline(yintercept = mean(reldata$`Memory Relative Reliability`), linetype = 2)+ # Add horizontal line at base mean
#   stat_compare_means(label = "p.signif", method = "t.test",
#                      ref.group = ".all.", hide.ns = TRUE)      # Pairwise comparison against all
# 
# #Violin -Memory plus jitter plot for relative reliablity 
# reldata %>%
#   ggplot(aes(x=reorder(`Network Name`, desc(`Memory Relative Reliability`)), y = `Memory Relative Reliability`, 
#              color=reorder(`Network Name`, desc(`Memory Relative Reliability`)), fill=reorder(`Network Name`, desc(`Memory Relative Reliability`)))) +
#   geom_violin()+
#   geom_jitter(color="black" , width=0.15, height=0.05, alpha=0.75, size=0.5)+
#   geom_hline(yintercept = 0, color="red", linetype="dashed") +  # Add horizontal line at 0 
#   ggtitle("Relative Reliability between Memory Task and Rest" , subtitle = "No Task Regression") +
#   scale_x_discrete(guide = guide_axis(angle = 60)) +
#   theme(panel.background = element_rect(fill='white'),
#         panel.border = element_blank(),
#         axis.line = element_line(colour = "black"),
#         plot.title = element_text(hjust = 0.5),
#         plot.subtitle = element_text(hjust = 0.5),
#         plot.caption = element_text(size = 8, 
#                                     face = "italic",
#                                     color = "#5F6375",
#                                     margin = margin(t = 15))) +
#   labs(
#     y = expression(~Delta * " FC-TRC"),
#     x = "")+
#   theme(legend.position = "none") +  
#   stat_summary(fun.y=mean, geom="point", size=1, color="red")+
#   ylim(-0.3, 0.3)+
#   scale_color_manual(values=c("black","black","black", "black","black","black","black","black","black","black","black","black","black","black","black","black","black"))+
#   scale_fill_manual(values=c("#0505A6","#9A99E0","grey", "grey","grey","grey","grey","grey","grey","grey","grey","grey","grey","grey","grey","grey","grey"))



#Memory scatterplot for relative reliablity 
tiff("Figure2F.tiff", units="in", width=5, height=5, res=1000)
memory<-ggplot(data=reldata, aes(x=reorder(`Network Name`, desc(`Network Name`)), y = `Memory Relative Reliability`)) +
  geom_point(aes(fill=`Network Name`), size=3, shape=21, stroke=NA)+
  coord_flip()+
  #  geom_violin()+
  #  geom_jitter(color="black" , width=0.15, height=0.05, alpha=0.75, size=0.5)+
  geom_hline(yintercept = 0, color="red", linetype="dashed") +  # Add horizontal line at 0 
#  ggtitle("Relative Reliability between Memory Task and Rest" , subtitle = "No Task Regression") +
  #  scale_x_discrete(guide = guide_axis(angle = 60)=) +
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
  ylim(-0.25,0.27)+
  labs(
    y = expression(~Delta * " FC-TRC"),
    x = "")+
  theme(legend.position = "none") +
  stat_summary(fun.y=mean, size=0.4, color="black", geom="crossbar")+
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
             
plot(memory)
dev.off()
# ggarrange(motor, 
#           language + 
#             theme(axis.text.y = element_blank(),
#                   axis.ticks.y = element_blank(),
#                   axis.title.y = element_blank() ), 
#           memory + 
#             theme(axis.text.y = element_blank(),
#                   axis.ticks.y = element_blank(),
#                   axis.title.y = element_blank() ),
#           nrow = 1)
# annotate_figure(plot, top = text_grob("Relative Reliability between Task and Rest", 
#                                       face = "bold", size = 14))

#####################################################################################################################################################################################################################
#####################################################################################################################################################################################################################
#Task Regressed data

rm(list=ls())

# Load Relative data
reldata <- read_excel("/Users/shefalirai/Desktop/MSCData.xlsx", sheet='RelativeReli_Regressed')

#Calculate Percent change for motor task
change_reldata_motor <- (aggregate(reldata$`Motor Relative Reliability Reg`~reldata$Network,reldata,sum))/(aggregate(reldata$`Motor Relative Reliability Reg`~reldata$Network,reldata,length))
percentchange_reldata_motor <- change_reldata_motor*100
percentchange_reldata_motor[,1] <- unique(reldata$`Network Name`)
colnames(percentchange_reldata_motor) <- c("Network", "Motor_RelativeReli")

# Color order
netcolors <- data.frame(c(percentchange_reldata_motor$Network), percentchange_reldata_motor$Network)
colnames(netcolors) <- c('Net Names', 'Net Hex')
netcolors$`Net Hex`<- c('#EA3327','#0505A6','#DEDB54','#B69C61','#62C04B','#C49EDD','#3B8787','#3A284C','#565DA4','#8ED2AD','#CE7377','#6A4EB8','#489F65','#4192AC','#9A99E0','#83BB72','#456044')
percentchange_reldata_motor[,3] <- netcolors$`Net Hex`
colnames(percentchange_reldata_motor) <- c("Network", "Change", "Hex")

#Motor Regressed relative reliability 
tiff("SuppFigure4D.tiff", units="in", width=5, height=5, res=1000)
motorreg <- ggplot(data=reldata, aes(x=reorder(`Network Name`, desc(`Network Name`)), y = `Motor Relative Reliability Reg`)) +
  geom_point(aes(fill=`Network Name`), size=3, shape=21, stroke=NA)+
  coord_flip()+
  #  geom_violin()+
  #  geom_jitter(color="black" , width=0.15, height=0.05, alpha=0.75, size=0.5)+
  geom_hline(yintercept = 0, color="red", linetype="dashed") +  # Add horizontal line at 0 
  #  ggtitle("Relative Reliability between Motor Task and Rest" , subtitle = "Task Regressed") +
  #  scale_x_discrete(guide = guide_axis(angle = 60)=) +
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
  ylim(-0.4,0.2)+
  labs(
    y = expression(~Delta * " FC-TRC"),
    x = "")+
  theme(legend.position = "none") +
  stat_summary(fun=mean, size=0.4, color="black", geom="crossbar")+
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
             
plot(motorreg)
dev.off()


#Language Regressed relative reliability 
tiff("SuppFigure4E.tiff", units="in", width=5, height=5, res=1000)
Languagereg <- ggplot(data=reldata, aes(x=reorder(`Network Name`, desc(`Network Name`)), y = `Language Relative Reliability Reg`)) +
  geom_point(aes(fill=`Network Name`), 
             size=3, stroke=NA, shape=21)+
  coord_flip()+
  #  geom_violin()+
  #  geom_jitter(color="black" , width=0.15, height=0.05, alpha=0.75, size=0.5)+
  geom_hline(yintercept = 0, color="red", linetype="dashed") +  # Add horizontal line at 0 
  #  ggtitle("Relative Reliability between Language Task and Rest" , subtitle = "Task Regressed") +
  #  scale_x_discrete(guide = guide_axis(angle = 60)=) +
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
  ylim(-0.4,0.2)+
  labs(
    y = expression(~Delta * " FC-TRC"),
    x = "")+
  theme(legend.position = "none") +
  stat_summary(fun=mean, size=0.4, color="black", geom="crossbar")+
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
             
plot(Languagereg)
dev.off()


#Memory Regressed relative reliability 
tiff("SuppFigure4F.tiff", units="in", width=5, height=5, res=1000)
Memoryreg <- ggplot(data=reldata, aes(x=reorder(`Network Name`, desc(`Network Name`)), y = `Memory Relative Reliability Reg`)) +
  geom_point(aes(fill=`Network Name`), 
             stroke=NA,pch=21, size=3)+
  coord_flip()+
  #  geom_violin()+
  #  geom_jitter(color="black" , width=0.15, height=0.05, alpha=0.75, size=0.5)+
  geom_hline(yintercept = 0, color="red", linetype="dashed") +  # Add horizontal line at 0 
  #  ggtitle("Relative Reliability between Memory Task and Rest" , subtitle = "Task Regressed") +
  #  scale_x_discrete(guide = guide_axis(angle = 60)=) +
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
  ylim(-0.4,0.2)+
  labs(
    y = expression(~Delta * " FC-TRC"),
    x = "")+
  theme(legend.position = "none") +
  stat_summary(fun=mean, size=0.4, color="black", geom="crossbar")+
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
             
plot(Memoryreg)
dev.off()






# # Motor Percent Change Regressed Bar plot
# percentchange_reldata_motor %>%
#   ggplot(aes(x=reorder(Network, Change), y = Change, fill=Hex)) +
#   geom_bar(stat="identity")+
#   ggtitle("Percent Change in Relative Reliability between Motor Task and Rest" , subtitle = "Task Regressed") +
#   coord_flip()+
#   theme(panel.background = element_rect(fill='white'),
#         panel.border = element_blank(),
#         axis.line = element_line(colour = "black"),
#         plot.title = element_text(hjust = 0.5),
#         plot.subtitle = element_text(hjust = 0.5),
#         plot.caption = element_text(size = 8, 
#                                     face = "italic",
#                                     color = "#5F6375",
#                                     margin = margin(t = 15))) +
#   labs(
#     x = "",
#     y = "% Change")+
#   theme(legend.position = "none") +  
#   scale_fill_manual(values=c("#0505A6","#B69C61","#EA3327", "#DEDB54", "#62C04B","#3B8787","#C49EDD","#565DA4","#83BB72","#9A99E0","#4192AC","#6A4EB8","#489F65","#456044","#CE7377","#8ED2AD","#3A284C"))


# # Motor Relative Absolute Values No Regression Box plot
# # boxplot with anova against base mean
# ggboxplot(reldata, x = "Network Name", y = "Motor Relative Reliability Reg", color="Network",
#           palette= ,add = "jitter", legend = "none") +
#   ggtitle("Relative Reliability between motor task and rest" , subtitle = "Task Regressed") +
#   coord_flip() + 
#   geom_hline(yintercept = mean(reldata$`Motor Relative Reliability Reg`), linetype = 2)+ # Add horizontal line at base mean
#   stat_compare_means(label = "p.signif", method = "t.test",
#                      ref.group = ".all.", hide.ns = TRUE)      # Pairwise comparison against all
# 

# #Violin plus jitter plot for relative reliablity 
# reldata %>%
#   ggplot(aes(x=reorder(`Network Name`, desc(`Motor Relative Reliability Reg`)), y = `Motor Relative Reliability Reg`)) +
#   geom_violin(trim=FALSE)+
#   geom_jitter(width=0.15, height=0.05, alpha=0.5, size=0.75)+
#   geom_hline(yintercept = 0, color="red", linetype="dashed") +  # Add horizontal line at 0 
#   ggtitle("Relative Reliability between Motor Task and Rest" , subtitle = "Task Regressed") +
#   scale_x_discrete(guide = guide_axis(angle = 60)) +
#   theme(panel.background = element_rect(fill='white'),
#         panel.border = element_blank(),
#         axis.line = element_line(colour = "black"),
#         plot.title = element_text(hjust = 0.5),
#         plot.subtitle = element_text(hjust = 0.5),
#         plot.caption = element_text(size = 8, 
#                                     face = "italic",
#                                     color = "#5F6375",
#                                     margin = margin(t = 15))) +
#   labs(
#     y = expression(~Delta * " FC-TRC"),
#     x = "")+
#   theme(legend.position = "none") +  
#   scale_fill_manual(values=c("#456044","#8ED2AD","#CE7377", "#3A284C","grey","grey","grey","grey","grey","grey","grey","grey","grey","grey","grey","grey","grey"))
# 
# 
# 
# #Language Task 
# #Calculate Percent change for language
# change_reldata_language <- (aggregate(reldata$`Language Relative Reliability Reg`~reldata$Network,reldata,sum))/(aggregate(reldata$`Language Relative Reliability Reg`~reldata$Network,reldata,length))
# percentchange_reldata_language <- change_reldata_language*100
# percentchange_reldata_language[,1] <- unique(reldata$`Network Name`)
# colnames(percentchange_reldata_language) <- c("Network", "Language_RelativeReli")
# 
# # Color order
# netcolors <- data.frame(c(percentchange_reldata_language$Network), percentchange_reldata_language$Network)
# colnames(netcolors) <- c('Net Names', 'Net Hex')
# netcolors$`Net Hex`<- c('#EA3327','#0505A6','#DEDB54','#B69C61','#62C04B','#C49EDD','#3B8787','#3A284C','#565DA4','#8ED2AD','#CE7377','#6A4EB8','#489F65','#4192AC','#9A99E0','#83BB72','#456044')
# percentchange_reldata_language[,3] <- netcolors$`Net Hex`
# colnames(percentchange_reldata_language) <- c("Network", "Change", "Hex")
# 
# 
# # Language Percent Change Regressed Bar plot
# percentchange_reldata_language %>%
#   ggplot(aes(x=reorder(Network, Change), y = Change, fill=Hex)) +
#   geom_bar(stat="identity")+
#   ggtitle("Percent Change in Relative Reliability between Language Task and Rest" , subtitle = "Task Regressed") +
#   coord_flip()+
#   theme(panel.background = element_rect(fill='white'),
#         panel.border = element_blank(),
#         axis.line = element_line(colour = "black"),
#         plot.title = element_text(hjust = 0.5),
#         plot.subtitle = element_text(hjust = 0.5),
#         plot.caption = element_text(size = 8, 
#                                     face = "italic",
#                                     color = "#5F6375",
#                                     margin = margin(t = 15))) +
#   labs(
#     x = "",
#     y = "% Change")+
#   theme(legend.position = "none") +  
#   scale_fill_manual(values=c("#0505A6","#B69C61","#EA3327", "#DEDB54", "#62C04B","#3B8787","#C49EDD","#565DA4","#83BB72","#9A99E0","#4192AC","#6A4EB8","#489F65","#456044","#CE7377","#8ED2AD","#3A284C"))
# 
# 
# # # Language Relative Absolute Values No Regression Box plot
# # # boxplot with anova against base mean
# # ggboxplot(reldata, x = "Network Name", y = "Language Relative Reliability Reg", color="Network",
# #           palette= ,add = "jitter", legend = "none") +
# #   ggtitle("Relative Reliability between language task and rest" , subtitle = "Task Regressed") +
# #   coord_flip() + 
# #   geom_hline(yintercept = mean(reldata$`Language Relative Reliability Reg`), linetype = 2)+ # Add horizontal line at base mean
# #   stat_compare_means(label = "p.signif", method = "t.test",
# #                      ref.group = ".all.", hide.ns = TRUE)      # Pairwise comparison against all
# # 
# #Violin plus jitter plot for relative reliablity 
# reldata %>%
#   ggplot(aes(x=reorder(`Network Name`, desc(`Language Relative Reliability Reg`)), y = `Language Relative Reliability Reg`)) +
#   geom_violin(trim=FALSE)+
#   geom_jitter(width=0.15, height=0.05, alpha=0.5, size=0.75)+
#   geom_hline(yintercept = 0, color="red", linetype="dashed") +  # Add horizontal line at 0 
#   ggtitle("Relative Reliability between Language Task and Rest" , subtitle = "Task Regressed") +
#   scale_x_discrete(guide = guide_axis(angle = 60)) +
#   theme(panel.background = element_rect(fill='white'),
#         panel.border = element_blank(),
#         axis.line = element_line(colour = "black"),
#         plot.title = element_text(hjust = 0.5),
#         plot.subtitle = element_text(hjust = 0.5),
#         plot.caption = element_text(size = 8, 
#                                     face = "italic",
#                                     color = "#5F6375",
#                                     margin = margin(t = 15))) +
#   labs(
#     y = expression(~Delta * " FC-TRC"),
#     x = "")+
#   theme(legend.position = "none") +  
#   scale_fill_manual(values=c("#456044","#8ED2AD","#CE7377", "#3A284C","grey","grey","grey","grey","grey","grey","grey","grey","grey","grey","grey","grey","grey"))
# 
# 
# 
# 
# #Memory Task 
# #Calculate Percent change for memory
# change_reldata_memory <- (aggregate(reldata$`Memory Relative Reliability Reg`~reldata$Network,reldata,sum))/(aggregate(reldata$`Memory Relative Reliability Reg`~reldata$Network,reldata,length))
# percentchange_reldata_memory <- change_reldata_memory*100
# percentchange_reldata_memory[,1] <- unique(reldata$`Network Name`)
# colnames(percentchange_reldata_memory) <- c("Network", "Memory_RelativeReli")
# 
# # Color order
# netcolors <- data.frame(c(percentchange_reldata_memory$Network), percentchange_reldata_memory$Network)
# colnames(netcolors) <- c('Net Names', 'Net Hex')
# netcolors$`Net Hex`<- c('#EA3327','#0505A6','#DEDB54','#B69C61','#62C04B','#C49EDD','#3B8787','#3A284C','#565DA4','#8ED2AD','#CE7377','#6A4EB8','#489F65','#4192AC','#9A99E0','#83BB72','#456044')
# percentchange_reldata_memory[,3] <- netcolors$`Net Hex`
# colnames(percentchange_reldata_memory) <- c("Network", "Change", "Hex")
# 
# 
# # Memory Percent Change Regressed Bar plot
# percentchange_reldata_memory %>%
#   ggplot(aes(x=reorder(Network, Change), y = Change, fill=Hex)) +
#   geom_bar(stat="identity")+
#   ggtitle("Percent Change in Relative Reliability between Memory Task and Rest" , subtitle = "Task Regressed") +
#   coord_flip()+
#   theme(panel.background = element_rect(fill='white'),
#         panel.border = element_blank(),
#         axis.line = element_line(colour = "black"),
#         plot.title = element_text(hjust = 0.5),
#         plot.subtitle = element_text(hjust = 0.5),
#         plot.caption = element_text(size = 8, 
#                                     face = "italic",
#                                     color = "#5F6375",
#                                     margin = margin(t = 15))) +
#   labs(
#     x = "",
#     y = "% Change")+
#   theme(legend.position = "none") +  
#   scale_fill_manual(values=c("#0505A6","#B69C61","#EA3327", "#DEDB54", "#62C04B","#3B8787","#C49EDD","#565DA4","#83BB72","#9A99E0","#4192AC","#6A4EB8","#489F65","#456044","#CE7377","#8ED2AD","#3A284C"))
# 
# 
# # # Memory Relative Absolute Values No Regression Box plot
# # # boxplot with anova against base mean
# # ggboxplot(reldata, x = "Network Name", y = "Memory Relative Reliability Reg", color="Network",
# #           palette= ,add = "jitter", legend = "none") +
# #   ggtitle("Relative Reliability between memory task and rest" , subtitle = "Task Regressed") +
# #   coord_flip() + 
# #   geom_hline(yintercept = mean(reldata$`Memory Relative Reliability Reg`), linetype = 2)+ # Add horizontal line at base mean
# #   stat_compare_means(label = "p.signif", method = "t.test",
# #                      ref.group = ".all.", hide.ns = TRUE)      # Pairwise comparison against all
# # 
# #Violin plus jitter plot for relative reliablity 
# reldata %>%
#   ggplot(aes(x=reorder(`Network Name`, desc(`Memory Relative Reliability Reg`)), y = `Memory Relative Reliability Reg`)) +
#   geom_violin(trim=FALSE)+
#   geom_jitter(width=0.15, height=0.05, alpha=0.5, size=0.75)+
#   geom_hline(yintercept = 0, color="red", linetype="dashed") +  # Add horizontal line at 0 
#   ggtitle("Relative Reliability between Memory Task and Rest" , subtitle = "Task Regressed") +
#   scale_x_discrete(guide = guide_axis(angle = 60)) +
#   theme(panel.background = element_rect(fill='white'),
#         panel.border = element_blank(),
#         axis.line = element_line(colour = "black"),
#         plot.title = element_text(hjust = 0.5),
#         plot.subtitle = element_text(hjust = 0.5),
#         plot.caption = element_text(size = 8, 
#                                     face = "italic",
#                                     color = "#5F6375",
#                                     margin = margin(t = 15))) +
#   labs(
#     y = expression(~Delta * " FC-TRC"),
#     x = "")+
#   theme(legend.position = "none") +  
#   scale_fill_manual(values=c("#456044","#8ED2AD","#CE7377", "#3A284C","grey","grey","grey","grey","grey","grey","grey","grey","grey","grey","grey","grey","grey"))
# 
# 
# 
