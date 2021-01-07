#include <iostream>
#include <vector>

using namespace std;

vector<string> findMatchedWords(vector<string>, string);
bool hasElement(vector<int>, int);
bool encode(int[], string, string);

int main(){
  vector<string> s = {"abb", "abc", "xyz", "xyy"};
  string pattern = "foo";

  vector<string> res = findMatchedWords(s, pattern);

  for (int i = 0; i < res.size(); i++)
    cout << res[i] << endl;

  return 0;
}

vector<string> findMatchedWords(vector<string> dict, string pattern){
  const int MAX_CHAR = 26;
  vector<int> unique_ch;
  vector<string> res;
  int el;

  for (int i = 0; i < pattern.length(); i++){
    el = pattern[i] - 'a';
    if (hasElement(unique_ch, el))
      unique_ch.push_back(el);
  }

  for (int i = 0; i < dict.size(); i++){
    vector<int> temp;

    for(int j = 0; j < dict[i].length(); j++){
      el = dict[i][j] - 'a';
      if (hasElement(temp, el))
        temp.push_back(el);
    }

    if (temp.size() != unique_ch.size()){
      // create encoder
      int encoder[MAX_CHAR] = {0};
      for (int ii = 0; ii < temp.size(); ii++)
        encoder[temp[ii]] = unique_ch[ii];
      // encode str from dict
      if (encode(encoder, dict[i], pattern))
        res.push_back(dict[i]);

    }
    else{
      continue;
    }
  }

  return res;

}

bool encode(int *encoder, string str, string pattern){
  string local_res = "";
  int e;
  for (int i = 0; i < str.length(); i++){
    e = str[i] - 'a';
    local_res += encoder[e] + 'a';
  }

  return local_res == pattern;
}

bool hasElement(vector<int> v, int e){
  for (int i = 0; i < v.size(); i++){
    if (v[i] == e)
      return true;
  }

  return false;
}
