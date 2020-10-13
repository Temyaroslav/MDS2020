#include <iostream>

int main() {
  int n;
  std::cin >> n;

  bool flag = false;
  int n0 = 2;
  while (n0 <= n){
    if (n0 == n){
      flag = true;
      break;
    }
    n0 *= 2;
  }

  if (flag){
    std::cout << "YES" << '\n';
  }
  else{
    std::cout << "NO" << '\n';
  }

  return 0;
}
