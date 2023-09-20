import sys
import tkinter as tk
import time
### vizualizace prohledavani do hloubky \ do sirky v bludisti

def nacti_vstup(soubor):
    # nacita vstupni soubor
    with open(soubor, encoding='utf-8-sig') as infile:
        lines = infile.readlines()
    # vstup ve formatu txt s bludistem
    pocet_sloupcu, pocet_radku = lines.pop(0).split(" ")
    pocet_sloupcu = int(pocet_sloupcu)
    pocet_radku = int(pocet_radku.rstrip("\n"))
    x_startu = None
    y_startu = None
    x_cile = None
    y_cile = None
    parents = dict() # bude slouzit k nalezeni cesty zpet -
    # ke kazdemu policku zaznamena policko, ktere bylo na ceste pred nim 
    frontier = [] # fronta nebo zasobnik
    mapa = dict()
    # mapa = {(x,y) : e}
    y = -1 # cislo radku, indexuju od nuly
    x = 0 # poradi v radku, indexuju tez od nuly
    for radek in lines:
        radek = radek.rstrip("\n")
        y += 1
        x = 0
        for element in radek:
            mapa[(x, y)] = element
            if element == "S": # pokud je policko start
                parents[(x, y)] = None # jeste pred polickem nic nebylo
                frontier.append((x, y)) # pridam do fronty/ zasobniku - jako pocatecni policko
                x_startu = x # ulozi souradnice startu
                y_startu = y
                
            if element == "C": # pokud narazi na cil
                x_cile = x # ulozi souradnice cile
                y_cile = y    
            x += 1

    #print("souradnice startu", x_startu, y_startu)
    #print("souradnice cile", x_cile, y_cile)
    #print(frontier)
    #print(mapa)

    return pocet_sloupcu, pocet_radku, x_startu, y_startu, x_cile, y_cile, mapa, frontier, parents
  
def prohledej(typ, pocet_sloupcu, pocet_radku, x_startu, y_startu, x_cile, y_cile, mapa, frontier, parents, bludiste, ms):
    # spusti prohledavani bfs, pokud typ je 0
    # spusti prohledavani dfs, pokud typ je 1
    smery = [(1, 0), (-1, 0), (0, 1), (0, -1)]
    cil_nalezen = False # jeste nebyl nalezen cil
    explored = set() # mnozina navstivenych policek
    # mnozina policek, na kterych jsem uz byla
    while len(frontier):
        if typ == 0:
            # typ je bfs, tudiz vybiram z fronty
            aktp = frontier.pop(0) # tzn. aktualni policko, na kterem stojim
        else: 
            # typ je dfs, tudiz vybiram ze zasobniku
            aktp = frontier.pop() # tzn. aktualni policko, na kterem stojim

        for policko in frontier:
            bludiste[policko].config(bg = "green") # obarvi policka, ktera jsou ve fronte nebo zasobniku
        
        ms.update() # vykresluje
        # https://www.daniweb.com/programming/software-development/threads/468733/time-sleep-in-for-loop-using-tkinter
        time.sleep(0.1) # mala pauza
        if mapa[aktp] == "C":
            cil_nalezen = True
            bludiste[aktp].config(bg="yellow")  # obarvi akt policko
            break
    
        if aktp not in explored: #tzn. aktp jeste nebylo nenavstivene a neni cil
        #     ted zkontroluji, jestli jsou policka kolem aktp zdi nebo cesty
            explored.add(aktp) # prida akt policko do mnoziny prozkoumanych
            bludiste[aktp].config(bg = "light green") # obarvi akt policko
            for smer in smery:
                nove_x = aktp[0] + smer[0]
                nove_y = aktp[1] + smer[1]
                
                if (nove_x, nove_y) not in mapa:
                    #jsme v autu, neni to v mape
                    continue
                
                sousedova_pozice = (nove_x , nove_y)
                if mapa[sousedova_pozice] in (".", "C"): #na sousedovu pozici jde vstoupit, neni zed
                    if (sousedova_pozice not in explored
                        and sousedova_pozice not in frontier): # pokud soused nebyl prozkoumany a neni jeste ve frontier
                        frontier.append(sousedova_pozice)
                        parents[sousedova_pozice] = aktp
                        #print("pridano do frontier", sousedova_pozice)
                                
    print("Nalezen cil?", cil_nalezen, aktp, frontier)
    
    if cil_nalezen:
        # najdu cestu zpet -> cesta bude zacinat startem a koncit cilem:
        # parents = {kde : odkud sem dosel}
        akt_rodic = (x_cile, y_cile) # resp. klic ve slovniku
        cesta = [akt_rodic] # seznam s policky cesty
        while akt_rodic != (x_startu, y_startu): # dokud v ceste nedosel zpet
            akt_rodic = parents[akt_rodic] # najde predchozi policko
            bludiste[akt_rodic].config(bg = "blue") # obarvi akt policko
            cesta.append(akt_rodic) # prida do cesty
        cesta.reverse() # aby byla cesta ze startu do cile
        print("cesta", cesta)
        print("delka cesty", len(cesta))



    return

def main():
    path = "./bludiste_vstup.txt"
    #path = "C:/programs/test/ag 2021 2022/bludiste_vstup.txt"
    # path = "/share/home/studenti/cinkovao/programy_6a/bludiste_vstup.txt"
    if len(sys.argv) > 1 and sys.argv[1].startswith("-p="):
        path = sys.argv[1][3:]
    pocet_sloupcu, pocet_radku, x_startu, y_startu, x_cile, y_cile, mapa, frontier, parents = nacti_vstup(path)
    print(pocet_sloupcu, pocet_radku, x_startu, y_startu, x_cile, y_cile, mapa)
    ms = tk.Tk()
    # misto na bludiste
    frame1 = tk.Frame(ms)
    frame1.grid(row = 1, column = 1, sticky = tk.NSEW)
    bludiste = dict()
    for j in range(pocet_radku): # rozmer x 
        for i in range(pocet_sloupcu): # rozmer y
            barva = None
            text = None
            if mapa[(i,j)] == "#":
                barva = "maroon"
                text = str(i) + ";" + str(j) # souradnice policka
            else:
                barva = "beige"
                text = str(i) + ";" + str(j) # souradnice policka
            if mapa[(i,j)] == "S":
                text = "START" + "\n" + str(i) + ";" + str(j)
            if mapa[(i,j)] == "C":
                text = "CÍL" + "\n" + str(i) + ";" + str(j)
            bludiste[(i, j)] = tk.Button(frame1, text= text ,height= 2, width=5, bg = barva)
            bludiste[(i, j)].grid(row = j, column = i, sticky = tk.NSEW)
    # misto na tlacitka
    frame2 = tk.Frame(ms)
    frame2.grid(row = 2, column = 1, sticky = tk.NSEW)

    # tlacitko na prohledavani do sirky
    bfs_tlacitko = tk.Button(frame2, text= "prohledavej do sirky!" ,height= 3, width=30, bg = "light blue", command = lambda: prohledej(
        0, pocet_sloupcu, pocet_radku, x_startu, y_startu, x_cile, y_cile, mapa, frontier, parents, bludiste, ms) )
    bfs_tlacitko.grid(row = 1, column = 1, sticky = tk.NSEW)


    # tlacitko na prohledavani do hloubky
    dfs_tlacitko = tk.Button(frame2, text= "prohledavej do hloubky!",
                             height= 3, width=30,
                             bg = "light blue", command = lambda: prohledej(
        1, pocet_sloupcu, pocet_radku, x_startu, y_startu, x_cile, y_cile, mapa, frontier, parents, bludiste, ms))
    dfs_tlacitko.grid(row = 1, column = 2, sticky = tk.NSEW)

    # fun fact: nevim proc, ale pomohlo pouzit lambda funkci, aby se command nespustil hned po spusteni kodu:
    # https://stackoverflow.com/questions/49085244/tkinter-button-command-getting-executed-before-clicking-the-button

    ms.mainloop()
    
    return



if __name__ == "__main__":
    main()
