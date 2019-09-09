from methods import *

# Number of iterations (the number of matrices to be generated)
# all tasks for each matrix
n = 1

cond_num = [0]*n
inverse_time = [0]*n
gauss_norm = [0]*n
gauss_time = [0]*n
lup_build_time = [0]*n
lup_norm = [0]*n
lup_solve_time = [0]*n
cholesky_norm = [0]*n
cholesky_time = [0]*n
relaxation_norm = [0]*n
relaxation_time = [0]*n
qr_time = [0]*n
qr_norm = [0]*n
least_squares_norm = [0]*n
least_squares_time = [0]*n
gmres_time = [0]*n
gmres_norm = [0]*n 
gmres_arnoldi_time = [0]*n
gmres_arnoldi_norm = [0]*n 


for i in range(n):
    print("Itaration number:",i+1)
    m = generate_matrix(256,8)
    y = generate_vector(256,8)
    b = multiplication(m,y)
    
    cond_num[i] = condition_number(m)
    t1_inv = time.time()
    inv(m)
    inverse_time[i] = time.time()-t1_inv
    
    t2_gauss = time.time()
    x = gauss_max_element(m,b)
    gauss_time[i] = time.time()-t2_gauss
    gauss_norm[i] = max_norm(substract_vectors(y,x))
    
    t3_lup = time.time()
    lu = lup_build(m,b)
    lup_build_time[i] = time.time()-t3_lup
    t4_lup = time.time()
    x = lup_solve(lu)
    lup_solve_time[i] = time.time()-t4_lup
    lup_norm[i] = max_norm(substract_vectors(y,x))

    t5_cholesky = time.time()
    x = cholesky_decomposition(m,b)
    cholesky_time[i] = time.time() - t5_cholesky
    cholesky_norm[i] = max_norm(substract_vectors(y,x))

    t6_relaxation = time.time()
    x = relaxation(m,b)
    relaxation_time[i] = time.time() - t6_relaxation
    relaxation_norm[i] = max_norm(substract_vectors(y,x))

    t7_qr = time.time()
    x = qr_decomposition(m,b)
    qr_time[i] = time.time() - t7_qr
    qr_norm[i] = max_norm(substract_vectors(y,x))

    t8_least_squares = time.time()
    x = least_sq_tuple(m,b,8)
    least_squares_time[i] = time.time() - t8_least_squares
    least_squares_norm[i] = least_sq_custom(x)
    
    t9_gmres = time.time()
    x = gmres(m,b)
    gmres_time[i] = time.time() - t9_gmres
    gmres_norm[i] = max_norm(substract_vectors(y,x))

    t10_arnoldi = time.time()
    x = gmres_arnoldi_modified(m,b)
    gmres_arnoldi_time[i] = time.time() - t10_arnoldi
    gmres_arnoldi_norm[i] = max_norm(substract_vectors(y,x))

with open("test.txt" , "w") as fout:

    fout.write("\tTASK 1 (condition number and inverse matrix)\n")
    fout.write("min condition number: "+str(min(cond_num))+"\n")
    fout.write("max condition number: "+str(max(cond_num))+"\n")
    fout.write("average condition number: "+str(sum(cond_num)/n)+"\n")
    fout.write("average time to find inverse matrix: "+str(sum(inverse_time)/n)+"\n")

    fout.write("\n\n\tTASK 2 (Gauss)\n")
    fout.write("min Gauss max-norm: "+str(min(gauss_norm))+"\n")
    fout.write("max Gauss max-norm: "+str(max(gauss_norm))+"\n")
    fout.write("average Gauss max-norm: "+str(sum(gauss_norm)/n)+"\n")
    fout.write("average time to solve by Gauss: "+str(sum(gauss_time)/n)+"\n")

    fout.write("\n\n\tTASK 3 (LUP)\n")
    fout.write("min LUP max-norm: "+str(min(lup_norm))+"\n")
    fout.write("max LUP max-norm: "+str(max(lup_norm))+"\n")
    fout.write("average LUP max-norm: "+str(sum(lup_norm)/n)+"\n")
    fout.write("average time to build LUP: "+str(sum(lup_build_time)/n)+"\n")
    fout.write("average time to solve by LUP: "+str(sum(lup_solve_time)/n)+"\n")

    fout.write("\n\n\tTASK 4 (Cholesky)\n")
    fout.write("min Cholesky max-norm: "+str(min(cholesky_norm))+"\n")
    fout.write("max Cholesky max-norm: "+str(max(cholesky_norm))+"\n")
    fout.write("average Cholesky max-norm: "+str(sum(cholesky_norm)/n)+"\n")
    fout.write("average time to solve by Cholesky: "+str(sum(cholesky_time)/n)+"\n")

    fout.write("\n\n\tTASK 5 (Relaxation)\n")
    fout.write("min relaxation max-norm: "+str(min(relaxation_norm))+"\n")
    fout.write("max relaxation max-norm: "+str(max(relaxation_norm))+"\n")
    fout.write("average relaxation max-norm: "+str(sum(relaxation_norm)/n)+"\n")
    fout.write("average time to solve by relaxation: "+str(sum(relaxation_time)/n)+"\n")

    fout.write("\n\n\tTASK 6 (QR)\n")
    fout.write("min QR max-norm: "+str(min(qr_norm))+"\n")
    fout.write("max QR max-norm: "+str(max(qr_norm))+"\n")
    fout.write("average QR max-norm: "+str(sum(qr_norm)/n)+"\n")
    fout.write("average time to solve by QR: "+str(sum(qr_time)/n)+"\n")

    fout.write("\n\n\tTASK 7 (Least squares)\n")
    fout.write("min least squares euclidean-norm: "+str(min(least_squares_norm))+"\n")
    fout.write("max least squares euclidean-norm: "+str(max(least_squares_norm))+"\n")
    fout.write("average least squares euclidean-norm: "+str(sum(least_squares_norm)/n)+"\n")
    fout.write("average time to solve by least squares: "+str(sum(least_squares_time)/n)+"\n")

    fout.write("\n\n\tTASK 8 (GMRES)\n")
    fout.write("min GMRES max-norm: "+str(min(gmres_norm))+"\n")
    fout.write("max GMRES max-norm: "+str(max(gmres_norm))+"\n")
    fout.write("average GMRES max-norm: "+str(sum(gmres_norm)/n)+"\n")
    fout.write("average time to solve by GMRES: "+str(sum(gmres_time)/n)+"\n")

    fout.write("\n\n\tTASK 9 (GMRES Arnoldi)\n")
    fout.write("min GMRES Arnoldi max-norm: "+str(min(gmres_arnoldi_norm))+"\n")
    fout.write("max GMRES Arnoldi max-norm: "+str(max(gmres_arnoldi_norm))+"\n")
    fout.write("average GMRES Arnoldi max-norm: "+str(sum(gmres_arnoldi_norm)/n)+"\n")
    fout.write("average time to solve by GMRES Arnoldi: "+str(sum(gmres_arnoldi_time)/n)+"\n")

