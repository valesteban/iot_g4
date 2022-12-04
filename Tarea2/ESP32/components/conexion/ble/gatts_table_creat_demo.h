/*
 * SPDX-FileCopyrightText: 2021 Espressif Systems (Shanghai) CO LTD
 *
 * SPDX-License-Identifier: Unlicense OR CC0-1.0
 */


// #include <stdio.h>
// #include <stdlib.h>
// #include <string.h>


/* Attributes State Machine */
enum
{
    IDX_SVC,            // SERVICIO
    IDX_CHAR_A,         //CARACTERISTICA   ---> 3  caracteristicas  para A   ----> TITULO   (solo se lee)
    IDX_CHAR_VAL_A,     //CARACTERISTICA                                     ----> Valor
    IDX_CHAR_CFG_A,     //CARACTERISTICA                                     ----> configuracion (escribible)

    IDX_CHAR_B,         //CARACTERISTICA   ---> 2 caracteristicas para  B
    IDX_CHAR_VAL_B,     //CARACTERISTICA

    IDX_CHAR_C,         //CARACTERISTICA   ---> 2 caracteristicas para C
    IDX_CHAR_VAL_C,     //CARACTERISTICA

    HRS_IDX_NB,
};

// LA FORMA DEL SERVICIO (PERFIL SERVICIO)
