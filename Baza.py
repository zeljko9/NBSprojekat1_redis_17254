import redis

#   korisnici (skup)->mejlovi //sadd
#   korisnik (hash)->mejl, naziv, zanrovi //hmset
#   zanrovi (skup)->nazivi_zanrova //sadd
#   filmovi_po_zanru (skup)->nazivi_filmova //sadd

class Baza:
    
    def __init__(self):
        self.r=redis.StrictRedis(host='localhost', port=6379, db=0, decode_responses=True)
    
    def resetuj(self):
        self.r.flushall()

    def pretplati_se(self, korisnik, zanrovi):
        if korisnik[1] in self.vrati_korisnike():
            self.azuriraj_korisnika(korisnik[1], zanrovi)
            return 'azurirano'
        self.r.sadd('korisnici',korisnik[1])    #dodavanje mejlova(korisnika)
        dct=dict()
        dct['ime']=korisnik[0]                  #dodavanje imena korisnika
        a=str()
        for z in zanrovi:                       
            if not self.r.sismember('zanrovi', z) and z != '':
                self.r.sadd('zanrovi',z)            #dodavanje zanrova u zanrove ako ne postoji
            if z != '':    
                a=z+','
        dct['zanrovi']=a
        self.r.hmset(korisnik[1],dct)  
        return 'dodato'             #dodavanje zanrova u pretplacene zanrove za korisnika

    def de_pretplata(self, korisnik):
        self.r.srem('korisnici',korisnik)
        pom=self.r.hmget(korisnik, 'zanrovi')
        pom=str(pom).plit(',')
        newpom=list()
        self.r.hdel(korisnik)
        self.r.delete(korisnik)
        korisnici=self.r.smembers('korisnici')
        for k in korisnici:
            for p in pom:
                if p in self.r.hmget(k, 'zanrovi'):
                    newpom.append(p)
        for p in pom:
            if p not in newpom:
                self.r.srem('zanrovi', p)

    def azuriraj_korisnika(self, korisnik, zanrovi):
        self.r.hset(korisnik, 'zanrovi', zanrovi)
        

    def azuriraj_zanr(self, zanr, lista_filmova):
        self.r.delete(zanr)
        for lf in lista_filmova:
            self.r.sadd(zanr, lf)

    def vrati_zanrove(self):
        return self.r.smembers('zanrovi')

    def vrati_filmove(self, zanr):
        return self.r.smembers(zanr)

    def vrati_korisnike(self):
        return self.r.smembers('korisnici')

    def vrati_podatke(self, mejl):
        return self.r.hgetall(mejl)    

    def uporedi_filmove(self, filmovi, zanr):
        for nf in filmovi:
            self.r.sadd('novi_filmovi',nf)
        a=self.r.sdiff('novi_filmovi',zanr)
        #a=list(map(lambda k: k if k not in filmovi else None,a))
        self.r.delete('novi_filmovi')
        if len(a)!=0:
            self.azuriraj_zanr(zanr, filmovi)
        return a

    def koga_obavestiti(self, d):       # d je dictionary sa spiskom novih filmova po zanru
        pom=dict()                      # pom je dictionary sa spiskom novih filmova po korisniku(mejlu)
        korisnici=self.vrati_korisnike()
        for zanr in d:
            novi_filmovi=self.uporedi_filmove(d[zanr], zanr)
            if len(novi_filmovi)==0:
                continue
            for m in korisnici:
                conv=self.vrati_podatke(m)
                #conv2={k.decode("utf-8"):v.decode("utf-8") for k,v in conv.items()}
                if zanr in conv['zanrovi'].split(','):
                    if zanr!='':
                        if zanr in pom:
                            pom[m].append(novi_filmovi)
                        else:
                            pom[m]=novi_filmovi
        return pom