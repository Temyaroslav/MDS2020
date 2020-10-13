#include <iostream>
#include <string>
#include <sstream>
#include <vector>

int get_unique(int n){
    int res = 0;
    int cnt[10] = {0};
    while (n > 0){
        int rem = n % 10;
        cnt[rem]++;

        n = n / 10;
    }

    for (int i = 0; i < 10; i++){
        if (cnt[i] == 1){
            res++;
        }
    }

    return res;
}

int main()
{
    using namespace std;

    string input;
    vector<string> v;
    int pnl = 0;

    while (getline(cin, input)){
        istringstream iss(input);
        v.clear();
        for (string s; iss >> s; )
            v.push_back(s);

        if (v[1] == "A999AA"){
            break;
        }
        else {
            stringstream ss(v[0]);
            int speed;
            ss >> speed;
            if (speed > 60){
                stringstream ss(v[1].substr(1, 3));
                int x;
                ss >> x;
                int c = get_unique(x);

                if (c == 3){
                    pnl += 100;
                }
                else if (c == 1){
                    pnl += 500;
                }
                else if (c == 0){
                    pnl += 1000;
                }
            }
        }
    }

    cout << pnl << endl;

    return 0;
}
