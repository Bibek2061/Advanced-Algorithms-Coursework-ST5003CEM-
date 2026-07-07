#include <stdio.h>
#include <stdlib.h>
#include <pthread.h>
#include <time.h>

#define MAX_SIZE 80000

int data[MAX_SIZE];
int temp[MAX_SIZE];

pthread_mutex_t mutex;

typedef struct
{
    int left;
    int right;
} ThreadData;


/* ==========================================================
   RANDOM DATA GENERATION
   ========================================================== */

void generate_data()
{
    srand(time(NULL));

    for(int i=0;i<MAX_SIZE;i++)
    {
        data[i]=rand()%100000;
    }
}


/* ==========================================================
   MERGE FUNCTION
   ========================================================== */

void merge(int left,int mid,int right)
{
    int i=left;
    int j=mid+1;
    int k=left;

    while(i<=mid && j<=right)
    {
        if(data[i]<=data[j])
            temp[k++]=data[i++];
        else
            temp[k++]=data[j++];
    }

    while(i<=mid)
        temp[k++]=data[i++];

    while(j<=right)
        temp[k++]=data[j++];

    for(i=left;i<=right;i++)
        data[i]=temp[i];
}


/* ==========================================================
   SEQUENTIAL MERGE SORT
   ========================================================== */

void merge_sort(int left,int right)
{
    if(left>=right)
        return;

    int mid=(left+right)/2;

    merge_sort(left,mid);
    merge_sort(mid+1,right);

    merge(left,mid,right);
}
/* ==========================================================
   PARALLEL SORT THREAD FUNCTION
   ========================================================== */

void* parallel_sort(void* arg)
{
    ThreadData* data_range = (ThreadData*)arg;

    int left = data_range->left;
    int right = data_range->right;

    merge_sort(left, right);

    pthread_mutex_lock(&mutex);
    printf("Thread sorted range %d to %d\n", left, right);
    pthread_mutex_unlock(&mutex);

    pthread_exit(NULL);
}

/* ==========================================================
   CHECK IF ARRAY IS SORTED
   ========================================================== */

int is_sorted()
{
    for(int i=1;i<MAX_SIZE;i++)
    {
        if(data[i-1]>data[i])
            return 0;
    }

    return 1;
}


/* ==========================================================
   TIME DIFFERENCE IN SECONDS
   ========================================================== */

double time_difference(struct timespec start, struct timespec end)
{
    double seconds = end.tv_sec - start.tv_sec;
    double nanoseconds = end.tv_nsec - start.tv_nsec;

    return seconds + nanoseconds / 1000000000.0;
}


/* ==========================================================
   PARALLEL MERGE SORT USING THREADS
   ========================================================== */

double run_parallel_sort(int thread_count)
{
    pthread_t threads[thread_count];
    ThreadData ranges[thread_count];

    int chunk = MAX_SIZE / thread_count;

    struct timespec start, end;

    generate_data();

    clock_gettime(CLOCK_MONOTONIC, &start);

    for(int i=0;i<thread_count;i++)
    {
        ranges[i].left = i * chunk;

        if(i == thread_count - 1)
            ranges[i].right = MAX_SIZE - 1;
        else
            ranges[i].right = (i + 1) * chunk - 1;

        pthread_create(&threads[i], NULL, parallel_sort, &ranges[i]);
    }

    for(int i=0;i<thread_count;i++)
    {
        pthread_join(threads[i], NULL);
    }

    int current_size = chunk;

    while(current_size < MAX_SIZE)
    {
        for(int left=0; left<MAX_SIZE-1; left += 2*current_size)
        {
            int mid = left + current_size - 1;
            int right = left + 2*current_size - 1;

            if(right >= MAX_SIZE)
                right = MAX_SIZE - 1;

            if(mid < right)
                merge(left, mid, right);
        }

        current_size *= 2;
    }

    clock_gettime(CLOCK_MONOTONIC, &end);

    return time_difference(start, end);
}

/* ==========================================================
   MAIN FUNCTION
   ========================================================== */

int main()
{
    pthread_mutex_init(&mutex, NULL);

    struct timespec start, end;

    printf("=============================================\n");
    printf("TASK 5 - CONCURRENT PROGRAMMING\n");
    printf("Parallel Merge Sort using POSIX Threads\n");
    printf("=============================================\n\n");

    /* Sequential Version */
    generate_data();

    clock_gettime(CLOCK_MONOTONIC, &start);

    merge_sort(0, MAX_SIZE - 1);

    clock_gettime(CLOCK_MONOTONIC, &end);

    double sequential_time = time_difference(start, end);

    printf("Sequential Merge Sort\n");
    printf("----------------------\n");
    printf("Execution Time : %.6f seconds\n", sequential_time);
    printf("Sorted         : %s\n\n", is_sorted() ? "YES" : "NO");


    /* Parallel Versions */
    int thread_counts[] = {1, 2, 4, 8};

    printf("Parallel Merge Sort Results\n");
    printf("-------------------------------------------------------------\n");
    printf("%-10s %-15s %-15s\n", "Threads", "Time (s)", "Speedup");
    printf("-------------------------------------------------------------\n");

    for(int i = 0; i < 4; i++)
    {
        double parallel_time = run_parallel_sort(thread_counts[i]);

        double speedup = sequential_time / parallel_time;

        printf("%-10d %-15.6f %-15.2f\n",
               thread_counts[i],
               parallel_time,
               speedup);
    }

    pthread_mutex_destroy(&mutex);

    return 0;
}