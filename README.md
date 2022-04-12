# TrackingRobot
Jest to projekt robota mającego na celu śledzenie człowieka. <br />
Cały kod napisany został z myślą o knstrukcji robota opartego na Raspberry Pi z podłączoną kamerką. <br />
Całość sterowania została zaprojektowana z myślą o konstukcji z sterownikiem L298, który reguluje pracę dwóch silników DC. <br />
Autorzy: Ernest Torz, Patrycja Kałużna, Jacek Ziętek, Piotr Czekaj
<br /> 
<br />
# Instrukcja
W celu uruchomienia programu, należy pobrać projekt, a następnie:
1) Pobrać wirtualne środowisko (jeśli takowe nie jest pobrane), poleceniem: sudo pip3 install virtualenv 
2) Stworzyć środowisko poleceniem: python3 -m venv nazwa_srodowiska 
3) Uruchomić środowisko poleceniem: source nazwa_srodowiska/bin/activate 
4) Pobrać potrzebne biblioteki poleceniem: bash requierments.sh 
5) Uruchomić program poleceniem: python3 main.py --modeldir Sample_TFlite_model/
<br/>

