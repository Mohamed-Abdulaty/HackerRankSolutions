#include <bits/stdc++.h>

using namespace std;

constexpr int hourGlassbaseSize = 3;

// Complete the hourglassSum function below.
int hourglassSum(vector<vector<int>> arr) {
    int ret{0}, s{0};
    for(int i = 0; i < arr[0].size() - hourGlassbaseSize + 1; i++) {
        for(int j = 0; j < arr.size() - hourGlassbaseSize + 1; j++) {
            s  = arr[i  ][j] + arr[i  ][j+1] + arr[i  ][j+2] +
                               arr[i+1][j+1] +
                 arr[i+2][j] + arr[i+2][j+1] + arr[i+2][j+2];
            ret = std::max<int>(ret, s);
        }        
    }
    return ret;
}

int main()
{
    ofstream fout(getenv("OUTPUT_PATH"));

    vector<vector<int>> arr(6);
    for (int i = 0; i < 6; i++) {
        arr[i].resize(6);

        for (int j = 0; j < 6; j++) {
            cin >> arr[i][j];
        }

        cin.ignore(numeric_limits<streamsize>::max(), '\n');
    }

    int result = hourglassSum(arr);

    fout << result << "\n";

    fout.close();

    return 0;
}
