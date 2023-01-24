import os
from enumeratori import TipIgraca
from konvertovanje import int_u_slovo, slovo_u_int,int_u_vrstu
from tabla import Tabla
from enumeratori import StanjePolja

class Igra:
  def __init__(this) -> None:
    this.odabir_igraca()
    this.tabla = Tabla()
    this.tabla.stampaj()

  def odabir_igraca(this):
      this.trenutno_igra = TipIgraca.X
      this.ocisti_konzolu()
      print("Pravila igre Domineering:")
      print("Korisnik na pocetku bira da li zeli da bude X ili O.Njegove figure ce biti predstavljene na tabli u zavisnosti od njegovog izbora.")
      print("Dalje, korisnik je u mogucnosti da odabere dimenzije table na kojoj ce se ova igra igrati.")
      print("X uvek igra prvi i bira polje na kojoj ce postaviti figuru.")
      print("Figura je dimenzija 2x1 za X i 1x2 za O.")
      print("Primer postavljanja figure na tabli: Ukoliko korisnik koji je X unese polje [1 A], figura ce biti postavljena na polju [1 A] i polju [2 A].")
      print("Slicno i za O,ukoliko korisnik unese polje [1 A] figura ce biti postavljena na poljima [1 A] [1 B].")
      print("Ukoliko dodje do loseg unosa u konzoli,korisniku ce biti ispisano zbog cega je doslo do greske.")
      print("Dalje ako je potez od X-a validan, na potezu ce biti O,i obrnuto.")
      print("Igraci ce vuci poteze naizmenicno, sve dok se ne dodje do kraja igre,odnosno sve dok neki igrac ne bude bio u stanju da unese svoju figuru na tablu.")
      unos = input("Molimo izaberite koji igrac zelite da budete [X/O] \n==>(Ukoliko odaberete X bicete prvi na potezu)\n==>  ")
      while unos not in ['X', 'x', 'O','o']:
        unos = input("Pogresan unos! \nMolimo izaberite koji igrac zelite da budete [X/O] ")
      if(unos=='X' or unos == 'x'):
        this.tip_igraca = TipIgraca.X
      elif(unos=='O' or unos == 'o'):
        this.tip_igraca = TipIgraca.O
      print("Izabrali ste igraca " + ('X\n' if this.tip_igraca == TipIgraca.X else 'O\n'))

  
  def zapocni_igru(this):
    while not this.kraj_igre():
      this.novi_potez()
    else:
      print("Kraj igre! \nPobednik je " + ("X" if this.nadji_pobednika() == TipIgraca.X else "O"))

  def novi_potez(this):
    print('Trenutno na potezu: ' +   ('X' if this.trenutno_igra==TipIgraca.X else 'O'))
    vrsta, kolona = this.unos_poteza()
    provera=this.validiraj_potez(vrsta,kolona)
    if provera==True:
      if(this.trenutno_igra == TipIgraca.X):
        this.promeni_stanje(vrsta, kolona, StanjePolja.X, TipIgraca.X)
        this.trenutno_igra = TipIgraca.O
      else:
        this.promeni_stanje(vrsta, kolona, StanjePolja.O, TipIgraca.O)
        this.trenutno_igra = TipIgraca.X
      this.tabla.stampaj()
    elif provera=='Van Table':
      print("Van table!")#premasili ste dimenzije table!
    elif provera=='Polje zauzeto':
      print('Polje na koje zelite da odigrate potez je zauzeto!')
  def promeni_stanje(this, vrsta, kolona, stanje, tip_igraca):
    if(tip_igraca == TipIgraca.X):
      this.tabla.matrica[vrsta][kolona] = stanje
      this.tabla.matrica[vrsta - 1][kolona] = stanje
    else:
      this.tabla.matrica[vrsta][kolona] = stanje
      this.tabla.matrica[vrsta][kolona+1] = stanje

  def moguca_stanja(this):
    moguca_stanja = []
    print("-------------------- Prikaz svih mogucih poteza -----------------")
    if(this.trenutno_igra == TipIgraca.X):
      for i in range(1,this.tabla.brojVrsta):
        for j in range(0,this.tabla.brojKolona):
          if(this.validiraj_potez(i,j) == True):
            this.promeni_stanje(i, j, StanjePolja.X, TipIgraca.X)
            this.tabla.stampaj()
            print("Potez: [" + str(int_u_vrstu(i, this.tabla.brojVrsta)) + " - " + int_u_slovo(j)+ "]", end ="\n\n")
            moguca_stanja.append(str(int_u_vrstu(i, this.tabla.brojVrsta)) + " - " + int_u_slovo(j))
            this.promeni_stanje(i, j, StanjePolja.PRAZNO, TipIgraca.X)
    else:
      for i in range(0,this.tabla.brojVrsta):
        for j in range(0,this.tabla.brojKolona-1):
          if(this.validiraj_potez(i, j) == True):
            this.promeni_stanje(i, j, StanjePolja.O, TipIgraca.O)
            this.tabla.stampaj()
            print("Potez: [" +str(int_u_vrstu(i,this.tabla.brojVrsta)) + " - " + int_u_slovo(j) + "]", end ="\n\n")
            moguca_stanja.append(str(int_u_vrstu(i, this.tabla.brojVrsta)) + " - " + int_u_slovo(j))
            this.promeni_stanje(i, j, StanjePolja.PRAZNO, TipIgraca.O)
    print("Mozete odigrati sledece poteze: ")
    for stanje in moguca_stanja:
      print("[" + stanje + "]")

  def unos_poteza(this):
      print("Ukoliko zelite da vidite sve preostale moguce poteze unesite /h(elp)")
      vrstaString = input("Unesite vrstu u opsegu od [1-" + str(this.tabla.brojVrsta) + "]: ")
      while not vrstaString.isdigit():
        if(vrstaString == "/h" or vrstaString == "/help"):
          this.moguca_stanja()
          vrstaString = input("Unesite vrstu u opsegu od [1-" + str(this.tabla.brojVrsta) + "]: ")
        else:
          vrstaString =  input("Pogresan unos, vrsta se predstavlja cifrom! \nUnesite vrstu: [1-" + str(this.tabla.brojVrsta) + "] ")
      vrsta = int(vrstaString)
      vrsta = this.tabla.brojVrsta-vrsta
      kolonaString = input("Unesite kolonu u opsegu od [A-" + int_u_slovo(this.tabla.brojKolona-1) + "]: ")
      while not kolonaString.isalpha():
        kolonaString = input("Pogresan unos, kolona se predstavlja slovom! \nUnesite kolonu: [A-" + int_u_slovo(this.tabla.brojKolona-1) + "] ")
      kolona = slovo_u_int(kolonaString)
      return vrsta,kolona


  def validiraj_potez(this, vrsta, kolona):
    if(this.trenutno_igra == TipIgraca.X):
      if(vrsta-1 < 0 or vrsta >= this.tabla.brojVrsta or kolona < 0 or kolona>=this.tabla.brojKolona):
        return 'Van Table'
      if(this.tabla.matrica[vrsta][kolona]==StanjePolja.PRAZNO and this.tabla.matrica[vrsta-1][kolona]==StanjePolja.PRAZNO):
        return True
      else:
        return 'Polje zauzeto'
    else:
      if(vrsta < 0 or vrsta >= this.tabla.brojVrsta or kolona < 0 or kolona + 1>=this.tabla.brojKolona):
        return 'Van Table'
      if(this.tabla.matrica[vrsta][kolona]==StanjePolja.PRAZNO and this.tabla.matrica[vrsta][kolona+1]==StanjePolja.PRAZNO):
        return True
      else:
        return 'Polje zauzeto'

  def kraj_igre(this):
    if(this.trenutno_igra == TipIgraca.X):
      for i in range(1,this.tabla.brojVrsta):
        for j in range(0,this.tabla.brojKolona):
          if(this.tabla.matrica[i][j]==StanjePolja.PRAZNO and this.tabla.matrica[i-1][j]==StanjePolja.PRAZNO):
            return False
    else:
      for i in range(0,this.tabla.brojVrsta):
        for j in range(0,this.tabla.brojKolona-1):
          if(this.tabla.matrica[i][j]==StanjePolja.PRAZNO and this.tabla.matrica[i][j+1]==StanjePolja.PRAZNO):
            return False
    return True

      
  def nadji_pobednika(this):
    if(this.trenutno_igra == TipIgraca.X):
      return TipIgraca.O
    else:
      return TipIgraca.X
      
  def ocisti_konzolu(this):
    os.system('cls')
  
