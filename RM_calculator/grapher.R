path <- commandArgs(trailingOnly = TRUE)
graph <- '/graph.txt'
graph_out <- '/graph.pdf'

graph_path_text <- paste(path,graph,sep='')
graph_path_pdf <- paste(path,graph_out,sep='')

tab=read.table(graph_path_text,h=T)

w=c(tab$Nb,rev(tab$Nb))
v=c(tab$CI05,rev(tab$CI95))
v=c(tab$Median-tab$SD,rev(tab$Median + tab$SD))
v2=c(tab$aMedian-tab$aSD,rev(tab$aMedian + tab$aSD))

pdf(graph_path_pdf)
par(mfrow=c(2,2))
plot(100,100,xlim=c(3,max(w)),ylim=c(0,max(v) + 0.1),xlab=c("# Genomes"),ylab=c("r/m"))
polygon(w,v,col="gray88",border=NA)
points(tab$Nb,tab$Median,pch=16,cex=0.6,t="b")
#points(tab$Nb,tab$aMedian,pch=16,cex=0.6,t="b",col="red")



dev.off()
