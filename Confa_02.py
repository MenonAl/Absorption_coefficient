
import random
import numpy as np
import math
import pandas as pd

# print(math.exp(2))
# Spectrum = open("SpectrMol.txt")

with open("SpectrMol.txt", "r") as file:
    Spectrumline = file.readlines()

Spectrumline_Exponent = []
Spectrumline_wave_number = []
Spectrumline_Coef_Value = []
Spectrumline_Long = []

Spectrumline_Plank = []
Spectrumline_Plank_Exponent = []

surface_temperature = int(input("surface_temperature ="))           #296
surface_concentration = float(input("surface_concentration ="))       #4.2 * 10 ** 13
delta_temperature = float(input("delta_temperature =")) #-6.5 * 10 ** (-2)
count = 1

Atmosphere_concentration = surface_concentration
Atmosphere_temperature = []

concentration = float(input("concentration ="))
molecule_mass = float(input("molecule_mass ="))#7.3 * 10 ** (-26)

length = 10 ** 6

c = 3 * 10 ** 8
k = 1.38 * 10 ** (-23)
h = 6.626 * 10 ** (-34)
g = 9.81

for i in range(0, len(Spectrumline) - 1):
    Spectrumline_Plank_Exponent.append(0)
    Spectrumline_Plank.append(0)

def value():
    with open('info_value.txt', 'w', encoding='UTF-8') as outfile:
        for i in range(0, len(Spectrumline) - 1):
            Spectrumline_Coef_Value.append(float(Spectrumline[i][16:28]))

            print(Spectrumline[i][16:28], file=outfile)


def wave_number():
    with open('info_wave_number.txt', 'w', encoding='UTF-8') as outfile:
        for i in range(0, len(Spectrumline) - 1):
            Spectrumline_wave_number.append(float(Spectrumline[i][1:12]))

            print(Spectrumline_wave_number[i], file=outfile)


def exponent_value():
    with open('info_exponent_value.txt', 'w', encoding='UTF-8') as outfile:
        for i in range(0, len(Spectrumline) - 1):
            Spectrumline_Exponent.append(float(Spectrumline[i][29:32]))

            print(Spectrumline_Exponent[i], file=outfile)


def long():
    with open('info_long.txt', 'w', encoding='UTF-8') as outfile:
        for i in range(0, len(Spectrumline) - 1):
            Spectrumline_Long.append(1 / float(Spectrumline_wave_number[i]) * 10 ** 4)

            print(Spectrumline_Long[i], file=outfile)


def plank():
    with open('info_plank.txt', 'w', encoding='UTF-8') as outfile:
        for i in range(0, len(Spectrumline) - 1):
            value_01 = (2 * math.pi * c ** 2 * h) / (Spectrumline_Long[i] * 10 ** (-6)) ** 5
            value_02 = 1 / (math.exp(h * c / (Spectrumline_Long[i] * 10 ** (-6) * k * surface_temperature)) - 1)

            value = value_01 * value_02

            Spectrumline_Plank[i] = value

            print(Spectrumline_Plank[i], file = outfile)

        print('100%')


def plank_exponent():
    global count
    with open('info_plank_exponent.txt', 'w', encoding='UTF-8') as outfile:

        for i in range(0, len(Spectrumline) - 1):

            exp_coef =  length * Atmosphere_concentration * Spectrumline_Coef_Value[i] * 10 ** Spectrumline_Exponent[i]

            if exp_coef > 100:

                Spectrumline_Plank_Exponent[i] = 0

            else:

                Spectrumline_Plank_Exponent[i] = Spectrumline_Plank[i] / math.exp(exp_coef)
                #print(exp_coef)
            if count == 1:

                print(Spectrumline_Plank_Exponent[i], file=outfile)



def layer_temperature():
    with open('info_layer_temperature', 'w', encoding='UTF-8') as outfile:
        for i in range(0, 1000):
            Atmosphere_temperature.append(surface_temperature + delta_temperature * i)

            print(Atmosphere_temperature[i], file=outfile)

    return 0


def gas_concentration():
    global count, Atmosphere_concentration
    with open('info_pressure.txt', 'w', encoding='UTF-8') as outfile:

        value()

        wave_number()

        exponent_value()

        long()

        plank()

        layer_temperature()

        for i in range(0, 1000):

            Atmosphere_concentration = Atmosphere_concentration * math.exp(-molecule_mass * g * 10/ (k * Atmosphere_temperature[i]))
            #print(Atmosphere_concentration)
            #print(surface_concentration * math.exp(-molecule_mass * g * 10/ (k * Atmosphere_temperature[i])))
            percent = i/10

            print(str(percent) + '%')

            if i == 999:

                count = 1

                plank_exponent()

            else:

                plank_exponent()

                for i in range(0, len(Spectrumline) - 1):
                    Spectrumline_Plank[i] = Spectrumline_Plank_Exponent[i]

            # print (Atmosphere_concentration, file = outfile)
    return 0


def koef ():

    summ_exp = 0
    summ_plank = 0
    for i in range (0,len(Spectrumline)-1):

        summ_exp+=Spectrumline_Plank_Exponent[i]
        summ_plank+=Spectrumline_Plank[i]

    print("k = " + str(1-summ_exp/(summ_plank)))


#gas_concentration()

value()

wave_number()

exponent_value()

long()

plank()

plank_exponent()

koef()