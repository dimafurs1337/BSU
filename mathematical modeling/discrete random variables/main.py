from methods import *

n,l = 1000, 2
m,p = 5, 0.6

print("Poisson sequence with l=",l, sep="")
seqPoisson = generatePoissonSeq(n,l)
print("Sample Mean     : {:.3}, Genuine Mean     : {:d}".format(SampleMean(seqPoisson,n),l))
print("Sample Variance : {:.3}, Genuine Variance : {:d}".format(SampleVariance(seqPoisson,n),l))
print("Xi2 : {:.3}\n".format(PoissonXi2(seqPoisson,n,l)))

print("Binomial sequence with m={:d}, p={:.1}".format(m,p))
seqBinomial = generateBinomialSeq(n,m,p)
print("Sample Mean     : {:.3}, Genuine Mean     : {:.3}".format(SampleMean(seqBinomial,n),BinomialMean(m,p)))
print("Sample Variance : {:.3}, Genuine Variance : {:.3}".format(SampleVariance(seqBinomial,n),BinomialVariance(m,p)))
print("Xi2 : {:.3}".format(BinomialXi2(seqBinomial,n,m,p)))








