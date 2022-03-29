#-------------------KÜTÜPHANE------------------#
#----------------------------------------------#

import sys
from PyQt5.QtWidgets import *
from GirisEkraniUI import *
from KayitEkraniUI import *
from SifremiUnuttumEkraniUI import *
from AsilPencereUI import *
import random
import hashlib as hasher

#---------------UYGULAMA OLUSTUR---------------#
#----------------------------------------------#

Uygulama = QApplication(sys.argv)

penGirisEkrani = QWidget()
ui1 = Ui_Form1()
ui1.setupUi(penGirisEkrani)

penKayitEkrani = QWidget()
ui2 = Ui_Form2()
ui2.setupUi(penKayitEkrani)

penSifremiUnuttumEkrani = QWidget()
ui3 = Ui_Form3()
ui3.setupUi(penSifremiUnuttumEkrani)

penAsilPencere = QMainWindow()
uiA = Ui_MainWindow()
uiA.setupUi(penAsilPencere)

penGirisEkrani.show()

#-------------KULLANICI GİRİŞ İÇİN VERİTABANI OLUŞTUR---------------#
#-------------------------------------------------------------------#

import sqlite3
global conn
global curs

conn = sqlite3.connect("SahibindenProjesiKullaniciVerileri.db")
curs = conn.cursor()

sorguCreTblKullaniciVerileri = ('CREATE TABLE IF NOT EXISTS KullaniciVerileri(    \
                                Id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,    \
                                KullaniciAdi TEXT NOT NULL,                       \
                                Sifre TEXT NOT NULL,                              \
                                MailAdresi TEXT NOT NULL,                         \
                                TelefonNumarasi TEXT NOT NULL,                    \
                                ReklamIzni TEXT,                                  \
                                SifreSalt TEXT NOT NULL,                          \
                                MailAdresiSalt TEXT NOT NULL,                     \
                                TelefonNumarasiSalt TEXT NOT NULL)')

curs.execute(sorguCreTblKullaniciVerileri)
conn.commit()

#-------------SALTİNG VE HASHİNG FONKSİYONLARI--------------#
#-----------------------------------------------------------#

"""
Veritabanımız da verilerimizi güvenli bir şekilde saklamak
için çok önemli olan hashing ve salting işlemlerini aşağıda 
ki fonksiyonları çeşitli yerlerde kullanarak yapacağız.
"""

def SALTINGHASHING(veri):

    """
    Salting işlemi için 6 haneli bir sayı oluşturup
    verimizin sonuna ekleyeceğiz. Bu işlemde while
    döngüsü kullanacağım bu nedenle bir sayaç oluşturmam
    gerekiyor.
    Ayrıca 6 haneli sayının rakamlarını seçmek için random
    modülünü import etmem gerekiyor.
    """
    sayac = 0
    while sayac<6:


        rakamlar = ["1","2","3","4","5","6","7","8","9","0"]
        veri += random.choice(rakamlar)
        sayac += 1

    salt = veri[-6:]
    sifreleyici = hasher.sha256()
    sifreleyici.update(veri.encode("utf-8"))
    veri = sifreleyici.hexdigest()
    liste = [veri,salt]
    return (liste)

def HASHING(veri):

    sifreleyici = hasher.sha256()
    sifreleyici.update(veri.encode("utf-8"))
    veri = sifreleyici.hexdigest()
    return veri


#-------------MAİN WİNDOW--------------#
#--------------------------------------#

def ASILPENCERE():
    penGirisEkrani.close()
    penAsilPencere.show()

#-------------KAYIT OLMA EKRANI--------------#
#--------------------------------------------#
ui1.lblBilgilendirmeGiris.setText("Hoşgeldiniz lütfen giriş yapın!")

def KAYITOLMAEKRANIKAYITOLBUTONU():

    #----- BİLGİLERİ ALMA -----#

    yenikullaniciadi = ui2.lneYeniKayitKullaniciAdi.text()
    yenisifre = ui2.lneYeniKayitSifre.text()
    yenimailadresi = ui2.lneYeniKayitMailAdresi.text()
    yenitelno = ui2.lneYeniKayitTelNo.text()
    yenitelno = yenitelno.replace(" ","")
    yenitelno = yenitelno[1:4] + yenitelno[5:]
    yenireklamizni = ui2.checkReklam.checkState()
    bilgilendirmemetni = ui2.checkBilgilendirmeMetni.checkState()

    veriler_listesi = [yenisifre,yenimailadresi,yenitelno]
    islenmis_veriler_listesi = []
    salt_degerleri = []

    for deger in veriler_listesi:

        listeler = SALTINGHASHING(deger)
        islenmis_veriler_listesi.append(listeler[0])
        salt_degerleri.append(listeler[1])


    #----- KAYIT OLA BASILDIKTAN SONRA VERİTABANINA GİRME -----#
    if len(yenikullaniciadi) == 0 or len(yenisifre) == 0 or len(yenimailadresi) == 0 or len(yenitelno) == 0:
        ui2.lblBilgilendirme.setText("Bilgileri eksik girdiniz!")
    else:
        if yenireklamizni == 2:
            yenireklamizni = "Evet"
        else:
            yenireklamizni = "Hayır"

        if bilgilendirmemetni == 0:
            ui2.lblBilgilendirme.setText("Bilgilendirme metni kutucuğunu işaretlemeniz gerek!")
        else:
            curs.execute('SELECT * FROM KullaniciVerileri WHERE KullaniciAdi = ?', (yenikullaniciadi,))
            conn.commit()

            veri = curs.fetchall()

            if len(veri) == 0:

                curs.execute('INSERT INTO KullaniciVerileri (KullaniciAdi,Sifre,MailAdresi,TelefonNumarasi,ReklamIzni,SifreSalt,MailAdresiSalt,TelefonNumarasiSalt) \
                VALUES(?,?,?,?,?,?,?,?)',(yenikullaniciadi,islenmis_veriler_listesi[0],islenmis_veriler_listesi[1],islenmis_veriler_listesi[2],yenireklamizni,salt_degerleri[0],salt_degerleri[1],salt_degerleri[2]))
                conn.commit()
                penKayitEkrani.close()
                penGirisEkrani.show()
                str = "Kaydın başarılı "+yenikullaniciadi+". Lütfen giriş yap."
                str1 = f"<html><head/><body><p><span style=\" color:#008000;\">{str}</span></p></body></html>"
                ui1.lblBilgilendirmeGiris.setText(str1)
            else:
                ui2.lblBilgilendirme.setText("Bu kullanıcı adı ile kayıtlı başka bir hesap bulunmakta.")

#-------------KAYIT OL BUTONU--------------#
#------------------------------------------#

def KAYITOL():

    #----- GİRİŞ PENCERESİNİ KAPATIP KAYIT PENCERESİNİ AÇMA -----#
    penGirisEkrani.close()
    penKayitEkrani.show()

#-------------GİRİŞ YAP BUTONU--------------#
#-------------------------------------------#

def GIRISYAP():

    #----- BİLGİLERİ ALMA -----#
    kullanici_adi = ui1.lneKullaniciAdi.text()
    sifre = ui1.lneSifre.text()


    # ----- GİRİŞ YAPA BASILDIKTAN SONRA Kİ DOĞRULAMALAR -----#
    if len(kullanici_adi) == 0 or len(sifre) == 0:
        str = "<html><head/><body><p><span style=\" color:#ff0000;\">Bilgileri eksik girdiniz.</span></p></body></html>"
        ui1.lblBilgilendirmeGiris.setText(str)
    else:
        curs.execute("SELECT * FROM KullaniciVerileri WHERE KullaniciAdi = ?", (kullanici_adi,))
        conn.commit()
        data = curs.fetchall()

        if len(data) == 0:
            str = "<html><head/><body><p><span style=\" color:#ff0000;\">Böyle bir kullanıcı bulunmamaktadır.</span></p></body></html>"
            ui1.lblBilgilendirmeGiris.setText(str)
        else:
            saltsifre = data[0][6]
            sifre += saltsifre

            veri = HASHING(sifre)

            curs.execute("SELECT * FROM KullaniciVerileri WHERE KullaniciAdi = ? and Sifre = ?", (kullanici_adi,veri))
            conn.commit()
            kullanicidata = curs.fetchall()


            if len(kullanicidata) != 0:
                str = ("<html><head/><body><p><span style=\" color:#008000;\">Giriş Başarılı.</span></p></body></html>")
                ui1.lblBilgilendirmeGiris.setText(str)

                """
                Projenin bu satırından sonra ki aşamaları bu kayıt ve giriş sistemini entegre edeceğiniz projeye göre
                şekillendirebilirsiniz. Şu an bu sistem kendi başına çalıştığı için Asıl Pencere'de birşey bulunmamaktadır.
                """

                ASILPENCERE()

            else:
                str = ("<html><head/><body><p><span style=\" color:#ff0000;\">Kullanıcı adı veya şifre yanlış!</span></p></body></html>")
                ui1.lblBilgilendirmeGiris.setText(str)

#-------------ŞİFRENİZİ Mİ UNUTTUNUZ BUTONU--------------#
#--------------------------------------------------------#

def SIFRENIZIMIUNUTTUNUZBUTONU():

    #----- GİRİŞ PENCERESİNİ KAPATIP ŞİFREMİ UNUTTUM PENCERESİNİ AÇAN FONKSİYON -----#
    penGirisEkrani.close()
    penSifremiUnuttumEkrani.show()
    ui3.lneYeniSifre.setReadOnly(True)
    ui3.lneYeniSifreDogrula.setReadOnly(True)
    ui3.lneEmailKod.setReadOnly(True)

#-------------KODLARI GÖNDER BUTONU--------------#
#------------------------------------------------#

def KODLARIGONDERBUTONU():

    _kullaniciadi = ui3.lneUnutKullaniciAdi.text()
    _mailadresi = ui3.lneMailAdresi.text()
    temizhal = ui3.lneMailAdresi.text()

    global kodlar
    kodlar = ''

    #----- MAİLİ GÖNDERME İŞLEMLERİ -----#
    if (len(_kullaniciadi) or len(_mailadresi)) != 0:
        curs.execute("SELECT * FROM KullaniciVerileri WHERE KullaniciAdi = ?", (_kullaniciadi,))
        conn.commit()
        data = curs.fetchall()

        if len(data) != 0:
            _mailadresiSalt = data[0][7]
            _mailadresi = temizhal

            _mailadresi += _mailadresiSalt

            veri = HASHING(_mailadresi)

            if data[0][3] == veri:
                ui3.lblBilgilendirmeSifremiUnuttum.setText("Kodlar gönderildi...")
                ui3.lneUnutKullaniciAdi.setReadOnly(True)
                ui3.lneMailAdresi.setReadOnly(True)

                #-----MAİLE KOD YOLLAMA-----#
                #---------------------------#

                import smtplib
                from email.mime.multipart import MIMEMultipart
                from email.mime.text import MIMEText
                import random

                mailadresi = temizhal

                mesaj = MIMEMultipart()
                mesaj["From"] = "pythondeneme06@gmail.com"
                mesaj["To"] = mailadresi
                mesaj["Subject"] = "Şifre değiştirme için mail doğrulama kodu"
                kod = ''
                while len(kod) < 6:
                    kod += str(random.randint(1,10))
                kodlar += kod
                mesaj_govdesi = MIMEText(kod, "plain")
                mesaj.attach(mesaj_govdesi)

                try:
                    mail = smtplib.SMTP("smtp.gmail.com", 587)

                    mail.ehlo()

                    mail.starttls()

                    mail.login("pythondeneme06@gmail.com", "mca171003")

                    mail.sendmail(mesaj["From"], mesaj["To"], mesaj.as_string())

                    ui3.lblBilgilendirmeSifremiUnuttum.setText("Doğrulama maili gönderildi!")
                    mail.close()
                    ui3.lneYeniSifre.setReadOnly(False)
                    ui3.lneYeniSifreDogrula.setReadOnly(False)
                    ui3.lneEmailKod.setReadOnly(False)
                except:
                    ui3.lblBilgilendirmeSifremiUnuttum.setText("Mail gönderilirken bir hata oldu!")

        else:
            stringdegeri = ("<html><head/><body><p><span style=\" color:#ff0000;\">Bu bilgilere sahip bir</span></p></body></html>\n\
            <html><head/><body><p><span style=\" color:#ff0000;\">kullanıcı yok</span></p></body></html>")
            ui3.lblBilgilendirmeSifremiUnuttum.setText(stringdegeri)
    else:
        ui3.lblBilgilendirmeSifremiUnuttum.setText("Kullanıcı adı kısmı boş!")



#-------------ŞİFREYİ DEĞİŞTİR BUTONU--------------#
#--------------------------------------------------#

def SIFREYIDEGISTIRBUTONU():

    #----- ŞİFREYİ DEĞİŞTİRME BUTONU -----#
    if ui3.lneUnutKullaniciAdi.isReadOnly():
        girilmismailkodu = str(ui3.lneEmailKod.text())
        if girilmismailkodu == kodlar:
            if ui3.lneYeniSifre.text() == ui3.lneYeniSifreDogrula.text():
                curs.execute("SELECT * FROM KullaniciVerileri WHERE KullaniciAdi=?",(ui3.lneUnutKullaniciAdi.text(),))
                data = curs.fetchall()
                _id = data[0][0]
                _YeniSifre = ui3.lneYeniSifre.text()
                _YeniSifre += data[0][6]
                _YeniSifre = HASHING(_YeniSifre)
                curs.execute("UPDATE KullaniciVerileri SET Sifre = ? WHERE KullaniciAdi = ?",(_YeniSifre,ui3.lneUnutKullaniciAdi.text()))
                conn.commit()
                penSifremiUnuttumEkrani.close()
                penGirisEkrani.show()
                ui1.lblBilgilendirmeGiris.setText("Şifreniz başarıyla değiştirildi. Lütfen giriş yapın.")
            else:
                ui3.lblBilgilendirmeSifremiUnuttum.setText("İki şifre uyuşmuyor!")
        else:
            ui3.lblBilgilendirmeSifremiUnuttum.setText("Maile giden kod ile eşleşme yok.")
    else:
        ui3.lblBilgilendirmeSifremiUnuttum.setText("Önce yukarıda ki boşluklar doldurulmalı!")

#-------------SİNYAL-SLOT--------------#
#--------------------------------------#

ui1.btnKayitOl.clicked.connect(lambda : KAYITOL())
ui1.btnGirisYap.clicked.connect(lambda : GIRISYAP())
ui1.btnSifreUnutma.clicked.connect(lambda : SIFRENIZIMIUNUTTUNUZBUTONU())
ui2.btnKaydol.clicked.connect(lambda : KAYITOLMAEKRANIKAYITOLBUTONU())
ui3.btnKodlariGonder.clicked.connect(lambda : KODLARIGONDERBUTONU())
ui3.btnSifreyiDegistir.clicked.connect(lambda : SIFREYIDEGISTIRBUTONU())

sys.exit(Uygulama.exec_())

# Benimle iletişime geçmek için: cihanayindi00@gmail.com
# You can reach me with this: cihanayindi00@gmail.com
# Thanks for comments..!

