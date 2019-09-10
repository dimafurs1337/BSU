from methods import *

m = [[1.2,0.5,0.3],[-0.4,1.2,0.1],[0.3,-0.1,1.2]]
b = [4,1,-1]

realValue = np.linalg.solve([[1.2,0.5,0.3],[-0.4,1.2,0.1],[0.3,-0.1,1.2]],[4,1,-1])
draw(test(m,b,realValue))