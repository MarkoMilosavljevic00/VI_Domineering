
from enumeratori import StanjePolja
from konvertovanje import int_u_slovo


class Tabla:
  def __init__(this) -> None:
    print("Izbor parametara za tablu\n ")
    unos = int(input("Broj vrsta table: "))
    while unos < 1 or unos > 26:
      unos =  int(input("Pogresan unos! Tabla moze imati najmanje 1 a najvise 26 vrsti \nBroj vrsta table:"))
    this.brojVrsta = unos

    unos = int(input("Broj kolona table: "))
    while unos < 1 or unos > 26:
      unos =  int(input("Pogresan unos! Tabla moze imati najmanje 1 a najvise 26 kolona \nBroj kolona table:"))
    this.brojKolona = unos

    this.matrica = [[StanjePolja.PRAZNO for i in range(this.brojKolona)] for j in range(this.brojVrsta)]

  def stampaj(this):
    this.stampajKolone()

    print('  ',end ='')
    for i in range(0, this.brojKolona):
      print(' =',end='')
    print('')

    for i in range(0 ,this.brojVrsta):
      print(str(this.brojVrsta-i)+"||",end='')
      for j in range(0,this.brojKolona):
        print(str(this.matrica[i][j])+'|',end='')
      print("|"+str(this.brojVrsta-i), end='\n')
      print('  ',end ='')
      if(i < this.brojVrsta - 1):
        for j in range(0,this.brojKolona):
          print(' -',end='')
        print('')

    for i in range(0, this.brojKolona):
      print(' =',end='')
    print('')

    this.stampajKolone()

  def stampajKolone(this):
    print('  ',end ='')
    for i in range(0, this.brojKolona):
      print(' ' + int_u_slovo(i) ,end='')
    print('')