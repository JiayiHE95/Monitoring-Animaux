# import the required libraries
#import csv
import pickle
import os.path
from datetime import datetime
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from mimetypes import MimeTypes
from googleapiclient.http import MediaFileUpload

SCOPES_SHEET = ['https://www.googleapis.com/auth/spreadsheets']
SCOPES_DRIVE = ['https://www.googleapis.com/auth/drive']

############# A modifier avant de lancer le programme #######################
# le path qui indique où sont stockés les fichiers sur l'ordinateur
path="/Users/lenaisdesbos/Documents/projetRas/"

# fonction qui permet de connecter au google drive
def connexion(type, SCOPES):
    
    connexion=None
    # La variable creds stockera le jeton d'accès de l'utilisateur.
    # Si aucun token valide n'est trouvé, nous en créerons un.
    creds = None
  
    # Vérifier si le fichier token.pickle existe
    #if os.path.exists('/Users/lenaisdesbos/Documents/projetRas/token.pickle'):
    if os.path.exists(path+"token.pickle"):
  
        # Lire le token et le stocker dans la variable creds
        #with open('/Users/lenaisdesbos/Documents/projetRas/token.pickle', 'rb') as token:
        with open(path+"token.pickle", 'rb') as token:
            creds = pickle.load(token)
  
    # Si aucun justificatif d'identité valide n'est disponible, demandez à l'utilisateur de se connecter.
    if not creds or not creds.valid:
  
        # Si le token est expiré, il sera rafraîchi, sinon, nous en demanderons un nouveau.
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            #flow = InstalledAppFlow.from_client_secrets_file('/Users/lenaisdesbos/Documents/projetRas/key.json', SCOPES)
            flow = InstalledAppFlow.from_client_secrets_file(path+"key.json", SCOPES)
            creds = flow.run_local_server(port=0)
  
        # Sauvegarder le token d'accès dans le fichier token.pickle pour une utilisation future.
        # with open('/Users/lenaisdesbos/Documents/projetRas/token.pickle', 'wb') as token:
        with open(path+"token.pickle", 'wb') as token:
            pickle.dump(creds, token)
  
    # Connecter aux API service au choix
    if type=="drive":
        connexion = build('drive', 'v3', credentials=creds)
    elif type=="sheet": 
        connexion = build('sheets', 'v4', credentials=creds)
 
    return connexion


# fonction permet de créer un dossier avec un sous dossier donné (ou non)
def createFolder_drive(drive, folder_name, folder_parents=None):
    folder_id = None
    
    # vérifier si le dossier qu'on veut créer existe déjà 
    query = "mimeType='application/vnd.google-apps.folder' and trashed=false and name='" + folder_name + "'"
    results = drive.files().list(pageSize=1, q=query, fields="files(id, name)").execute()
    folders = results.get('files', [])
    
    #s'il exite, on récupère id de dossier
    if folders:
        folder_id = folders[0]['id']
        print("il existe déjà un dossier nommé " + folder_name)
        
    #sinon, on le crée
    else:
        file_metadata = {
                'name': folder_name,
                'mimeType': 'application/vnd.google-apps.folder'
            }
        if folder_parents :
            file_metadata['parents']=[folder_parents]
  
        folder_file = drive.files().create(body=file_metadata,fields='id').execute()
        folder_id = folder_file.get('id')
        print("Création d'un dossier nommé " + folder_name + " réussie")
        
    return folder_id
 



