#include <opencv2/opencv.hpp>
#include <iostream>

int main()
{
    // Provide the path to your image file
    std::string imagePath = "cart.jpg";

    // Read the image
    cv::Mat image = cv::imread(imagePath);

    // Check if the image was successfully loaded
    if (image.empty())
    {
        std::cerr << "Error: Could not open or find the image" << std::endl;
        return -1;
    }

    // Display the image (optional)
    cv::imshow("Image", image);
    // cv::waitKey(0); // Wait for a key press

    return 0;
}
