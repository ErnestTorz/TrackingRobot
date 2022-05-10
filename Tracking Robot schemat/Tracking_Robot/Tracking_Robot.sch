EESchema Schematic File Version 4
EELAYER 30 0
EELAYER END
$Descr A4 11693 8268
encoding utf-8
Sheet 1 1
Title "Tracking Robot"
Date "2022-05-10"
Rev ""
Comp ""
Comment1 "Ernest Torz"
Comment2 "Patrycja Kałużna"
Comment3 "Piotr Czekaj"
Comment4 "Jacek Ziętek"
$EndDescr
$Comp
L Connector:Raspberry_Pi_2_3 J1
U 1 1 627A6421
P 1725 5725
F 0 "J1" H 1825 7300 50  0000 C CNN
F 1 "Raspberry_Pi_4B" H 1875 7125 50  0000 C CNN
F 2 "" H 1725 5725 50  0001 C CNN
F 3 "https://www.raspberrypi.org/documentation/hardware/raspberrypi/schematics/rpi_SCH_3bplus_1p0_reduced.pdf" H 1725 5725 50  0001 C CNN
	1    1725 5725
	1    0    0    -1  
$EndComp
$Comp
L Driver_Motor:L298HN U2
U 1 1 627AB8B8
P 6425 3075
F 0 "U2" H 6425 3956 50  0000 C CNN
F 1 "L298HN" H 6425 3865 50  0000 C CNN
F 2 "Package_TO_SOT_THT:TO-220-15_P2.54x2.54mm_StaggerOdd_Lead4.58mm_Vertical" H 6475 2425 50  0001 L CNN
F 3 "http://www.st.com/st-web-ui/static/active/en/resource/technical/document/datasheet/CD00000240.pdf" H 6575 3325 50  0001 C CNN
	1    6425 3075
	1    0    0    -1  
$EndComp
$Comp
L Simulation_SPICE:DIODE D3
U 1 1 627AD5B8
P 7325 3525
F 0 "D3" V 7371 3445 50  0000 R CNN
F 1 "1N4007" V 7280 3445 50  0000 R CNN
F 2 "" H 7325 3525 50  0001 C CNN
F 3 "~" H 7325 3525 50  0001 C CNN
F 4 "Y" H 7325 3525 50  0001 L CNN "Spice_Netlist_Enabled"
F 5 "D" H 7325 3525 50  0001 L CNN "Spice_Primitive"
	1    7325 3525
	0    -1   -1   0   
$EndComp
$Comp
L Simulation_SPICE:DIODE D5
U 1 1 627B1946
P 7925 3525
F 0 "D5" V 7971 3445 50  0000 R CNN
F 1 "1N4007" V 7880 3445 50  0000 R CNN
F 2 "" H 7925 3525 50  0001 C CNN
F 3 "~" H 7925 3525 50  0001 C CNN
F 4 "Y" H 7925 3525 50  0001 L CNN "Spice_Netlist_Enabled"
F 5 "D" H 7925 3525 50  0001 L CNN "Spice_Primitive"
	1    7925 3525
	0    -1   -1   0   
$EndComp
$Comp
L Simulation_SPICE:DIODE D7
U 1 1 627B20AE
P 8500 3525
F 0 "D7" V 8546 3445 50  0000 R CNN
F 1 "1N4007" V 8455 3445 50  0000 R CNN
F 2 "" H 8500 3525 50  0001 C CNN
F 3 "~" H 8500 3525 50  0001 C CNN
F 4 "Y" H 8500 3525 50  0001 L CNN "Spice_Netlist_Enabled"
F 5 "D" H 8500 3525 50  0001 L CNN "Spice_Primitive"
	1    8500 3525
	0    -1   -1   0   
$EndComp
$Comp
L Simulation_SPICE:DIODE D9
U 1 1 627B2DA9
P 9025 3525
F 0 "D9" V 9071 3445 50  0000 R CNN
F 1 "1N4007" V 8980 3445 50  0000 R CNN
F 2 "" H 9025 3525 50  0001 C CNN
F 3 "~" H 9025 3525 50  0001 C CNN
F 4 "Y" H 9025 3525 50  0001 L CNN "Spice_Netlist_Enabled"
F 5 "D" H 9025 3525 50  0001 L CNN "Spice_Primitive"
	1    9025 3525
	0    -1   -1   0   
$EndComp
$Comp
L Simulation_SPICE:DIODE D2
U 1 1 627BA3B5
P 7325 2175
F 0 "D2" V 7371 2095 50  0000 R CNN
F 1 "1N4007" V 7280 2095 50  0000 R CNN
F 2 "" H 7325 2175 50  0001 C CNN
F 3 "~" H 7325 2175 50  0001 C CNN
F 4 "Y" H 7325 2175 50  0001 L CNN "Spice_Netlist_Enabled"
F 5 "D" H 7325 2175 50  0001 L CNN "Spice_Primitive"
	1    7325 2175
	0    -1   -1   0   
$EndComp
$Comp
L Simulation_SPICE:DIODE D4
U 1 1 627BA3BD
P 7925 2175
F 0 "D4" V 7971 2095 50  0000 R CNN
F 1 "1N4007" V 7880 2095 50  0000 R CNN
F 2 "" H 7925 2175 50  0001 C CNN
F 3 "~" H 7925 2175 50  0001 C CNN
F 4 "Y" H 7925 2175 50  0001 L CNN "Spice_Netlist_Enabled"
F 5 "D" H 7925 2175 50  0001 L CNN "Spice_Primitive"
	1    7925 2175
	0    -1   -1   0   
$EndComp
$Comp
L Simulation_SPICE:DIODE D6
U 1 1 627BA3C5
P 8500 2175
F 0 "D6" V 8546 2095 50  0000 R CNN
F 1 "1N4007" V 8455 2095 50  0000 R CNN
F 2 "" H 8500 2175 50  0001 C CNN
F 3 "~" H 8500 2175 50  0001 C CNN
F 4 "Y" H 8500 2175 50  0001 L CNN "Spice_Netlist_Enabled"
F 5 "D" H 8500 2175 50  0001 L CNN "Spice_Primitive"
	1    8500 2175
	0    -1   -1   0   
$EndComp
$Comp
L Simulation_SPICE:DIODE D8
U 1 1 627BA3CD
P 9025 2175
F 0 "D8" V 9071 2095 50  0000 R CNN
F 1 "1N4007" V 8980 2095 50  0000 R CNN
F 2 "" H 9025 2175 50  0001 C CNN
F 3 "~" H 9025 2175 50  0001 C CNN
F 4 "Y" H 9025 2175 50  0001 L CNN "Spice_Netlist_Enabled"
F 5 "D" H 9025 2175 50  0001 L CNN "Spice_Primitive"
	1    9025 2175
	0    -1   -1   0   
$EndComp
$Comp
L Motor:Motor_DC M1
U 1 1 627BEE17
P 10575 2200
F 0 "M1" V 10281 2150 50  0000 C CNN
F 1 "Motor_DC" V 10372 2150 50  0000 C CNN
F 2 "" V 10606 2143 50  0001 C CNN
F 3 "~" V 10606 2143 50  0001 C CNN
	1    10575 2200
	0    1    1    0   
$EndComp
$Comp
L power:GND #PWR06
U 1 1 627D638A
P 6425 3950
F 0 "#PWR06" H 6425 3700 50  0001 C CNN
F 1 "GND" H 6430 3777 50  0000 C CNN
F 2 "" H 6425 3950 50  0001 C CNN
F 3 "" H 6425 3950 50  0001 C CNN
	1    6425 3950
	1    0    0    -1  
$EndComp
Wire Wire Line
	6125 3775 6125 3900
Wire Wire Line
	6125 3900 6225 3900
Wire Wire Line
	6425 3900 6425 3950
Wire Wire Line
	6225 3775 6225 3900
Connection ~ 6225 3900
Wire Wire Line
	6225 3900 6425 3900
Connection ~ 6425 3900
Wire Wire Line
	6425 3775 6425 3900
Wire Wire Line
	9025 3675 9025 3900
Wire Wire Line
	9025 3900 8500 3900
Wire Wire Line
	8500 3675 8500 3900
Connection ~ 8500 3900
Wire Wire Line
	7925 3675 7925 3900
Connection ~ 7925 3900
Wire Wire Line
	7925 3900 8500 3900
Wire Wire Line
	7325 3675 7325 3900
Wire Wire Line
	7325 3900 7925 3900
Wire Wire Line
	9025 2025 8500 2025
Wire Wire Line
	8500 2025 7925 2025
Connection ~ 8500 2025
Wire Wire Line
	7925 2025 7325 2025
Connection ~ 7925 2025
Wire Wire Line
	6525 2375 6525 2025
Wire Wire Line
	7325 2325 7325 2425
Wire Wire Line
	8500 2325 8500 2950
Wire Wire Line
	9475 2425 7325 2425
Connection ~ 7325 2425
Connection ~ 8500 2950
Wire Wire Line
	8500 2950 9500 2950
$Comp
L Connector:Screw_Terminal_01x02 J4
U 1 1 627E67A8
P 9675 2425
F 0 "J4" H 9755 2417 50  0000 L CNN
F 1 "Screw_Terminal_01x02" H 9755 2326 50  0000 L CNN
F 2 "" H 9675 2425 50  0001 C CNN
F 3 "~" H 9675 2425 50  0001 C CNN
	1    9675 2425
	1    0    0    -1  
$EndComp
Text GLabel 9125 2425 3    50   Input ~ 0
M1+
Text GLabel 9425 2525 3    50   Input ~ 0
M1-
Text GLabel 10275 2200 0    50   Input ~ 0
M1+
Text GLabel 10775 2200 2    50   Input ~ 0
M1-
$Comp
L Motor:Motor_DC M2
U 1 1 627EED97
P 10600 3475
F 0 "M2" V 10306 3425 50  0000 C CNN
F 1 "Motor_DC" V 10397 3425 50  0000 C CNN
F 2 "" V 10631 3418 50  0001 C CNN
F 3 "~" V 10631 3418 50  0001 C CNN
	1    10600 3475
	0    1    1    0   
$EndComp
Text GLabel 10300 3475 0    50   Input ~ 0
M2+
Text GLabel 10800 3475 2    50   Input ~ 0
M2-
$Comp
L Connector:Screw_Terminal_01x02 J5
U 1 1 627F08D0
P 9700 2950
F 0 "J5" H 9780 2942 50  0000 L CNN
F 1 "Screw_Terminal_01x02" H 9780 2851 50  0000 L CNN
F 2 "" H 9700 2950 50  0001 C CNN
F 3 "~" H 9700 2950 50  0001 C CNN
	1    9700 2950
	1    0    0    -1  
$EndComp
Text GLabel 9150 2950 3    50   Input ~ 0
M2+
Text GLabel 9375 3050 3    50   Input ~ 0
M2-
Wire Wire Line
	5725 3075 5725 4650
Wire Wire Line
	5725 4650 5600 4650
Wire Wire Line
	5500 4650 5500 2975
Wire Wire Line
	5300 4650 5175 4650
Wire Wire Line
	5175 4650 5175 2575
Wire Wire Line
	9025 2325 9025 3050
Wire Wire Line
	7925 2325 7925 2525
Wire Wire Line
	7325 2025 6525 2025
Connection ~ 7325 2025
Wire Wire Line
	7025 2875 7325 2875
Connection ~ 7325 2875
Wire Wire Line
	7325 2875 7325 3375
Wire Wire Line
	7025 2975 7925 2975
Connection ~ 7925 2975
Wire Wire Line
	7925 2975 7925 3375
Wire Wire Line
	7025 3175 8500 3175
Connection ~ 8500 3175
Wire Wire Line
	8500 3175 8500 3375
Wire Wire Line
	7025 3275 9025 3275
Connection ~ 9025 3275
Wire Wire Line
	9025 3275 9025 3375
Wire Wire Line
	7325 2425 7325 2875
Wire Wire Line
	7925 2525 9475 2525
Connection ~ 7925 2525
Wire Wire Line
	7925 2525 7925 2975
Wire Wire Line
	8500 2950 8500 3175
Wire Wire Line
	9025 3050 9500 3050
Connection ~ 9025 3050
Wire Wire Line
	9025 3050 9025 3275
Wire Wire Line
	5825 3075 5725 3075
Wire Wire Line
	5500 2975 5825 2975
Wire Wire Line
	5825 2675 5400 2675
Wire Wire Line
	5400 2675 5400 4650
Wire Wire Line
	5825 2575 5175 2575
$Comp
L Device:Jumper_NO_Small JP2
U 1 1 6281906A
P 4825 2775
F 0 "JP2" H 4825 2960 50  0000 C CNN
F 1 "Jumper_NO" H 4825 2869 50  0000 C CNN
F 2 "" H 4825 2775 50  0001 C CNN
F 3 "~" H 4825 2775 50  0001 C CNN
	1    4825 2775
	1    0    0    -1  
$EndComp
Text GLabel 925  5625 0    50   Input ~ 0
IN1
Text GLabel 925  5725 0    50   Input ~ 0
EnA
Text GLabel 925  6325 0    50   Input ~ 0
IN3
Text GLabel 925  5525 0    50   Input ~ 0
IN4
Text GLabel 925  5125 0    50   Input ~ 0
IN2
Text GLabel 2525 6525 2    50   Input ~ 0
EnB
Wire Wire Line
	7325 3900 6425 3900
Connection ~ 7325 3900
$Comp
L power:+5V #PWR01
U 1 1 6281CFE2
P 1525 3875
F 0 "#PWR01" H 1525 3725 50  0001 C CNN
F 1 "+5V" H 1540 4048 50  0000 C CNN
F 2 "" H 1525 3875 50  0001 C CNN
F 3 "" H 1525 3875 50  0001 C CNN
	1    1525 3875
	1    0    0    -1  
$EndComp
Wire Wire Line
	1525 3875 1525 4425
$Comp
L power:GND #PWR02
U 1 1 628217B8
P 2025 7250
F 0 "#PWR02" H 2025 7000 50  0001 C CNN
F 1 "GND" H 2030 7077 50  0000 C CNN
F 2 "" H 2025 7250 50  0001 C CNN
F 3 "" H 2025 7250 50  0001 C CNN
	1    2025 7250
	1    0    0    -1  
$EndComp
$Comp
L power:+12V #PWR03
U 1 1 62824489
P 3275 2425
F 0 "#PWR03" H 3275 2275 50  0001 C CNN
F 1 "+12V" H 3290 2598 50  0000 C CNN
F 2 "" H 3275 2425 50  0001 C CNN
F 3 "" H 3275 2425 50  0001 C CNN
	1    3275 2425
	-1   0    0    1   
$EndComp
Wire Wire Line
	5825 2775 4925 2775
$Comp
L Device:Jumper_NO_Small JP3
U 1 1 62827035
P 4825 3175
F 0 "JP3" H 4825 3360 50  0000 C CNN
F 1 "Jumper_NO" H 4825 3269 50  0000 C CNN
F 2 "" H 4825 3175 50  0001 C CNN
F 3 "~" H 4825 3175 50  0001 C CNN
	1    4825 3175
	1    0    0    -1  
$EndComp
Wire Wire Line
	5825 3175 4925 3175
Wire Wire Line
	4725 2775 4725 2975
Text GLabel 5025 3175 3    50   Input ~ 0
EnB
Text GLabel 5025 2775 3    50   Input ~ 0
EnA
Wire Wire Line
	6425 2375 4425 2375
Wire Wire Line
	4425 2375 4425 2975
Wire Wire Line
	4425 2975 4725 2975
Connection ~ 4725 2975
Wire Wire Line
	4725 2975 4725 3175
$Comp
L Device:R R1
U 1 1 6282D48C
P 4425 3400
F 0 "R1" H 4495 3446 50  0000 L CNN
F 1 "1K" H 4495 3355 50  0000 L CNN
F 2 "" V 4355 3400 50  0001 C CNN
F 3 "~" H 4425 3400 50  0001 C CNN
	1    4425 3400
	1    0    0    -1  
$EndComp
$Comp
L Device:LED D1
U 1 1 6282E576
P 4425 3700
F 0 "D1" V 4464 3582 50  0000 R CNN
F 1 "LED" V 4373 3582 50  0000 R CNN
F 2 "" H 4425 3700 50  0001 C CNN
F 3 "~" H 4425 3700 50  0001 C CNN
	1    4425 3700
	0    -1   -1   0   
$EndComp
Wire Wire Line
	4425 2975 4425 3250
Connection ~ 4425 2975
$Comp
L Device:CP C2
U 1 1 62831C98
P 4025 3400
F 0 "C2" H 4143 3446 50  0000 L CNN
F 1 "220uF" H 4143 3355 50  0000 L CNN
F 2 "" H 4063 3250 50  0001 C CNN
F 3 "~" H 4025 3400 50  0001 C CNN
	1    4025 3400
	1    0    0    -1  
$EndComp
$Comp
L Regulator_Linear:KA78M05_TO252 U1
U 1 1 62833180
P 3450 2975
F 0 "U1" H 3450 3217 50  0000 C CNN
F 1 "78M05" H 3450 3126 50  0000 C CNN
F 2 "Package_TO_SOT_SMD:TO-252-2" H 3450 3200 50  0001 C CIN
F 3 "https://www.onsemi.com/pub/Collateral/MC78M00-D.PDF" H 3450 2925 50  0001 C CNN
	1    3450 2975
	1    0    0    -1  
$EndComp
Wire Wire Line
	4425 2975 4025 2975
Wire Wire Line
	4025 3250 4025 2975
Connection ~ 4025 2975
Wire Wire Line
	4025 2975 3750 2975
Wire Wire Line
	3450 3275 3450 3850
Wire Wire Line
	4025 3550 4025 3850
Connection ~ 4025 3850
Wire Wire Line
	4025 3850 4425 3850
Connection ~ 3450 3850
$Comp
L Device:Jumper_NC_Small JP1
U 1 1 628462B9
P 2800 2975
F 0 "JP1" H 2800 3187 50  0000 C CNN
F 1 "Jumper_NC" H 2800 3096 50  0000 C CNN
F 2 "" H 2800 2975 50  0001 C CNN
F 3 "~" H 2800 2975 50  0001 C CNN
	1    2800 2975
	1    0    0    -1  
$EndComp
Wire Wire Line
	3150 2975 2900 2975
$Comp
L Device:CP C1
U 1 1 62849925
P 2700 3400
F 0 "C1" H 2818 3446 50  0000 L CNN
F 1 "220uF" H 2818 3355 50  0000 L CNN
F 2 "" H 2738 3250 50  0001 C CNN
F 3 "~" H 2700 3400 50  0001 C CNN
	1    2700 3400
	1    0    0    -1  
$EndComp
Wire Wire Line
	3450 3850 2700 3850
Wire Wire Line
	2700 3850 2700 3550
Wire Wire Line
	2700 3250 2700 2975
$Comp
L Connector:Screw_Terminal_01x03 J2
U 1 1 6284ECBA
P 3450 2075
F 0 "J2" V 3414 1887 50  0000 R CNN
F 1 "Screw_Terminal_01x03" V 3323 1887 50  0000 R CNN
F 2 "" H 3450 2075 50  0001 C CNN
F 3 "~" H 3450 2075 50  0001 C CNN
	1    3450 2075
	0    -1   -1   0   
$EndComp
$Comp
L power:GND #PWR04
U 1 1 6285B9FA
P 3450 2425
F 0 "#PWR04" H 3450 2175 50  0001 C CNN
F 1 "GND" H 3455 2252 50  0000 C CNN
F 2 "" H 3450 2425 50  0001 C CNN
F 3 "" H 3450 2425 50  0001 C CNN
	1    3450 2425
	1    0    0    -1  
$EndComp
Wire Wire Line
	3450 2275 3450 2425
Wire Wire Line
	3450 3850 4025 3850
Wire Wire Line
	2025 7025 2025 7250
$Comp
L power:GND #PWR05
U 1 1 6285E0F8
P 3450 4100
F 0 "#PWR05" H 3450 3850 50  0001 C CNN
F 1 "GND" H 3455 3927 50  0000 C CNN
F 2 "" H 3450 4100 50  0001 C CNN
F 3 "" H 3450 4100 50  0001 C CNN
	1    3450 4100
	1    0    0    -1  
$EndComp
Wire Wire Line
	3450 3850 3450 4100
Wire Wire Line
	2700 2275 2700 2975
Connection ~ 2700 2975
Wire Wire Line
	3550 2275 4425 2275
Wire Wire Line
	4425 2275 4425 2375
Connection ~ 4425 2375
Wire Wire Line
	6525 2025 5500 2025
Wire Wire Line
	5500 2025 5500 1775
Connection ~ 6525 2025
Wire Wire Line
	2700 1775 2700 2275
Connection ~ 2700 2275
Wire Wire Line
	2700 1775 5500 1775
Wire Wire Line
	2700 2275 3275 2275
Wire Wire Line
	3275 2425 3275 2275
Connection ~ 3275 2275
Wire Wire Line
	3275 2275 3350 2275
Text GLabel 5175 4400 0    50   Input ~ 0
IN1
Text GLabel 5400 4400 0    50   Input ~ 0
IN2
Text GLabel 5500 4400 2    50   Input ~ 0
IN3
Text GLabel 5725 4400 2    50   Input ~ 0
IN4
$Comp
L Connector:Conn_01x04_Male J3
U 1 1 62876127
P 5400 4850
F 0 "J3" V 5554 4562 50  0000 R CNN
F 1 "Conn_01x04_Male" V 5463 4562 50  0000 R CNN
F 2 "" H 5400 4850 50  0001 C CNN
F 3 "~" H 5400 4850 50  0001 C CNN
	1    5400 4850
	0    -1   -1   0   
$EndComp
$EndSCHEMATC
