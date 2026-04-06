import sys


def paarungen(freie_staedte, aktuelle_paare, aktuelle_kosten):
    k = len(freie_staedte)
    global limit
    
    if k == 0:
        if optimize:
            if aktuelle_kosten < limit:
                limit = aktuelle_kosten
        else:
            print_paare(sorted(aktuelle_paare))
        return

    erste = freie_staedte[0]
    

    for i in range(1, k):
        partner = freie_staedte[i]
        
        neue_kosten = aktuelle_kosten + kosten[erste][partner]
        #jede Paarung kostet mindestens 1, die neue Paarung wurde noch nicht abgezogen
        if neue_kosten > limit - (k-2)/2: continue
        
        paarungen(freie_staedte[1:i] + freie_staedte[i+1:], aktuelle_paare + [(erste, partner)], neue_kosten)


def print_paare(paare):
    teile = []
    
    for a, b in paare:
        teile.append(a + b)
    
    print(" ".join(teile))


dateiname = sys.argv[1]    
optimize = False
if len(sys.argv) > 2 and sys.argv[2] == "-o":
    optimize = True
    
with open(dateiname, "r", encoding="utf-8") as f:
    zeilen = f.readlines()

# erste Zeile auswerten
erste_zeile = zeilen[0].strip().split()

n = int(erste_zeile[0])
limit = int(erste_zeile[1])

# zweite Zeile
staedte = zeilen[1].strip().split()

# Kostenmatrix als Dictionary
kosten = {}

for i in range(2, len(zeilen)):
    werte = zeilen[i].strip().split()
    stadt = staedte[i-2]

    kosten[stadt] = {}

    #nur obere Dreiecksmatrix speichern ohne Diagonale
    for j in range(i-1, len(werte)):
        kosten[stadt][staedte[j]] = int(werte[j])
        
        
paarungen(staedte, [], 0)
if optimize:
    print(limit)
        
