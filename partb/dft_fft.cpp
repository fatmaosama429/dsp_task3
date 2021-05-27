#define _USE_MATH_DEFINES
#include <math.h>
#include <complex>
#include <vector>
#include <iostream>
#include <iomanip>
using namespace std;
#define FFT_h
extern "C"
{
void fft(complex<double> *x, const int N) {
	// Check if it is splitted enough
	if (N <= 1) {
		return;
	}

	// Split even and odd
	// const int k= N/2;
	    complex<double> odd[N/2];
	    complex<double> even[N/2];
	for (int i = 0; i < N / 2; i++) {
		even[i] = x[i*2];
		odd[i] = x[i*2+1];
	}

	// Split on tasks
	fft(even, N/2);
	fft(odd, N/2);


	// Calculate FFT
	for (int k = 0; k < N / 2; k++) {
		complex<double> t = exp(complex<double>(0, -2 * M_PI * k / N)) *odd[k];
        x[k] = even[k] + t;
		x[N / 2 + k] = even[k] - t;
	}
}


//dft function
  void dft ( complex<double>sig_data[],complex<double>output[], int N)
{
    //allocate memory for internals
     complex<double> intSum;

    for ( int k=0; k<N; k++)
    {
        intSum=  complex<double>(0,0);
        for ( int n=0; n<N; n++)
        {
            double real = cos (((2*M_PI)/N) *k * n);
            double imaginary = sin (((2*M_PI)/N) *k * n);
             complex<double> complex_fn  (real, -imaginary);
            intSum += sig_data[n] *complex_fn;
        }
        output[k]= intSum;
    }
    
}
}

int main()
{
int N= 8;
 complex<double> signal []= {1, 1, 1, 1, 0, 0, 0, 0};
 complex<double> output[8];
 dft(signal, output, N);
 fft(signal, N);
    
    for (int i = 0; i < N; i++)
        {
            cout << i<<"//" <<"FT= " << output[i] <<'\n' ;
            cout <<'\n' ;
            
          cout << i << "))" << "fft=" << output[i] << '\n';
		   cout<< '\n';
        }
return 0;

}




