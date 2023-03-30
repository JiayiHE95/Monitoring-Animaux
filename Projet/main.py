import threading
import time
import grovepi
import os
import csv
from datetime import datetime
import threading

# Connect to analog port
sound_sensor = 0
# Connect to digital port
water_sensor = 2
button = 3
relay = 4
led = 5

grovepi.pinMode(water_sensor,"INPUT")
grovepi.pinMode(button,"INPUT")
grovepi.pinMode(sound_sensor,"INPUT")
grovepi.pinMode(led,"OUTPUT")
cmd = "omxplayer -p -o local son.mp3"

# la volume à partir de la quelle on considère que le son est un bruit pour lancer la caméra
# A vous de modifier cette valeur
threshold_value = 300

#fonction qui enregistre les actions passées sur raspberry
def writeCsv(action):
    #récupère l'heure actuelle
    date=str(datetime.now())
    #ecrire les actions passées sur raspberry
    fichier = open("historiqueActions.csv", "a+", newline='') 
    writer = csv.writer(fichier,delimiter=";")
    writer.writerow([date,action])
    fichier.close()

# class thread pour bouton et haut-parleur
class MonThread1 (threading.Thread):
    def __init__(self, s):
        threading.Thread.__init__(self)
        self.s = s

    def run(self):
        i = 0
        while True:
            #comme le tempps d'arrêt est très petit, on limite l'affichage à une fois toute les 10 boucles pour ne pas surcharger le terminal
            if i%10==0:
                print("thread ", self.s, " : ", i)
            i+=1
            try:
                if grovepi.digitalRead(button)==1: #si on appuie sur le bouton
                    os.system(cmd) #on lance la commande pour faire passer le son
                    writeCsv("appuie bouton") #on enregistre l'action sur le fichier
                time.sleep(0.1) #on fait une pose très petite pour que le bouton réagisse dès qu'on appuie dessus

            except IOError:
                print ("Error")
                writeCsv("erreur bouton ou haut-parleur") #on enregistre l'erreur dans le fichier

# class thread pour capteur eau et pompe
class MonThread2 (threading.Thread):
    def __init__(self, s):
        threading.Thread.__init__(self)
        self.s = s

    def run(self):
        i = 0
        while True:
            print("thread ", self.s, " : ", i)
            i+=1
            try:
                if grovepi.digitalRead(water_sensor)==0: #si le capteur est mouillé
                    grovepi.digitalWrite(relay,0) #la pompe s'éteint (led relais éteinte)
                    time.sleep(60) #on fait une pause d'une minute, pas besoin de vérifier plus souvent lorsque le capteur et déjà mouillé (ça ne pourra pas déborder), en 1 minute, l'animal ne peut pas s'assoiffer
                else: # sinon (si le capteur est sec)
                    grovepi.digitalWrite(relay,1) #la pompe se met en marche (led relais allumée)
                    print("pompe allumée")
                    
                    writeCsv("mise en route de la pompe") #on enregistre l'action sur le fichier
                    time.sleep(1) #on fait une pause de seulement une seconde pour que la gamelle ne déborde pas

            except KeyboardInterrupt:
                grovepi.digitalWrite(relay,0)
                writeCsv("interruption clavier capteur eau et pompe") #on enregistre l'interruption dans le fichier
                break
            except IOError:
                print ("Error")
                writeCsv("erreur capteur eau ou pompe") #on enregistre l'erreur dans le fichier

# class thread pour capteur son et camera
class MonThread3 (threading.Thread):
    def __init__(self, s):
        threading.Thread.__init__(self)
        self.s = s

    def run(self):
        i = 0
        while True:
            print("thread ", self.s, " : ", i)
            i+=1
            try:
                # On regarde le volume sonore
                sensor_value = grovepi.analogRead(sound_sensor)
                print("sensor_value = %d" %sensor_value)

                # Si il y a du bruit, on allume la caméra
                if sensor_value > threshold_value:
                    grovepi.digitalWrite(led,1) #la led s'allume pour indiquer que la caméra est en fonctionnement
                    os.system("python3 camera.py") #on appelle le fichier qui lance l'enregistrement de la caméra
                    writeCsv("enregistrement camera")
                    grovepi.digitalWrite(led,0) #on éteint la led pour indiquer que l'enregistrement est terminé

                time.sleep(.5) #on fait une pause très courte pour être sûr de ne rater aucun bruit

            except IOError:
                print ("Error")
                writeCsv("erreur capteur son ou camera") #on enregistre l'erreur dans le fichier

m = MonThread1("BoutonHP") # crée le premier thread
m.start()                    # démarre le thread

m2 = MonThread2("Water")  # crée un second thread
m2.start()                 # démarre le thread,

m3 = MonThread3("SoundCamera")  # crée un troisième thread
m3.start()                       # démarre le thread
