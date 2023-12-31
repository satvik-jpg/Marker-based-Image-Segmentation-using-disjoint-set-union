// step1:display_org_image.py to know the position of markers
// step2:display_gradient_image.py to store the gradient array in data2.txt
// step3:run test.cpp to generate segmented image array
// step4:run display_image_from_txt.py to get the segmented image border or run display_rgb_segmented_image
#include <iostream>
#include <fstream>
#include <sstream>
#include <vector>
#include <map>
#include <algorithm>
#include <set>
using namespace std;
typedef long long ll;
vector<ll> parent;
vector<double> image;
vector<double> final_segmented_image;
ll width, height;
ll FIND(ll p)
{
    if (parent[p] >= 0)
    {
        parent[p] = FIND(parent[p]);
        return parent[p];
    }
    else
    {
        return (p);
    }
}
void UNION(ll p, ll r)
{
    if (parent[p] == -1 && parent[r] == -2)
        parent[p] = -2;
    parent[r] = p;
}
void MARKER(ll p, ll p1)
{
    if (p1 >= 0 && p1 <= width * (height - 1) + width - 1)
    {
        if (parent[p1] != -3)
        {
            ll root = FIND(p1);
            if (root != p)
                UNION(p, root);
        }
    }
}
void NON_MARKER(ll p, ll p1)
{
    if (p1 >= 0 && p1 <= width * (height - 1) + width - 1)
    {
        if (parent[p1] != -3)
        {
            ll root = FIND(p1);
            if (root != p)
            {
                if (parent[p] == -1 || parent[root] == -1)
                    UNION(p, root);
            }
        }
    }
}
void HIGHLIGHT(ll p, ll p1)
{
    if (p1 >= 0 && p1 <= width * (height - 1) + width - 1)
    {
        if (parent[p] > parent[p1])
        {
            final_segmented_image[p] = 255;
        }
    }
}
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
    parent.assign(width * height, -3);
    final_segmented_image.assign(width * height, 0);
    ll x1, y1, x2, y2, c1, c2;
    // jour.jpg
    //  y1 = 217;
    //  x1 = 466;
    //  y2 = 306;
    //  x2 = 612;

    // cart.jpg
    // y1 = 208;
    // x1 = 190;
    // y2 = 286;
    // x2 = 344;

    // moount.jpg
    y1 = 73;
    x1 = 142;
    y2 = 238;
    x2 = 393;
    for (ll k = 1; k <= 2; k++)
    {
        // cout << "Enter the coordinates corresponding to marker : " << endl;
        // cin >> y1 >> x1 >> y2 >> x2;

        for (ll i = 0; i < height; i++)
        {
            for (ll j = 0; j < width; j++)
            {
                if (i >= y1 && i <= y2 && (j == x2 || j == x1))
                {
                    image[i * width + j] = -1;
                }
                if (j >= x1 && j <= x2 && (i == y1 || i == y2))
                {
                    image[i * width + j] = -1;
                }
            }
        }
        // jour.jpg
        //  y1 = 117;
        //  x1 = 110;
        //  y2 = 284;
        //  x2 = 352;

        // cart.jpg
        // y1 = 190;
        // x1 = 662;
        // y2 = 329;
        // x2 = 815;

        // mount.jpg
        y1 = 762;
        x1 = 303;
        y2 = 860;
        x2 = 476;
    }
    inputFile.close();
    vector<pair<ll, ll>> m;
    for (ll i = 0; i < height; i++)
    {
        for (ll j = 0; j < width; j++)
        {
            m.push_back({image[i * width + j], (i * width + j)});
        }
    }
    sort(m.begin(), m.end());
    for (auto pixel_list : m)
    {
        ll pixel = pixel_list.second;
        if (pixel_list.first == -1)
        {
            parent[pixel] = -2;
            MARKER(pixel, pixel - width - 1);
            MARKER(pixel, pixel - width);
            MARKER(pixel, pixel - width + 1);
            MARKER(pixel, pixel - 1);
            MARKER(pixel, pixel + 1);
            MARKER(pixel, pixel + width - 1);
            MARKER(pixel, pixel + width);
            MARKER(pixel, pixel + width + 1);
        }
        else
        {
            parent[pixel] = -1;
            NON_MARKER(pixel, pixel - width - 1);
            NON_MARKER(pixel, pixel - width);
            NON_MARKER(pixel, pixel - width + 1);
            NON_MARKER(pixel, pixel - 1);
            NON_MARKER(pixel, pixel + 1);
            NON_MARKER(pixel, pixel + width - 1);
            NON_MARKER(pixel, pixel + width);
            NON_MARKER(pixel, pixel + width + 1);
        }
    }
    ll group = 1;
    for (ll i = m.size() - 1; i >= 0; i--)
    {
        ll pixel = (m[i]).second;
        if (parent[pixel] < 0)
        {
            parent[pixel] = group;
            group = group + 1;
        }
        else
        {
            parent[pixel] = parent[parent[pixel]];
        }
    }
    // cout << group << endl;

    for (auto pixel_list : m)
    {
        ll pixel = pixel_list.second;
        HIGHLIGHT(pixel, pixel - width - 1);
        HIGHLIGHT(pixel, pixel - width);
        HIGHLIGHT(pixel, pixel - width + 1);
        HIGHLIGHT(pixel, pixel - 1);
        HIGHLIGHT(pixel, pixel + 1);
        HIGHLIGHT(pixel, pixel + width - 1);
        HIGHLIGHT(pixel, pixel + width);
        HIGHLIGHT(pixel, pixel + width + 1);
    }

    ofstream outputFile("output.txt");
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            outputFile << final_segmented_image[i * width + j] << " ";
        }
        outputFile << endl;
    }
}