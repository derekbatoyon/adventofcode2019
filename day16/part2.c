#include <ctype.h>
#include <pthread.h>
#include <stdarg.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <time.h>
#include <unistd.h>

const int thread_count = 8;

int locked_fprintf(FILE * restrict stream, const char * restrict format, ...)
{
    static pthread_mutex_t printer_mutex = PTHREAD_MUTEX_INITIALIZER;

    va_list args;
    va_start(args, format);

    pthread_mutex_lock(&printer_mutex);
    int result = vfprintf(stream, format, args);
    pthread_mutex_unlock(&printer_mutex);

    va_end(args);

    return result;
}

struct job_t
{
    char * input;
    char * output;
    int length;
    int min;
    int max;
};

int parse_phases(char * arg, int * pphases)
{
    if ((arg == NULL) || (arg[0] != '-')) return 0;
    if (*(++arg) == '\0') return 0;

    char * endptr;
    int result = strtol(arg, &endptr, 10);
    if (*endptr == '\0')
    {
        if (pphases != NULL) *pphases = result;
        return 1;
    }

    return 0;
}

int filesize(char * filename)
{
    struct stat info;
    int error = stat(filename, &info);
    if (error)
    {
        perror("stat");
        exit(EXIT_FAILURE);
    }

    return info.st_size;
}

void dump_message(FILE * fout, char * message, int length)
{
    if (message == NULL) return;

    for (int i=0; i<length; ++i)
    {
        fprintf(fout, "%d", message[i]);
    }
    fprintf(fout, "\n");
}

void * thread_func(void * arg)
{
    struct job_t * pjob = (struct job_t *)arg;

    char * input = pjob->input;
    char * output = pjob->output;
    int length = pjob->length;
    int min = pjob->min;
    int max = pjob->max;

    //locked_fprintf(stderr, "%2d -> %d\n", min, max);

    for (int i=min; i<max; ++i)
    {
        int step = (i + 1) * 4;
        int total = 0;
        for (int offset=0; offset<=i; ++offset)
        {
            int start = i + offset;
            for (int index=start; index<length; index+=step)
            {
                total += input[index];
            }
            start = 3 * i + 2 + offset;
            for (int index=start; index<length; index+=step)
            {
                total -= input[index];
            }
        }
        output[i] = abs(total) % 10;
    }

    return NULL;
}

void execute(char * input, char * output, int length)
{
    pthread_t threads[thread_count];
    struct job_t jobs[thread_count];

    div_t q = div(length, thread_count);
    int work_per_thread = q.quot;
    int extra_work = q.rem;

    int ti = 0;
    int last_limit = 0;

    while (extra_work)
    {
        jobs[ti].input = input;
        jobs[ti].output = output;
        jobs[ti].length = length;
        jobs[ti].min = last_limit;
        jobs[ti].max = jobs[ti].min + work_per_thread + 1;
        last_limit = jobs[ti].max;
        --extra_work;

        int error = pthread_create(&threads[ti], NULL, thread_func, (void *)&jobs[ti]);
        if (error) goto pthread_failure;

        ++ti;
    }

    for (; ti<thread_count; ++ti)
    {
        jobs[ti].input = input;
        jobs[ti].output = output;
        jobs[ti].length = length;
        jobs[ti].min = last_limit;
        jobs[ti].max = jobs[ti].min + work_per_thread;
        last_limit = jobs[ti].max;

        int error = pthread_create(&threads[ti], NULL, thread_func, (void *)&jobs[ti]);
        if (error) goto pthread_failure;
    }

    for (int ti=0; ti<thread_count; ++ti)
    {
        pthread_join(threads[ti], NULL);
    }

    return;

pthread_failure:
    locked_fprintf(stderr, "failed to create thread\n");
    exit(EXIT_FAILURE);
}

int read_input(char * filename, char * buffer)
{
    FILE * fin = fopen(filename, "r");
    if (fin == NULL)
    {
        perror("fopen");
        exit(EXIT_FAILURE);
    }

    char * ptr = buffer;
    while (fread(ptr, 1, 1, fin))
    {
        if (isdigit(*ptr))
        {
            *ptr -= '0';
            ++ptr;
        }
    }

    if (ferror(fin))
    {
        perror("fread");
        exit(EXIT_FAILURE);
    }

    fclose(fin);
    return ptr - buffer;
}

int repeat_input(char * buffer, int message_length, int multiplier)
{
    for (int i=0; i<message_length; ++i)
    {
        for (int j=1; j<multiplier; ++j)
        {
            int index = j * message_length + i;
            buffer[index] = buffer[i];
        }
    }
    return message_length * multiplier;
}

int main(int argc, char * argv[])
{
    time_t curtime;

    int message_length = 0;
    int multiplier = 1;
    int phases = 1;
    char * input_file;

    int opt;
    while ((opt = getopt(argc, argv, "m:p:")) != -1)
    {
        switch (opt)
        {
            case 'm':
                multiplier = atoi(optarg);
                break;
            case 'p':
                phases = atoi(optarg);
                break;
            default: /* '?' */
                fprintf(stderr, "usage: %s [-m multiplier] input_file\n", argv[0]);
                exit(EXIT_FAILURE);
        }
    }

    if (optind >= argc)
    {
        fprintf(stderr, "usage: %s [-m multiplier] input_file\n", argv[0]);
        exit(EXIT_FAILURE);
    }

    input_file = argv[optind];
    message_length = filesize(input_file);

    char * buffer_a = (char *)malloc(message_length * multiplier);
    char * buffer_b = (char *)malloc(message_length * multiplier);
    if (buffer_a == NULL || buffer_b == NULL)
    {
        fprintf(stderr, "not enough memory\n");
        exit(EXIT_FAILURE);
    }

    message_length = read_input(input_file, buffer_a);
    message_length = repeat_input(buffer_a, message_length, multiplier);

    if (phases == 1)
    {
        time(&curtime);
        locked_fprintf(stderr, "start %s", ctime(&curtime));

        execute(buffer_a, buffer_b, message_length);
        dump_message(stdout, buffer_b, message_length);
    }
    else
    {
        for (int half_phase=0; half_phase<phases/2; ++half_phase)
        {
            time(&curtime);
            locked_fprintf(stderr, "phase %d start %s", half_phase*2+1, ctime(&curtime));

            execute(buffer_a, buffer_b, message_length);
            execute(buffer_b, buffer_a, message_length);
        }

        if (phases % 2 == 0)
        {
            dump_message(stdout, buffer_a, 8);
        }
        else
        {
            time(&curtime);
            locked_fprintf(stderr, "phase %d start %s", phases, ctime(&curtime));

            execute(buffer_a, buffer_b, message_length);
            dump_message(stdout, buffer_b, 8);
        }
    }

    time(&curtime);
    locked_fprintf(stderr, "finish %s", ctime(&curtime));

    free(buffer_a);
    free(buffer_b);

    return 0;
}
