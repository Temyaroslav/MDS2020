#include <iostream>
#include <string>

using namespace std;

int strstr(string, string);

int main(){
  string s = "GeeksForGeeks", x = "Fr";

  cout << strstr(s, x) << endl;

  return 0;
}

int strstr(string s, string x){
  int c = -1;
  bool flag;

  for (int i = 0; i < s.length(); i++){
    if (s[i] == x[0]){
      c = i;
      flag = true;
      for (int j = 1; j < x.length(); j++){
        if (s[i + j] != x[j]){
          c = -1;
          flag = false;
          break;
        }
      }
      if (flag)
        break;
    }
  }

  return c;
}
