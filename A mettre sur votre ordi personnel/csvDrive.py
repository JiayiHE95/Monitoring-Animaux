from googlePratique import *
import csv

############# A modifier avant de lancer le programme #######################
# adresse ip de la Raspberry et 
# le path qui indique où sont stockés les fichiers sur l'ordinateur
ip="192.168.251.159"
path="/Users/lenaisdesbos/Documents/projetRas/"

#fonction qui crée un google sheet et renvoie son id
def creer_sheet(drive, sheet_name, folder):
    
    # une requête qui vérifie si google sheet qu'on veut créer existe
    query = "mimeType='application/vnd.google-apps.spreadsheet' and trashed=false and name='" + sheet_name + "'"
    results = drive.files().list(q=query,fields='files(id, name)').execute()
    sheet = results.get('files', [])
    
    #si le google sheet exite, on récupère son id
    if sheet:
        sheet_id = sheet[0]['id']
        return sheet_id
    
    #sinon, on le crée
    else:
        body = {
        'mimeType': 'application/vnd.google-apps.spreadsheet',
        'name': sheet_name,
        }
        # vérifie si on souhaite créer le sheet dans un dossier indiqué
        if folder:
            body['parents']=[folder]
        sheet_file=drive.files().create(body=body).execute()
        sheet_id = sheet_file.get('id')
        return sheet_id
       

#fonction qui enregistre les actions passées sur raspberry
#def writeCsv(action):
    #récupère l'heure actuelle
    #date=str(datetime.now())
    #ecrire les actions passées sur raspberry
    #fichier = open("historiqueActions.csv", "a+", newline='') 
    #writer = csv.writer(fichier,delimiter=";")
    #writer.writerow([date,action])
    #fichier.close()   


#fonction qui permet d'ecrire directement sur google sheet
def ecrire_sheet(sheet, sheet_id, range_name, value_input_option, values):
    result = sheet.spreadsheets().values().batchGet(spreadsheetId=sheet_id, ranges="A1:B1").execute()
    ranges = result.get('valueRanges', [])
    # si c'est un nouveau sheet, on va le configurer en mettant
    if 'values' not in ranges[0]:
        attributs=[["date","action"]]
        sheet.spreadsheets().values().append(spreadsheetId=sheet_id, 
                                                  range=range_name,
                                                  valueInputOption=value_input_option, 
                                                  body={'values': attributs}).execute()
        print("fichier Historique configurée")
        
    result = sheet.spreadsheets().values().append(spreadsheetId=sheet_id, 
                                                  range=range_name,
                                                  valueInputOption=value_input_option, 
                                                  body={'values': values}).execute()
    print(f"{(result.get('updates').get('updatedCells'))} informations ajoutées.")
    
    return result


#fonction qui récupère les données d'un scv, les enregistrer localement et sur drive 
def readCsvAndSend(sheet, sheet_id):
    #copier le csv depuis raspberry
    #os.system("scp pi@"+ip+":~/Projet/historiqueActions.csv /Users/lenaisdesbos/Documents/projetRas/")
    os.system("scp pi@"+ip+":~/Projet/historiqueActions.csv "+path)
    
    #supprimer le csv du raspberry
    os.system("ssh pi@"+ip+" rm /home/pi/Projet/historiqueActions.csv")
    
    #creer un csv historique s'il existe pas
    fichier= open("historique.csv", "a+", newline='')
    writer = csv.writer(fichier,delimiter=";")
    reader = csv.reader(fichier,delimiter=";")
  
    #lire le csv récupéré depuis raspberry
    #fichierTemp = open("/Users/lenaisdesbos/Documents/projetRas/historiqueActions.csv", "r", newline='')
    fichierTemp = open(path+"historiqueActions.csv", "r", newline='')
    reader = csv.reader(fichierTemp,delimiter=";")
    for ligne in reader:
        #Enregistrement local dans csv historique
        writer.writerow(ligne)
        #Enregistrement dans Google sheet
        ecrire_sheet(sheet, sheet_id, "A1:B1", "USER_ENTERED", [ligne])

    fichierTemp.close()
    fichier.close()
    
    #supprimer le csv temporaire historiqueActions
    #os.system("rm /Users/lenaisdesbos/Documents/projetRas/historiqueActions.csv")
    os.system("rm "+path+"historiqueActions.csv")
    

#connecter au google drive et creer un dossier
drive=connexion("drive", SCOPES_DRIVE)
folder=createFolder_drive(drive,"Monitoring-Animaux")

#Accéder au google sheet et creer un csv s'il exite pas
sheet=connexion("sheet", SCOPES_SHEET)
sheet_id=creer_sheet(drive,"historique", folder)

readCsvAndSend(sheet, sheet_id)