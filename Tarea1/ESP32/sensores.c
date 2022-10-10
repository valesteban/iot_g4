#include <stdio.h>
#include <stdlib.h>

#define MY_PI 3.1415926f

#include <math.h>

// valores para THPC dados en el enunciado
#define MIN_TEMP 5
#define MAX_TEMP 30
#define MIN_HUM 30
#define MAX_HUM 80
#define MIN_PRES 1000
#define MAX_PRES 1200
#define MIN_CO2 30
#define MAX_CO2 200

#define MIN_BATT_LEVEL 1
#define MAX_BATT_LEVEL 100

// valores para ACC KPI del enunciado
#define MIN_AMPX 0.0059f
#define MAX_AMPX 0.12f
#define MIN_AMPY 0.0041f
#define MAX_AMPY 0.11f
#define MIN_AMPZ 0.008f
#define MAX_AMPZ 0.15f
#define MIN_FRECX 29.0f
#define MAX_FRECX 31.0f
#define MIN_FRECY 59.0f
#define MAX_FRECY 61.0f
#define MIN_FRECZ 89.0f
#define MAX_FRECZ 91.0f

/*
Retorna un numero flotante aleatorio en el rango [min, max]
*/
float randFloat(float min, float max)
{
    return min + rand()*(max-min)/RAND_MAX; 
    // hay promoción de rand() desde int a float al multiplicar por (max-min), por lo que no es necesario hacer un cast a float
}

/*
Retorna un numero entero aleatorio en el rango [min, max-1]
*/
int randInt(int min, int max)
{
    return (rand() % (max-min)) + min;
}

/*
typedef struct {
    float accx;
    float accy;
    float accz;
} Accel;

int accelInit(Accel *pAccel, int n)
{
    pAccel->accx = 2*sinf(2*MY_PI*0.001f*n);
    pAccel->accy = 3*cosf(2*MY_PI*0.001f*n);
    pAccel->accz = 10*sinf(2*MY_PI*0.001f*n);
    return 0;
}

int printAccel(Accel *pAccel)
{
    printf("{Acc_x: %.4f; Acc_y: %.4f; Acc_z: %.4f}\n", pAccel->accx, pAccel->accy, pAccel->accz);
    return 0;
}

typedef struct {
    Accel* data;
} AccelSensor;

int accelSInit(AccelSensor* pAccelS, int size)
{
    int randomN = randInt(0,size * 2);
    pAccelS->data = malloc(size * sizeof(Accel));

    for(int i = 0; i < size; i++ )
    {
        Accel acc ;
        accelInit(&acc, randomN+i);
        printAccel(&acc);
        pAccelS->data[i] = acc;
    }
}
*/

/*
Estructura para representar un arreglo de puntos que representan aceleraciones.
Cada dimensión X,Y,Z están representadas en arreglos de largo size
*/
typedef struct {
    float* datax;
    float* datay;
    float* dataz;
    int size;
} AccelSensor;

int accelDataSet(AccelSensor* pAccelS, int index, float accx, float accy, float accz)
{
    if( index < 0 || index >= pAccelS->size)
    {
        return -1;
    }
    else
    {
        *(pAccelS->datax+index) = accx;
        *(pAccelS->datay+index) = accy;
        *(pAccelS->dataz+index) = accz;
        return 0;
    }
}

int printAccelPoint(AccelSensor* pAccelS, int index)
{
    if( index < 0 || index >= pAccelS->size)
    {
        return -1;
    }
    else
    {
        float* startx = pAccelS->datax;
        float* starty = pAccelS->datay;
        float* startz = pAccelS->dataz;
        printf("{Acc_x: %.4f; Acc_y: %.4f; Acc_z: %.4f}", *(startx+index), *(starty+index), *(startz+index));
        return 0;
    }
}


int accelInit(AccelSensor* pAccelS, int size)
{
    pAccelS->size = size;
    int randomN = randInt(0,size * 2);
    pAccelS->datax = NULL;
    pAccelS->datay = NULL;
    pAccelS->dataz = NULL;

    // falto memoria, fallo malloc, algo malo paso :(
    if( NULL == (pAccelS->datax = malloc(size * sizeof(float))))
    {
        return -1;
    }
    if( NULL == (pAccelS->datay = malloc(size * sizeof(float))))
    {
        return -1;
    }
    if( NULL == (pAccelS->dataz = malloc(size * sizeof(float))))
    {
        return -1;
    }

    for(int i = 0; i < size; i++ )
    {
        int n = randomN+i;
        float accx = 2*sinf(2*MY_PI*0.001f*n);
        float accy = 3*cosf(2*MY_PI*0.001f*n);
        float accz = 10*sinf(2*MY_PI*0.001f*n);
        accelDataSet(pAccelS, i, accx, accy, accz);
    }
    return 0;  
}

int printAccelP(AccelSensor* pAccelS)
{
    printf("[");
    for(int i=0; i < (pAccelS->size-1); i++)
    {

        printAccelPoint(pAccelS, i);
        printf(",\n");
    }
    printAccelPoint(pAccelS, pAccelS->size-1);
    printf("]\n");
}

/*
Estructura para almacenar datos de temperatura, humedad, presion y CO2
*/
typedef struct {
    char temp;
    char hum;
    float pres;
    float co2;
} ThpcSensor;

int thpcSInit(ThpcSensor* pThpcS)
{
    pThpcS->temp = (char) randInt(MIN_TEMP, MAX_TEMP+1);
    pThpcS->hum  = (char) randInt(MIN_HUM, MAX_HUM+1);
    pThpcS->pres = randFloat(MIN_PRES, MAX_PRES);
    pThpcS->co2  = randFloat(MIN_CO2, MAX_CO2);
    return 0;

}

int printThpcS(ThpcSensor* pThpcS)
{
    printf("{temp: %d; hum: %d; pres: %.4f; hum: %.4f}", pThpcS->temp, pThpcS->hum, pThpcS->pres, pThpcS->co2);
}

typedef struct {
    char level;
} BattSensor;

int battSInit(BattSensor* pBattS)
{
    pBattS->level = (char) randInt(MIN_BATT_LEVEL, MAX_BATT_LEVEL+1);
    return 0;
}

typedef struct {
    float ampx;
    float frecx;
    float ampy;
    float frecy;
    float ampz;
    float frecz;
    float rms;
} AccelKpi;

int accelKInit(AccelKpi* pAccelK)
{
    float ampx = randFloat(MIN_AMPX, MAX_AMPX);
    float ampy = randFloat(MIN_AMPY, MAX_AMPY);
    float ampz = randFloat(MIN_AMPZ, MAX_AMPZ);

    pAccelK->ampx = ampx;
    pAccelK->frecx = randFloat(MIN_FRECX, MAX_FRECX);
    pAccelK->ampy = ampy;
    pAccelK->frecy = randFloat(MIN_FRECY, MAX_FRECY);
    pAccelK->ampz = ampz;
    pAccelK->frecz = randFloat(MIN_FRECZ, MAX_FRECZ);
    pAccelK->rms = sqrtf(ampx*ampx + ampy*ampy + ampz * ampz);

    return 0;

}


int main()
{
    AccelSensor a;
    accelInit(&a, 5);
    printAccelP(&a);
    printAccelPoint(&a, 3);
    return 0;
}
