#include <iostream> 
#include <fstream>
#include <list>
#include <string.h>

//using namespace std;

//neighbor table list item type
struct neighborType
{
    std::string currNodeIF;          // currNodeIF
    std::string currNeighborIF;       // currNeighborIF
    float neigborLastTimeSeen;   // neigborLastTimeSeen
                                //using float because the value is in seconds
};

void getNeighbors(unsigned int* numberOfNeighbors, std::list <neighborType>& neighborList ){

    //assumes neighborList is empty
    std::string outFileName = "neighbors.txt";

    //build the command string
    std::string commandStr;
    commandStr = "sudo batctl n > ";
    commandStr += outFileName;

    //system call to batctl's neighbors table

    system(commandStr.c_str());

    //open file
    std::ifstream neighborInFile;
    neighborInFile.open(outFileName);
         //if there is no file return error     TO DO

    //read first 2 lines (assumes the first 2 lines are always there)
    std::string inString;
  
    getline(neighborInFile, inString)   ;
    getline(neighborInFile, inString);
   
    //primer read to loop through the file
    getline(neighborInFile, inString);

    while(neighborInFile.good()){
        neighborType neighborNode;
        //get Indices

        int StartIdx;
        int counter = 0;

        while (inString[counter] == ' '){
            counter++;
        }

        StartIdx = counter;

        //get IF
        counter = StartIdx;
        while (inString[counter] != ' '){
            counter++;
        }
        
        neighborNode.currNodeIF = inString.substr(StartIdx, counter - StartIdx - 1);

        //cycle through the spaces
        while (inString[counter] == ' '){
            counter++;
        }

        //get Neighbor IF Address
        StartIdx = counter;
        while (inString[counter] != ' '){
            counter++;
        }
    
        neighborNode.currNeighborIF = inString.substr(StartIdx, counter - StartIdx);

        //cycle through the spaces
        while (inString[counter] == ' '){
            counter++;
        }
        
        //get time
        StartIdx = counter;
    
        neighborNode.neigborLastTimeSeen = 
                    std::stof(inString.substr(StartIdx, inString.length() - StartIdx));

        //next up add the items to the list

        neighborList.push_back(neighborNode);

        getline(neighborInFile, inString);
    }
    *numberOfNeighbors = neighborList.size();
    neighborInFile.close();
}
//deviceID is MAC address
//numPackets is the number of packets sent by ping.
//packetsLost is the percentage of packets lost.  Using integer because the 
//data type that outputs the statistic is an unsinged integer 0 means
// perfect transmission and 100% means nothing was transmitted
void pingDevice(std::string deviceID, int* packetsLost, int numPackets = 1){
    
    std::string outFileName = "ping.txt";
    //build the command string
    std::string commandStr;
    commandStr = "sudo batctl p -c ";
    commandStr += std::to_string(numPackets);
    commandStr += " ";
    commandStr += deviceID;
    commandStr += " > ";
    commandStr += outFileName;

    //execute ping command 
    system(commandStr.c_str());

    //open file
    std::ifstream pingInFile;
    pingInFile.open(outFileName);
    //if there is no file return error     TO DO

    std::string inString;
    size_t pos;
    int numPos;

    //primer read to loop through the entire file in an attempt to get the 
    //line that contains percent sign the file that contains ping statistics

    getline(pingInFile, inString);
    
    while(pingInFile.good()){
        pos = inString.find("%");
        //cout << inString << " Pos: " << pos <<" nPos: " << string::npos << endl; 

        if (pos != std::string::npos ){
            break;
    }

        getline(pingInFile, inString);
    }

    numPos = pos;
    //cout << pos << " Nse 0_pos" << endl; 
    //cout << inString[numPos-1] << " Nse 0" << endl; 
    while (isdigit(inString[numPos-1]))
    {
        //cout << inString[numPos-1] << " Nse 0" << endl; 
        numPos--;

    }

   
    *packetsLost = stoi(inString.substr(numPos, pos - numPos));  
    //cout << inString.substr(numPos, pos - numPos) << " Nse num" << endl;    //debug statement
    pingInFile.close();

}

int main(int argc, char **argv)
{
    unsigned int numberOfNeighborDevices = 0;
    std::list <neighborType> listOfNeighborDevices;
    int lostPackets;

    //pingDevice("50:3e:aa:89:f2:0d", &lostPackets, 1);
    //cout << " Percent Packets lost:  " << lostPackets << endl;

    //get list of neighboring devices
    getNeighbors(&numberOfNeighborDevices, listOfNeighborDevices); 
    
    //after getting a list of neighors, ping the neighbors
    //go through the list if there are one or more neighbors
    if (numberOfNeighborDevices > 0){
        for (auto it = listOfNeighborDevices.begin(); it != listOfNeighborDevices.end(); ++it)
        {
            //pass number of packets default is 1, and MAC address
            std::cout << it->currNeighborIF << std::endl;
            pingDevice(it->currNeighborIF, &lostPackets, 1);
            std::cout << "Node:  " << it->currNeighborIF << " Percent Packets lost:  " << lostPackets << std::endl;
            
        
        }
    }




    /*cout << "Number of neighboring devices:  " << numberOfNeighborDevices << endl;

    int deviceCtr = 1;
    for (auto it = listOfNeighborDevices.begin(); it != listOfNeighborDevices.end(); ++it){
        cout << "Device " << deviceCtr << " Info: " << it->currNeighborIF; 
        cout << ' ' << it->neigborLastTimeSeen << "s" << endl; 
        deviceCtr++;

    }*/
        
    return 0;
}


