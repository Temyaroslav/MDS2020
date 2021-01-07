#include <iostream>

using namespace std;

char *encode(char *src);

int main(){

  char str[] = {"aaaabbbccc"};

  cout << encode(str) << endl;

  return 0;
}

char *encode(char *src){

  char cur_ch = src[0];
  int count = 0;
  string res = "";

  for (int i = 0; i < strlen(src); i++){
    if (src[i] != cur_ch){
      res += cur_ch;
      res += to_string(count);
      cur_ch = src[i];
      count = 1;
    }
    else{
      count++;
    }
  }

  res += cur_ch;
  res += to_string(count);

  int len = res.length();
  char *ch = new char[len + 1];

  for (int i = 0; i < len; i++)
    *(ch + i) = res[i];

  ch[len] = '\0';

  return ch;
}
