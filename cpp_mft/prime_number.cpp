#include <iostream>

int main(){
  int n;
  std::cin >> n;

  bool flag = true;

  if (n <= 1){
    flag = false;
  }
  else{
    for (int i = 2; i < n; i++){
      if (n % i == 0)
        flag = false;
    }
  }

  std::cout << flag << '\n';

  // flag ? std::cout << flag << '\n';

  return 0;
}
