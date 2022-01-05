import Baza as b
import BioskopPretrazivac as bp
import time
import SlanjeMejlova as sm
import threading


def mainLoop():
    baza=b.Baza()
    bioskop=bp.BioskopPretrazivac()
    noviFilmovi=dict()
    #baza.resetuj()
    
    while(True):
        noviFilmovi=bioskop.pretraga_filmovi_zanr()

        obavesti=baza.koga_obavestiti(noviFilmovi)
        for o in obavesti:
            podaci=baza.vrati_podatke(o)
            sm.posalji_mejl((podaci['ime'], o,), baza.vrati_podatke(o)['zanrovi'], obavesti[o])

        time.sleep(43200)


threading.Thread(target=mainLoop()).start()