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
library(DT)

tab <- matrix(c('MSC01',724, 4.08, 17730, "" , 'MSC02', 189, 1.15, 16374, "Motor Run 2: ses-func09; Glasslexical Run 1: ses-func04; Glasslexical Run 2: ses-func03, ses-func04; Memory Faces: ses-func04; Memory words: ses-func04, ses-func09; Memory scenes: ses-func04", 
                'MSC03', 1396, 7.87, 17730, "", 'MSC04', 127, 0.72, 17730, "", 'MSC05', 222, 1.25, 17730, "", 'MSC06', 238, 1.34, 17729, "Rest: ses-func08 contains only 817 volumes", 
                'MSC07', 296, 1.67, 17730, "", 'MSC08', 2471, 13.94, 17730, "", 'MSC09', 814, 4.59, 17730, "", 'MSC10', 1499, 8.51, 17609, "Memory scenes: ses-func06"), ncol=5, byrow=TRUE)
colnames(tab) <- c('Participant', 'Total Number of High Motion Volumes for All Tasks (Measure=FD)','Total Percent of High Motion Volumes','Total Number of Volumes for All Tasks', 'Missing Data')

#change order to put Column 3 after Column 1
tab <- tab[,c(1,3,2,4)]

tasktab <- matrix(c(419, 75, 170, 60, 64, 34, 56, 35, 598, 184, 
                    322, 292, 27, 23, 44, 33, 82, 41, 72, 27,
                    36, 37, 138, 27, 134, 97, 32, 33,
                    1809, 139, 350, 173, 398, 204, 96, 116,
                    934, 81, 265, 219), ncol=4, byrow=TRUE)
colnames(tasktab) <- c('High Motion Volumes: Resting State', 'High Motion Volumes: Motor Task','High Motion Volumes: Glasslexical Task','High Motion Volumes: Memory Tasks')


SuppTable1 <- cbind(tab,tasktab)
SuppTable1 <- SuppTable1[,c(1,2,3,5,6,7,4)]



