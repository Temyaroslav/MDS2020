#include <iostream>

int main(){
  int a, b, t;
  std::cin >> a >> b;

  while (b != 0){
    t = b;
    b = a % b;
    a = t;
  }

  std::cout << a << '\n';

  return 0;
}
