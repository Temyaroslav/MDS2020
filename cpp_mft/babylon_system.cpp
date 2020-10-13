#include <iostream>
#include <string>
#include <sstream>
#include <vector>
#include <cmath>


int main()
{
    using namespace std;

    int n, x, r;
    string res = "";
    cin >> n;

    r = 0;

    while (true){
        if (n < pow(60, r)){
            break;
        }
        else{
            r++;
        }
    }

    for (int i = r - 1; i >= 0; i--){
        int t = n / pow(60, i);
        if (t != 0){
            if (i == 0){
                for (int j = 0; j < n / 10; j++)
                    res +="<";
                for (int j = 0; j < n % 10; j++)
                    res += "v";
                break;
            }
            for (int ii = 0; ii < t; ii++){
                res += "v";
            }
            n -= pow(60, i) * t;
        }

        if (i != 0)
            res += ".";
    }

    cout << res << endl;

    return 0;
}
