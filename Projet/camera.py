import picamera
import time
import os
from datetime import datetime

########## A modifier avant de lancer le programme ###########################
# nom+adresse ip de l'ordinateur de l'utilisateur
# le path qui indique où sont stockés les fichiers sur l'ordinateur
userip="lenaisdesbos@192.168.251.36"
path="/Users/lenaisdesbos/Documents/projetRas/"


# allumer la caméra
camera = picamera.PiCamera()
camera.start_preview()
# si la caméra est mal posée : camera.rotation = 180

# Début vidéo (filmé pendant 10 secondes)
camera.start_recording('Video/video.h264')
time.sleep(10)
# Fin vidéo
camera.stop_recording()
# Eteindre la caméra
camera.stop_preview()

# convertir la vidéo en MP4
os.system('MP4Box -add Video/video.h264 Video/video.mp4')
# attendre 2 secondes pour être sûr que la conversion de l'extension est finie
time.sleep(2)

# Supprimer la video en h264
os.system("rm Video/video.h264")

# on copie la vidéo sur l'ordinateur depuis la raspberry
# os.system("scp Video/video.mp4 "+userip+":/Users/lenaisdesbos/Documents/projetRas/video.mp4")
os.system("scp Video/video.mp4 "+userip+":"+path+"video.mp4")

# mettre à jour l'historique sur google drive
#os.system("ssh "+userip+" python3 /Users/lenaisdesbos/Documents/projetRas/csvDrive.py")
os.system("ssh "+userip+" python3 "+path+"csvDrive.py")

# envoiyer la vidéo sur google drive depuis l'ordinateur
#os.system("ssh "+userip+" python3 /Users/lenaisdesbos/Documents/projetRas/videoDrive.py")
os.system("ssh "+userip+" python3 "+path+"videoDrive.py")

# supprimer la vidéo qui est sur raspberry car on l'a déjà enregistrée sur drive 
os.system("rm ~/Projet/Video/video.mp4")