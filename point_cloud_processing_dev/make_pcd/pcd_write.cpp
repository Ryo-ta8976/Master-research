#include <iostream>
#include <pcl/io/pcd_io.h>
#include <pcl/point_types.h>
#include <fstream>
#include <string>
#include <sstream>
#include <vector>


using namespace std;
int user_data;

vector<string> split(string& input, char delimiter)
{
    istringstream stream(input);
    string field;
    vector<string> result;
    while (getline(stream, field, delimiter)) {
        result.push_back(field);
    }
    return result;
}

int main (int argc, char** argv)
{
  pcl::PointCloud<pcl::PointXYZ> cloud;

  // Fill in the cloud data
  cloud.width    = 100;
  cloud.height   = 96;
  cloud.is_dense = false;
  cloud.points.resize (cloud.width * cloud.height);
  int i=0;

  ifstream ifs("../data/measure1.csv");

　string line;
　while (getline(ifs, line)) {
    vector<string> strvec = split(line, ',');

    cloud.points[i].x = stof(strvec.at(0));
    cloud.points[i].y = stof(strvec.at(1));
    cloud.points[i].z = stof(strvec.at(2));
    i++;
        
    // for (int i=0; i<strvec.size();i++){
    //     printf("%5f\n", stof(strvec.at(i)));
    // }
        
 }

//   for (size_t i = 0; i < cloud.points.size (); ++i)
//   {
//     cloud.points[i].x = 1024 * rand () / (RAND_MAX + 1.0f);
//     cloud.points[i].y = 1024 * rand () / (RAND_MAX + 1.0f);
//     cloud.points[i].z = 1024 * rand () / (RAND_MAX + 1.0f);
//   }

  pcl::io::savePCDFileASCII ("test_pcd.pcd", cloud);
  std::cerr << "Saved " << cloud.points.size () << " data points to test_pcd.pcd." << std::endl;

  for (size_t i = 0; i < cloud.points.size (); ++i)
    std::cerr << "    " << cloud.points[i].x << " " << cloud.points[i].y << " " << cloud.points[i].z << std::endl;



  return (0);
}