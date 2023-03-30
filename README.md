############### Monitoring Animaux ################

Jiayi HE, Lénaïs DESBOS, IG3 TD2

Avant de lancer le monitoring, il faut séparer les fichiers en deux endroits puis configurer certains fichiers.

######## Comment placer les fichiers ########
Sur Raspberry : mettre sous “/home/pi” le dossier “Projet”, dans lequel on trouve main.py, camera.py, son.mp3, historiqueAction.csv et un dossier “Video”. 
Sur l’ordinateur personnel, créer un dossier en y mettant : googlePratique.py, csvDrive.py, video.py, key.json, token.pickle


######## Changer les paramètres dans les fichiers ########
Le programme a besoin de l’adresse ip de Raspberry et l’adresse ip de l’ordinateur personnel pour pouvoir communiquer. Ainsi, on a besoin du path du dossier où on a placé les fichiers (sur l’ordinateur personnel) : 

camera.py : l’user et l’adresse ip de l’ordinateur personnel + le path 
videoDrive.py : le path
csvDrive.py : l’adresse ip de la Raspberry + le path
googlePratique.py : le path

Veuillez suivre les commentaires dans ces fichiers qui vous indiquent où et quoi modifier.


######## Pour lancer le programme ########
Il suffit de brancher la Raspberry.
Il se peut qu'il y aie un problème de connexion avec Google car le token est expiré, veuillez nous contacter ou suivre la section 3.4 du manuel utilisateur


######## Modules à importer sur la Raspberry ########
pip install picamera


######## Modules à importer sur l’ordinateur personnel (Python 3.7 ou +) ########
pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib


######## Pour accéder à Google Drive où sont stockées les vidéos et les actions réalisées ########
https://drive.google.com/drive/folders/1CLgc7_7KY1TpCy4FMC1lKvnhNmA4isGh
Si vous voulez stocker ces fichiers dans votre Drive personnel, veuillez nous donner votre adresse GMAIL ou suivre la section 3.4 du manuel utilisateur.

