#include <iostream>
#include <fstream>
#include <pthread.h>
#include <semaphore.h>
#include <unistd.h>

#include <random>
#include <chrono>
#include <vector>
#include <string>
#include <iomanip>
#include <cmath>

using namespace std;
mt19937 generator(
    chrono::steady_clock::now().time_since_epoch().count()
);
chrono::steady_clock::time_point start_time;
long long getTime()
{
    auto now = chrono::steady_clock::now();

    return chrono::duration_cast<chrono::seconds>(
        now - start_time
    ).count();
}


//global semaphores and locks
int total_operative,group_size,x,y;
int total_groups=0;
sem_t stations[4];
sem_t *groups;
pthread_t staffs[2];
int staff_ids[2] = {1,2};
pthread_mutex_t random_mutex;


pthread_t *operatives;
int *operative_id;
int completed_operations = 0;

sem_t logbook;
pthread_mutex_t reader;
pthread_mutex_t print_mutex;
int reader_count = 0;
pthread_mutex_t completed_mutex;
sem_t *operative_wakeup;
int *operative_state;
pthread_mutex_t arrival_mutex;
bool arrival_event = false;
int awakened_count = 0;
int selected_operative = -1;
int arrival_round = 0;
int getStaffDelay(int staff_id)
{
    pthread_mutex_lock(&random_mutex);
    if (staff_id == 1)
    {
        poisson_distribution<int> dist(5.0);
        pthread_mutex_unlock(&random_mutex);
        return dist(generator) + 1;
        
    }
    else
    {
        poisson_distribution<int> dist(8.0);
        pthread_mutex_unlock(&random_mutex);
        return dist(generator) + 1;
    }
    
}


int getArrivalTime()
{
    pthread_mutex_lock(&random_mutex);
    poisson_distribution<int> distribution(5.0);
    pthread_mutex_unlock(&random_mutex);
    return distribution(generator);
    
}


void initialize(){
    for (int i=0;i<4;i++){
        sem_init(&stations[i],0,1);      // 1 means station is available
        
    }
    
    for(int i=0;i<total_groups;i++)
        sem_init(&groups[i],0,0);
    sem_init(&logbook,0,1);
    pthread_mutex_init(&reader,NULL);
    pthread_mutex_init(&print_mutex,NULL);
    //pthread_mutex_init(&readOps,NULL);
    start_time = chrono::steady_clock::now();
    pthread_mutex_init(&completed_mutex, NULL);
    pthread_mutex_init(&arrival_mutex, NULL);
    operative_wakeup = new sem_t[total_operative];

    operative_state = new int[total_operative];

    for (int i=0;i<total_operative;i++)
    {
        sem_init(&operative_wakeup[i],0,0);
        operative_state[i] = 0;
    }
    pthread_mutex_init(&random_mutex,NULL);
}
void printMessage(string s)
{
    pthread_mutex_lock(&print_mutex);
    cout<<s<<endl;
    pthread_mutex_unlock(&print_mutex);
}

void start_read()
{
    pthread_mutex_lock(&reader);

    reader_count++;
     
    if(reader_count == 1)
    {
        sem_wait(&logbook);
    }

    pthread_mutex_unlock(&reader);
    
}
void end_read()
{
    pthread_mutex_lock(&reader);

    reader_count--;

    if (reader_count == 0)
        sem_post(&logbook);

    pthread_mutex_unlock(&reader);
    
}
void create_arrival_event()
{
    int delay = getArrivalTime();
    sleep(delay);
    pthread_mutex_lock(&arrival_mutex);
    arrival_round++;
    arrival_event = true;
    awakened_count = 0;
    pthread_mutex_lock(&random_mutex);
    uniform_int_distribution<int> distribution(0,total_operative-1);
    pthread_mutex_unlock(&random_mutex);
    for (int i = 0; i < total_operative; i++)
    {
        if (operative_state[i] == 0)
        {
            operative_state[i] = 1;
            awakened_count++;

            sem_post(&operative_wakeup[i]);
        }
    }


    pthread_mutex_unlock(&arrival_mutex);
}
bool wait_for_selection(int number)
{
    int index = number - 1;
    sem_wait(&operative_wakeup[index]);


    pthread_mutex_lock(&arrival_mutex);


    bool selected =
        (index == selected_operative);


    if (selected){

        operative_state[index] = 2;
    }
    else
    {

        operative_state[index] = 0;
    }


    pthread_mutex_unlock(&arrival_mutex);


    return selected;
}

void* station_work(void * arg){      //every op thread will do this after creation
    int number = *(int*) arg;
    int station_no = number%4;

    while ((true))
    {
        bool selected = wait_for_selection(number);
        if (selected) break;
    }
    string message =
                "Operative " +
                to_string(number) +
                " wants station TS" +
                to_string(station_no + 1) +
                " at time " +
                to_string(getTime());
    printMessage(message);
    

    //string message = "Operative " + to_string(number) +" wants station TS" +to_string(station_no+1) +"\n";
    
    sem_wait(&stations[station_no]);

    //do work here ----- > sleeping
    sleep(x);
    //message =  "Operative " + to_string(number) +" has completed document recreation at station TS" + to_string(station_no+1) +"\n";
    //printMessage(message);
    printMessage(
                "Operative " +
                to_string(number) +
                " has completed document recreation at time " +
                to_string(getTime())
            );
    sem_post(&stations[station_no]);
    
    int group_number = (number-1)/group_size;
    

    if(number % group_size == 0)    //leader
    {
        for(int i=0;i<group_size-1;i++)   //wait for all grp members, leader has already completed so -1
        {
            sem_wait(&groups[group_number]);
        }
        printMessage(
                "Unit " +
                to_string(group_number + 1) +
                " has completed document recreation phase at time " +
                to_string(getTime())
            );
        sem_wait(&logbook);
        sleep(y);
        pthread_mutex_lock(&completed_mutex);
        completed_operations++;
        pthread_mutex_unlock(&completed_mutex);
        sem_post(&logbook);
        printMessage(
                "Unit " +
                to_string(group_number + 1) +
                " has completed intelligence distribution at time " +
                to_string(getTime())
            );
    }
    else
    {
        sem_post(&groups[group_number]);
    }

    return NULL;
}


void* staff_work(void* arg)
{
    
    int staff_id = *(int*) arg;

    while(true)
    {
        int delay = getStaffDelay(staff_id);
        sleep(delay);
        start_read();
        pthread_mutex_lock(&completed_mutex);
        int completed = completed_operations;
        pthread_mutex_unlock(&completed_mutex);

        string msg = "Intelligence Staff " + to_string(staff_id)
              + " began reviewing logbook at time "
              + to_string(getTime())
              + ". Operations completed = "
              + to_string(completed_operations)
              + "\n";
        
        
        
        
        printMessage(msg);
        bool finished = (completed_operations == total_groups);
        end_read();
        if (finished) break;
    }
    return NULL;
}

void* arrival_coordinator(void *arg)
{
    (void)arg;
    while(true)
    {
        pthread_mutex_lock(&completed_mutex);
        int completed = completed_operations;
        pthread_mutex_unlock(&completed_mutex);
    }
}

int main(){
    //cin>>total_operative>>group_size>>x>>y;
    ifstream inputFile("input.txt");
    ofstream outputFile("output.txt");
    if (!inputFile.is_open() || !outputFile.is_open())
    {
        cerr << "Error opening input.txt or output.txt" << endl;
        return 1;
    }

    cin.rdbuf(inputFile.rdbuf());
    cout.rdbuf(outputFile.rdbuf());
    cin>>total_operative>>group_size>>x>>y;
     total_groups = total_operative/group_size;
    groups = new sem_t[total_groups];
    operatives = new pthread_t[total_operative];
    operative_id = new int[total_operative];
    initialize();
    pthread_create(&staffs[0],NULL,staff_work,&staff_ids[0]);
    pthread_create(&staffs[1],NULL,staff_work,&staff_ids[1]);
    for (int i=0;i<total_operative;i++){
        operative_id[i] = i+1;
        pthread_create(&operatives[i],NULL,station_work,&operative_id[i]);
    }
    for(int i=0;i<total_operative;i++)
    {
        pthread_join(operatives[i],NULL);
    }
    pthread_join(staffs[0],NULL);
    pthread_join(staffs[1],NULL);
    
        //wait for all threads in this group to finish
        //then do leaders work
        

    for(int i=0;i<4;i++) 
        sem_destroy(&stations[i]);
    for(int i=0;i<total_groups;i++)
        sem_destroy(&groups[i]);
    sem_destroy(&logbook);

    pthread_mutex_destroy(&reader);
    pthread_mutex_destroy(&print_mutex);
    pthread_mutex_destroy(&random_mutex);
    delete[] groups;
    delete[] operatives;
    delete[] operative_id;
}