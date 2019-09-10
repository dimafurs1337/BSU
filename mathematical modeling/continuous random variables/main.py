from methods import *

print("Normal distribution N(m,s); m=5, s**2 = 9")
normalSeq = generateNormSeq(1000,5,3)
print("Sample Mean     : {:.3}, Genuine Mean     : {:d}".format(SampleMean(normalSeq),5))
print("Sample Variance : {:.3}, Genuine Variance : {:d}".format(SampleVariance(normalSeq),9))
print("Xi2 : {:.3}".format(Pirson(normalSeq,10,NormFunc,5,3)))
print("Kolmogorov : {:.3}\n".format(Kolmogorov(normalSeq,NormFunc,5,3)))

print("Cauchy distribution C(a,b); a=-1, b=3")
cauchySeq = generateCauchySeq(1000,-1,3)
print("Xi2 : {:.5}".format(Pirson(cauchySeq,10,CauchyFunc,-1,3)))
print("Kolmogorov : {:.3}\n".format(Kolmogorov(cauchySeq,CauchyFunc,-1,3)))

print("Laplace distribution L(a,b); a=2, b=5")
laplaceSeq = generateLaplaceSeq(1000,2,5)
print("Sample Mean     : {:.3}, Genuine Mean     : {:d}".format(SampleMean(laplaceSeq),2))
print("Sample Variance : {:.3}, Genuine Variance : {:.2}".format(SampleVariance(laplaceSeq),0.08))
print("Xi2 : {:.5}".format(Pirson(laplaceSeq,10,LaplaceFunc,2,5)))
print("Kolmogorov : {:.3}\n".format(Kolmogorov(laplaceSeq,LaplaceFunc,2,5)))