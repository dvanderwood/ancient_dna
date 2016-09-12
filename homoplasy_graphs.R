###*****************************
# INITIAL COMMANDS TO RESET THE SYSTEM

rm(list = ls())
if (is.integer(dev.list())){dev.off()}
cat("\014")

#Set working directory
setwd('/Users/dvanderwood/Dropbox/Texas/ochman_lab/homoplasy/')
###*****************************


###*****************************
# INSTALL LIBRARIES
library('dplyr')
library('plyr')
library('tidyr')
library('ggplot2')
###*****************************

###*****************************
# INITIAL INPUTS

#Name of the input file
input_file = 'all_homoplasy_stats.txt'

# 'all_homoplasy_stats.txt'
# 'all_homoplasy_stats_pre_dyno_filter.txt'

###*****************************

###*****************************
#INITIAL DATA SETUP

#Upload homoplasy stats doc
data = read.table(input_file, sep = '\t', header = TRUE)
data_raw = data

#Remove the chr from the data in the chromosome column
data[,1] <- lapply(data[1], substring, 4)

#Split sample group into two columns, Ancient_Genome and Human_Composition
data$Ancient_Genome <- sapply(strsplit(as.character(data$Sample_Group), '_'), '[[', 1) 
data$Human_Composition <- sapply(strsplit(as.character(data$Sample_Group), '_'), '[[', 2)
data$Sample_Group = NULL
data <- data[c("Chromosome","Ancient_Genome","Human_Composition","Ancient_R_Sites","Ancient_Polymorhpisms","Informative_Sites","Total_Sites")] 
#data[,1] <- lapply(data[1],as.numeric) #Won't work when the x chromosome is added in
###*****************************


###*****************************
#DATA ANALYSIS

#Determine precentage of sites that underwent recombination that the ancient DNA was part of
#data$R_to_Info <- data$Ancient_R_Sites/data$Informative_Sites * 100
data$R_to_Total <- data$Ancient_R_Sites/data$Total_Sites * 100

#Determine precentage of ancient homoplasy sites from total number of ancient polymorphisms
#data$R_to_Info_normal <- data$Ancient_R_Sites/data$Informative_Sites * 100
data$R_to_Polymorphs <- data$Ancient_R_Sites/data$Ancient_Polymorhpisms *100

#Determine percentage of sites of the used exomes which contain ancient polymorphisms
data$Percent_Variants <- data$Ancient_Polymorhpisms/data$Total_Sites * 100



###*****************************


###*****************************
#GRAPHS

#Graph showing the precentage of Informative Sites which have ancient recombination
#data %>% group_by(Chromosome) %>% ggplot(aes(x = Chromosome, y = R_to_Info, 
#                                             color = Ancient_Genome, shape = Human_Composition,
#                                             size = Ancient_R_Sites)) + geom_point() ->chromosome_graph_info
#chromosome_graph_info

#Graph showing the precentage of Total sites which have ancient recombination
data %>% group_by(Chromosome) %>% ggplot(aes(x = Chromosome, y = R_to_Total, 
                                             color = Ancient_Genome, shape = Human_Composition,
                                             size = Ancient_R_Sites)) + geom_point() ->chromosome_graph_total
chromosome_graph_total


#Graph showing the precentage of Informative Sites which have ancient recombination, normalized by ancient polymorphisms
#data %>% group_by(Chromosome) %>% ggplot(aes(x = Chromosome, y = R_to_Info_normal, 
#                                             color = Ancient_Genome, shape = Human_Composition,
#                                             size = Ancient_R_Sites)) + geom_point() ->chromosome_graph_info_normal
#chromosome_graph_info_normal

#Graph showing the precentage of ancient homoplasy sites from total number of ancient polymorphisms, grouped by chromosomes
data %>% group_by(Chromosome) %>% ggplot(aes(x = Chromosome, y = R_to_Polymorphs, 
                                             color = Ancient_Genome, shape = Human_Composition,
                                             size = Ancient_R_Sites)) + geom_point() ->ancient_graph_poly
ancient_graph_poly

#Graph showing the precentage of ancient homoplasy sites from total number of ancient polymorphisms, grouped by ancient genome
data %>% group_by(Ancient_Genome) %>% ggplot(aes(x = Ancient_Genome, y = R_to_Polymorphs, 
                                             color = Chromosome, shape = Human_Composition,
                                             size = Ancient_R_Sites)) + geom_point() ->chromosome_graph_poly
chromosome_graph_poly

#Graph showing the precentage of ancient homoplasy sites from total number of ancient polymorphisms, grouped by ancient genome
data %>% group_by(Human_Composition) %>% ggplot(aes(x = Human_Composition, y = R_to_Polymorphs, 
                                                 color = Chromosome, shape = Ancient_Genome,
                                                 size = Ancient_R_Sites)) + geom_point() ->human_graph_poly
human_graph_poly


#Graph showing the percentage of sites of the used exomes which contain ancient polymorphisms
data %>% group_by(Chromosome) %>% ggplot(aes(x = Chromosome, y = Percent_Variants, 
                                             color = Ancient_Genome, shape = Human_Composition,
                                             size = Ancient_R_Sites)) + geom_point() ->chromosome_graph_percent_variants
chromosome_graph_percent_variants

###*****************************