# -*- coding:cp437 -*-
# WARNING : encodage pour Console DOS sous Windows uniquement !!!

# Direct Write (c) FRENCH TOUCH / Python 3
version="0.6 (09.2020)"

# Write a binary file directly to an Apple II image disk (DSK)
# Inputs (user or command line):
# - DSK image file
# - binary file
# - first track  (in Hexa WITHOUT 0x,$ or anything)
# - first sector (in Hexa WITHOUT 0x,$ or anything)
# - writing direction (increasing / decreasing sector) (+ or -)
# - Interleaving (D)os / (P)hysical / (F)ast Load
#
# Output:
# - modified DSK image file (warning: no backup!)

# Command line example: dw.py name.dsk binary.bin 0 A + d
# => write binary.bin to name.dsk from track $0, sector $A, upward direction with dos interleaving.

# All parameters (6) must be entered. There is no test performed on them.

import sys
import struct

if __name__ == '__main__':

    print()
    print("Direct Write",version)
    print(sys.argv)

    if len(sys.argv) < 7:
        nameDSK = input("Image disk name: ")
        nameBinary = input("Binary file name : ")
        track = int(input("First Track (Hexa) : "),16)
        sector = int(input("First Sector (Hexa) : "),16)
        sens = input("Direction (+/-) : ")
        interleaving = input("Interleaving (D/P/F) : ")
    else:    
        nameDSK = sys.argv[1]
        nameBinary = sys.argv[2]
        track = int(sys.argv[3],16)
        sector = int(sys.argv[4],16)
        sens = sys.argv[5]
        interleaving = sys.argv[6]

    if (interleaving == "p"):                   # physical interleaving (par rapport à un .dsk/.do)
        inter = [0x00,0x07,0x0E,0x06,0x0D,0x05,0x0C,0x04,0x0B,0x03,0x0A,0x02,0x09,0x01,0x08,0x0F]
    elif (interleaving == "f"):                 # fast load interleaving
        inter = [0x00,0x0E,0x0D,0x0C,0x0B,0x0A,0x09,0x08,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF]
    else:                                       # dos interleaving (default pour .dsk/.do)
        inter = [0x00,0x01,0x02,0x03,0x04,0x05,0x06,0x07,0x08,0x09,0x0A,0x0B,0x0C,0x0D,0x0E,0x0F]

    fbin = open(nameBinary,"rb")
    load = fbin.read()                          # lecture du fichier binaire
    lenBin = len(load)                          # on récupère la taille du binaire
    print(lenBin)
    
    modBin = bytearray(load)                    #
    reste = lenBin%256
    div = lenBin//256
    if (reste) != 0:                            # il y a un reste ? (donc pas un multiple de 256)
            nbSector = div+1                    # on calcule le nb de secteurs à écrire
            i = 0
            while i<(256*(div+1))-lenBin:       # on complète avec des zero pour obtenir un multplie de 256
                modBin.append(0)
                i+=1
    else:
            nbSector = div                      # si multiple de 256, nbSector est directement le résultat de la div.
            
    lenmodBin = len(modBin)                     # calcul de la nouvelle taille de liste contenant les octets à insérer
    offset = track*0x1000+sector*0x100          # calcul offset dans le fichier DSK pour l'écriture
    fDSK = open(nameDSK,"rb+")                  # ouverture fichier DSK (lecture + modification)
    record = fDSK.read()                        # lecture complète
    if len(record) != 143360:                   # vérification taille standard d'un fichier DSK
        print("problem with DSK file")
    else :
        bufDSK = struct.Struct("<143360B")      # structure fichier DSK (143360 x 1 byte)
        outDSK = bufDSK.unpack(record)          # on unpack le fichier DSK vers la structure définie
        modifiedDSK = bytearray(outDSK)         # on crée une bytearray à partir du contenu pour pouvoir la modifier
        if (sens == "+"):
        # sens incrémental pour copier le bin dans le DSK
            t = track
            s = sector
            j = 0
            k = 0
            while j<nbSector:
                s1 = inter[s]                   # on récupère le secteur correspondant à l'interleaving
                if s1==0xFF:
                    break                       # si mauvais secteur, on sort (Fast Load Only)
                dest = t*0x1000+s1*0x100        # calcul offset dans DSK du secteur à écrire
                i = 0                           # premier byte secteur en cours
                while i<256:                    # boucle écriture 1 secteur !
                    modifiedDSK[dest+i] = modBin[k]
                    i +=1
                    k +=1
                s +=1                           # secteur suivant
                if s>0x0F:                      # en bout de piste ?
                    s = 0                       # secteur remis à 0
                    t +=1                       # et piste suivante
                j +=1                           # nb secteur écrit + 1
            
        elif (sens == "-"):
        # sens décrémental
            t = track
            s = sector
            j = 0
            k = 0
            while j<nbSector:                   # boucle 1 - nb de secteurs à écrire
                s1 = inter[s]                   # on récupère le secteur correspondant à l'interleaving
                if s1==0xFF:
                    break                       # si mauvais secteur, on sort (Fast Load only)
                dest = t*0x1000+s1*0x100        # calcul offset secteur à écrire
                i = 0                           # premier byte secteur en cours
                while i<256:                    # boucle 2 - nb d'octets à écrire par secteur (256)
                    modifiedDSK[dest+i] = modBin[k]   # on copie chaque byte
                    i +=1                       # on incrémente de 1 (byte suivant dans le secteur)
                    k +=1                       # source (bin) + 1
                s -=1                           # secteur précédent
                if s<0:                         # au début de piste ?
                    s = 0xF                     # on saute alors au dernier secteur de la piste suivante
                    t -=1                       # on décrémente piste
                j +=1                           # nb secteur écrit + 1
                

        print()
        print("Writing",nbSector,"sectors (",hex(lenmodBin),"bytes ) from :")
        print("Sector",sector)
        print("Track",track)
        print("Direction : ", end='')
        if (sens == "+"):
            print("ascending")
        elif (sens == "-"):
            print("descending")
        print("Interleaving : ", end='')
        if (interleaving == "p"):
            print("physical")
        elif (interleaving == "f"):
            print("fast load")
        else:
            print("Dos 3.3")
        print()
        record = bufDSK.pack(*modifiedDSK)      # on repack la liste modifiée vers la structure
        fDSK.seek(0)			        # on remet à zero le file pointer (pour tout réécrire)
        fDSK.write(record)                   	# ecriture vers fichier sortie de la structure
        print("-> file",nameDSK,"modified")

    # fin - nettoyage / fermeture fichiers
    fbin.close()                                # fermeture fichier binaire
    fDSK.close()                                # fermeture fichier DSK
