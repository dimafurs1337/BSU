#include <algorithm>
#include <time.h>
using std::sort;

double *sequenceMCG(int n, int a0, int b, unsigned int m){
	double *seq = (double*)calloc(n, sizeof(double));
	unsigned int temp = a0;
	seq[0]= (double)(temp) / m;
	
	for(int i = 0; i < n; i++) {
		temp = (b * temp) % m;
		seq[i] = (double)(temp) / m;
	}
	return seq;
}

double KolmogorovFunc(int n, double *mass){
	sort(mass, mass + n);
	double D = 0;

	for (int i = 0; i < n; i++){
		if (D < fabs((double)(i + 1) / n - mass[i]))
			D = fabs((double)(i + 1) / n - mass[i]);
	}
	return sqrt(n)*D;
}

double PirsonFunc(int n, double* seq) {
	int *freq = (int*)calloc(10, sizeof(int));
	int c = 0;
	double sum = 0;

	for (int i = 0; i < n; i++){
		c = (int)(seq[i] * 10);		
		freq[c]++;
	}

	for (int i = 0; i < 10; i++)
		sum += pow((freq[i] - n * (0.1)),2) / (n * (0.1));
	
	free(freq);
	return sum;
}

int main(){

	srand(time(NULL));
	int a0 = 16807, b = 16807, K = 64;
	unsigned int M = 2147483648;
	int n = 1000;
	int c = 0;

	double *result1 = sequenceMCG(n, a0, b, M);
	double *result2 = (double*)calloc(n, sizeof(double));
	double *result3 = (double*)calloc(n, sizeof(double));
	double *temp = (double*)calloc(K, sizeof(double));

	for (int i = 0; i < n; i++)
		result2[i] = ((double)rand() / RAND_MAX);
	
	memcpy(temp, result1, K*sizeof(double));

	for (int i = 0; i < n; i++) {
		c = (int)(result2[i] * K);
		result3[i] = temp[c];
		temp[c] = result1[(i + K) % n];
	}
	
	printf("MCG                : Kolmogorov : %f\t Xi2 : %.2f\n", KolmogorovFunc(n, result1), PirsonFunc(n, result1));
	printf("MacLaren-Marsaglia : Kolmogorov : %f\t Xi2 : %.2f\n", KolmogorovFunc(n, result3), PirsonFunc(n, result3));

	system("pause");
	free(result1);
	free(result2);
	free(result3);
	free(temp);
}