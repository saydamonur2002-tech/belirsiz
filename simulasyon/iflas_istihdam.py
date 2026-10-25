# İflas/kapanış önleme ile korunan istihdam — varsayımsız üst sınır, alt sınır 0
# Kaynaklar: TOBB (2025 İY bina inşaatı kapanış 1.652), SGK 2024 (229.550 işyeri, 1.991.728 sigortalı),
# konkordato 2025 inşaat 511 dosya (konkordatotakip derlemesi), backtest zarar kohortu 87->15 ve 103->15
isyeri,sigortali,ins_ist=229_550,1_991_728,2_224_000
kisi=sigortali/isyeri
azalma={'düşük':1-15/87,'yüksek':1-15/103}
taban={'TOBB kapanış bina inşaatı (1.652×2 yıllık)':1652*2,'Konkordato inşaat 2025':511}
print('taban,firma_yil,risk_altindaki_is,azalma,korunan_ust_100,korunan_ust_10,insaat_istihdam_payi_100,alt_sinir')
for t,n in taban.items():
  r=n*kisi
  for k,a in azalma.items():
    u=r*a; print(f"{t} [{k}],{n},{r:.0f},{a:.3f},{u:.0f},{u*0.1:.0f},{u/ins_ist*100:.2f}%,0")
