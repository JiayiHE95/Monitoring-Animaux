from googlePratique import *

############# A modifier avant de lancer le programme #######################
# le path qui indique où sont stockés les fichiers sur l'ordinateur
path="/Users/lenaisdesbos/Documents/projetRas/"
    

#fonction qui va déposer une vidéo locale sur google drive
def videoUpload_drive(drive, filepath, folder=None):
          
    name = filepath.split('/')[-1]
      
    # Trouver le MimeType du fichier
    mimetype = MimeTypes().guess_type(name)[0]

    # génération du nom de la vidéo
    videoTime = str(datetime.now().date())+"-"+str(datetime.now().time())
    videoName = str(videoTime.split('.')[0])
    videoName = "video"+str(videoTime.split(':')[0])+"h"+str(videoTime.split(':')[1])+".mp4"

    file_metadata = {'name': videoName, 'parents': [folder]}
    media = MediaFileUpload(filepath, mimetype=mimetype)
      
    # Créer un nouveau fichier dans le stockage du lecteur
    drive.files().create(body=file_metadata, media_body=media, fields='id').execute()      
    print("Video déposée sur google drive réussie.")
    

#---------------- programme principale ----------------------

# connecter au google drive
drive=connexion("drive", SCOPES_DRIVE)
# creer un dossier sur google drive
folder=createFolder_drive(drive,"Monitoring-Animaux")

# creer un sous dossier
folder2=createFolder_drive(drive,"Enregistrements",folder)
# déposer la vidéo 
#videoUpload_drive(drive,'/Users/lenaisdesbos/Documents/projetRas/video.mp4', folder2)
videoUpload_drive(drive, path+"video.mp4", folder2)
