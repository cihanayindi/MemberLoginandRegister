import random
import os
import hashlib as hasher
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
    while sayac < 6:
        rakamlar = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "0"]
        veri += random.choice(rakamlar)
        sayac += 1

    salt = veri[-6:]
    veri = hash(veri)
    liste = [veri, salt]
    return (liste)

sifreleyici = hasher.sha256()
veri = "cihan123"
sifreleyici.update(veri.encode("utf-8"))
hash = sifreleyici.hexdigest()
print(hash)