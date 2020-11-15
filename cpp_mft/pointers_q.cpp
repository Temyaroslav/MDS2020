#include <iostream>
using namespace std;

void q1(){
  int arr[] = {10, 20};
  int *p1 = arr;
  ++*p1;
  cout << arr[0] << " " <<
      arr[1] << " " << *p1 << endl;

}

void q2(){
  int arr[] = {10, 20};
  int *p2 = arr;
  cout << *p2++ << " ";
  cout << arr[0] << " " <<
      arr[1] << " " << *p2 << endl;
}

void q3(){
  int arr[] = {10, 20};
  int *p3 = arr;
  cout << *++p3 << " ";
  cout << arr[0] << " " <<
      arr[1] << " " << *p3 << endl;
}

int main() {
    // q1();
    // q2();
    q3();

    return 0;
}
