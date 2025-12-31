#include <iostream>
#include <string>
#include <algorithm>
#include <ctime>
#include <filesystem>

using namespace std;
namespace fs = std::filesystem;

uintmax_t count_size(const std::string filename){
   
    try{
        if (fs::exists(filename)){
            uintmax_t size = fs::file_size(filename);
            return size;
        }else{
            std::cout << "File not found" << endl;
            return NULL;
        }
    }catch(std::exception& e){
        std::cerr << "Error: " << e.what() << endl;
    }
}


int main(){
    uintmax_t res = count_size("test.txt");
    std::cout << res << endl; // baits
    return 0;
}