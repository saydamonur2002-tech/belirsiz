# İşsizlik etkisi: net iş -> işsiz sayısı / oran değişimi. TÜİK İşgücü İstatistikleri, Ağustos 2026 (MEA, 30.09.2026)
LF=35_247_000; U=2_740_000; ATIL=0.310
# Yeni işin işsizlerden dolma payı: 1:1 mekanik üst sınır; ~%40 akım tabanlı kaba türetme (SBB 2022: işsiz->iş %43, işgücü dışı ~%10,3 hareket) 
P=(1.0,0.40)
sen={'Normal alt':0,'Normal üst (düşük)':126_691,'Normal üst (yüksek)':255_260}
print('senaryo,net_is,kapsam,issiz_degisim_1e1,oran_puan_1e1,issiz_degisim_40,oran_puan_40')
for k,n in sen.items():
  for c in (1.0,0.1):
    r=[]
    for p in P:
      dU=-n*c*p
      # işgücüne dışarıdan katılanlar LF'yi büyütür: LF'=LF+n*c*(1-p)
      lf=LF+n*c*(1-p) if n>0 else LF
      r+= [round(dU), round(100*((U+dU)/lf - U/LF),2)]
    print(f"{k},{n},{int(c*100)}%,"+",".join(map(str,r)))
