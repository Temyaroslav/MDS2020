#include <iostream>
const int MAX_DIVISORS_NUMBER = 10000;

int main(){
  int x;
  std::cin >> x;

  int Divisor[MAX_DIVISORS_NUMBER];
  int Divisor_top = 0;

  for (int d = 2; d <= x; d++){
    while (x % d == 0){
      Divisor[Divisor_top] = d;
      x /= d;
      Divisor_top++;
    }
  }

  for(int i = 0; i < Divisor_top; i++)
  {
    std::cout << Divisor[i] << std::endl;
  }

  return 0;
}
