#include <iostream>
#include <vector>
#include <cmath>

int main() {
  std::vector<int> v;
  int x;

  while (true){
   std::cin >> x;
   if (x == 0){
     break;
   }
   else{
     v.push_back(x);
   }
 }

   int c = 0;
   for(std::vector<int>::size_type i = 0; i != v.size(); i++){
    if (std::abs(v[i]) % 2 == 0){
      c++;
    }
  }

  std::cout << c << std::endl;

  return 0;
}
