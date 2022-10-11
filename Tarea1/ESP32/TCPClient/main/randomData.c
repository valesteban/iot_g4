
/* Un medidor de aceleración para este se generara un vector de 2000
datos por eje. Estos serán floats generados por la siguiente formula (n es un número cualquiera,
deben ser distintos entre datos del mismo eje):
– Accx = 2 · sin(2π · 0.001 · n)
– Accy = 3 · cos(2π · 0.001 · n)
– Accz = 10 · sin(2π · 0.001 · n)

*/
int Acceloremeter_Sensor(){

}

/*
(Temperatura-Humedad-Presión-CO2): representa un sensor de cada uno de
estos aspectos, genere su medición usando los siguientes valores:
– T emp = Valor aletorio entre 5.0 y 30.0
– Hum = Valor aletorio entre 30 a 80
– P res = Valor aletorio entre 1000 y 1200
– CO2 = Valor aletorio entre 30.0 y 200.0
*/
int  THPC_Sensor(){

}

/* representando el nivel de bateria del aparato, debera ser un valor entre 1 y 100*/
int  Batt_sensor(){

}

/*representa un sensor de vibraciones, midiendo en los tres ejes y sacando
su promedio (RMS, root mean square), para sus valores use:
– Ampx = valor aletorio entre 0.0059 y 0.12
– F recx = valor aletorio entre 29.0 y 31.0
– Ampy = valor aletorio entre 0.0041 y 0.11
– F recy = valor aletorio entre 59.0 y 61.0
– Ampz = valor aletorio entre 0.008 y 0.15
– F recz = valor aletorio entre 89.0 y 91.0
– RMS =
q
(Amp2
x + Amp2
y + Amp2
z
)
*/

int Acelerometer_kpi(){

}

