from methods import *

m = generate_matrix(10,8)
pair = find_different_eigs(m)
print("power iteration square norm l1: ",square_norm(substract_vectors(multiplication(m,pair[0][1]),scalar_vector_multiplication(pair[0][0],pair[0][1]))))
print("power iteration square norm l2: ",square_norm(substract_vectors(multiplication(m,pair[1][1]),scalar_vector_multiplication(pair[1][0],pair[1][1]))))

all_eigs = find_all_eigvals(m)
print("all eigvals by QR-algorithm: ",all_eigs)

sec = bisection(func,scales,10e-5)
print("bisection: ",sec)
newton_v1 = discrete_newton(func,sec)
print("discrete newton: ",newton_v1)
newton_v2 = improved_newton(roots=newton_v1)
print("improved newton: ",newton_v2)