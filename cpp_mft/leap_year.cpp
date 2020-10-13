#include <iostream>

int main(){
  int year;
  std::cin >> year;

  bool is_leap_year = false;

  if ((year % 4 == 0 && year % 100 != 0) || year % 400 == 0){
    is_leap_year = true;
  }

  if (is_leap_year){
    std::cout << "YES" << '\n';
  }
  else{
    std::cout << "NO" << '\n';
  }

  return 0;
}
