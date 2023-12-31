#include <iostream>
#include <fstream>
#include <vector>
#include <sstream>
using namespace std;
typedef long long ll;
ll width, height;
vector<double> image;

void calc_width(string file)
{
    ifstream inputFile2(file);

    // Check if the file is open
    if (!inputFile2.is_open())
    {
        cerr << "Error opening file!" << endl;
        return;
    }

    // Read the content of the file line by line
    string line;
    if (getline(inputFile2, line))
    {
        // Use a stringstream to parse the numbers in the first line
        istringstream iss(line);

        double number;
        int count = 0;

        // Count the numbers in the first line
        while (iss >> number)
        {
            count++;
        }

        // Output the result
        // cout << "Quantity of numbers before the first newline: " << count << std::endl;
        width = count;
    }
    else
    {
        cerr << "Empty file or error reading the first line!" << endl;
    }

    // Close the file
    inputFile2.close();
}
int main()
{
    string file = "data2.txt";
    calc_width(file);
    ifstream inputFile(file);
    if (!inputFile.is_open())
    {
        std::cerr << "Error opening file." << std::endl;
        return 1;
    }
    double number;
    ll i = 0;
    ll j = 0;
    while (inputFile >> number)
    {
        image.push_back(number);
        if (j == width - 1)
        {
            j = 0;
            i++;
        }
        else
            j++;
    }
    height = i;
    cout << width << " " << height << endl;
}
