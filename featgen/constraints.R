library(igraph)
g<-read.graph("../data/uniq_gsm_sms_one_account_igraph.csv",format="ncol",directed=TRUE)		
estimates=constraint(g)
write.csv( data.frame(vertex=names(estimates), value=estimates), "constraints.csv", row.names=FALSE)
