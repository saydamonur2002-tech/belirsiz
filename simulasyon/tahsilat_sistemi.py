# Maliyet açığı kuralı + dijital tahsilat sistemi: korunan iş (üst sınır), alt sınır 0
# Kaynak: Hazine ve Maliye Bak. (2018, AA): iflasların ~1/4'ü tahsil edilemeyen alacak kaynaklı
isyeri,sigortali,ins_ist=229_550,1_991_728,2_224_000
kisi=sigortali/isyeri
t=0.25                      # tahsilat kaynaklı iflas payı (kaynaklı, tüm sektörler)
azalma={'düşük':1-15/87,'yüksek':1-15/103}
taban={'TOBB kapanış bina inşaatı (1.652×2 yıllık)':1652*2,'Konkordato inşaat 2025':511}
print('taban,senaryo,risk_altindaki_is,yalniz_maliyet_ust,yalniz_tahsilat_ust,birlesik_ust,birlesik_ust_10,birlesik_pay,alt_sinir')
for n0,n in taban.items():
  r=n*kisi
  for k,a in azalma.items():
    m=r*a; th=r*t; b=r*((1-t)*a+t)   # tahsilat payı ve maliyet payı ayrık; tahsilat etkinliği =1 (üst)
    print(f"{n0},{k},{r:.0f},{m:.0f},{th:.0f},{b:.0f},{b*0.1:.0f},{b/ins_ist*100:.2f}%,0")
