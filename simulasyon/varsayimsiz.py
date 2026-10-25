"""Varsayimsiz degerlendirme: yalnizca kaynakli seriler/agirliklar. Kaynaklar VARSAYIMSIZ.md."""
import json,pandas as pd,numpy as np
exec(open('vergi_subvansiyon.py').read().split('SC={')[0])  # annual(), tarife, MW
# TUIK Insaat Maliyet Endeksi toplam (2015=100), aylik; hakedis.org (TUIK yansisi)
T={2015:[97.13,97.65,98.27,99.14,100.17,100.03,100.83,101.35,102.25,101.56,101.01,100.6],
2016:[108.19,108.12,109.39,110.26,112.11,111.6,111.52,111.9,112.19,113.06,115.83,118.9],
2017:[124.69,125.09,126.43,126.84,127.26,127.06,128.16,129.51,130.94,132.76,136.09,138.14],
2018:[144.92,146.6,149.08,152.1,156.58,160.17,162.78,172.71,182.87,182.57,176.85,173.57],
2019:[184.83,186.51,189.25,192.27,195.51,193.97,192.76,191.35,190.23,190.36,190.32,192.25],
2020:[202.04,202.34,202.34,204.08,206.85,208.46,210.43,216.3,220.87,227.47,234.07,240.35],
2021:[258.24,258.16,267.03,276.48,288.67,297.02,304.61,307.43,308.2,322.84,348.46,403.16],
2022:[464.6,491.2,538.26,571.22,593.87,614.46,654.13,667.06,677.52,700.8,709.02,719.25],
2023:[829.42,846.7,864.96,873.91,878.63,917.53,1061.35,1110.41,1137.77,1162.84,1180.47,1203.41],
2024:[1392.33,1439.85,1470.26,1501.41,1518.13,1524.19,1553.33,1571.62,1580.65,1604.06,1604.64,1615.82],
2025:[1762.81,1784.6,1811.84,1842.02,1858.21,1883.65,1910.25,1930.24,1947.06,1966.06,1988.57,2011.76],
2026:[2210.24,2243.55,2305.42,2368.46,2412.77,2423.57,2451.41,2501.4]}
c=pd.Series([v for y in T for v in T[y]],index=pd.date_range("2015-01-01",periods=sum(len(v) for v in T.values()),freq="MS"))
fx=pd.Series({pd.Timestamp(k):v["TRY"] for k,v in json.load(open("data/usdtry.json"))["rates"].items()}).resample("MS").mean()
bis=pd.read_csv("data/QTRN628BIS.csv",parse_dates=[0],index_col=0).iloc[:,0].resample("MS").interpolate()
R=[]
for D in (18,24):
  for i in range(len(c)-D):
    t0,t1=c.index[i],c.index[i+D];cost=c.iloc[i:i+D+1].values/c.iloc[i]
    fixed=1.3/cost[-1]-1
    p=1.3
    for k in range(6,D,6):p=max(p,1.3*cost[k])  # teslimden once 6 ayda bir: fiyat=maliyet x1,30 (tavan); teslim ani guncellemesi yok
    m=p/cost[-1]-1
    row=dict(teslim=D,baslangic=t0.date(),sabit_marj=fixed,kural_marj=m,alici_carpani=p/1.3)
    if t1 in bis.index and t0 in bis.index: row["bis_konut_carpani"]=bis[t1]/bis[t0]
    if t1 in fx.index and t0 in fx.index: row["alici_usd_carpani"]=(p/1.3)*fx[t0]/fx[t1]
    R.append(row)
r=pd.DataFrame(R);r.to_csv("data/varsayimsiz_backtest.csv",index=False)
s=r.groupby("teslim").agg(kohort=("sabit_marj","size"),sabit_ort=("sabit_marj","mean"),sabit_min=("sabit_marj","min"),sabit_zarar=("sabit_marj",lambda x:(x<0).sum()),
  kural_ort=("kural_marj","mean"),kural_min=("kural_marj","min"),kural_zarar=("kural_marj",lambda x:(x<0).sum()),alici_ort=("alici_carpani","mean"),bis_ort=("bis_konut_carpani","mean"),alici_usd=("alici_usd_carpani","mean"))
print(s.round(3).to_string())
sub=r.dropna(subset=["bis_konut_carpani"]);print("alici<=BIS konut artisi orani",sub.groupby("teslim").apply(lambda g:(g.alici_carpani<=g.bis_konut_carpani).mean()).round(3).to_dict())
# Agirliklar: TUIK bina insaati maliyet endeksi (2005=100): iscilik 30,9; tesisat malz 15,6; makine 1,2; genel malz 52,3 (Yeni Asya 2006)
LAB=.309
# zimni guncel pay (Laspeyres ozdesligi, Aralik yillik degisimler, tum insaat)
y=pd.read_csv("data/ime_aralik_yillik_degisim.csv");y["zimni_malzeme_payi_onceki_aralik"]=(y.toplam-y.iscilik)/(y.malzeme-y.iscilik);print(y.round(3).to_string())
# %10 marj: yalniz cimento payi kaynakli (ODTU via TURKCIMENTO %3-5, %3,5); olcek=0; carpan=(1-FAVOK)/0,9 (FAVOK>10% ise)
M=[]
for ad,f in [("Hazir beton FAVOK %6,2 (Oyak 2025)",.062),("Akcansa FAVOK %13,6",.136),("Cimsa FAVOK %17,9",.179),("Oyak cimento FAVOK %37,9",.379)]:
  carp=min(1,(1-f)/0.9)
  for pay in (.03,.035,.05): M.append(dict(sirket=ad,cimento_payi=pay,konut_maliyet_etkisi=round(pay*(carp-1),4)))
pd.DataFrame(M).to_csv("data/varsayimsiz_marj10.csv",index=False);print(pd.DataFrame(M).to_string())
# Vergi destegi: GV+damga / isveren maliyeti; insaatta %71,4 asgari ucret (0); geri kalan dagilim kaynaksiz -> sinir: alt 0, ust = SGK ekonomi dagilimi (kaynakli)
D_=[(1,.405),(1.1,.085),(1.4,.138),(1.85,.088),(2.3,.064),(2.75,.045),(3.25,.041),(3.7,.029),(4.15,.024),(4.6,.018),(5.05,.010),(5.55,.008),(6,.006),(6.45,.005),(6.95,.004),(7.35,.003)]
num=den=0
for k,p in D_:
  gv,dm=annual(k*MW,MW*.85);num+=(gv+dm)*p;den+=k*MW*12*1.2175*p
sh=num/den;print("vergi/isveren maliyeti ust (SGK ekonomi, 7,5x ustu haric)",round(sh,4),"konut etkisi ust",round(-sh*LAB,4))
out=pd.DataFrame([dict(kalem="iscilik agirligi TUIK 2005",deger=LAB),dict(kalem="vergi payi ust sinir",deger=round(sh,4)),dict(kalem="hedefli destek konut etkisi ust sinir",deger=round(-sh*LAB,4)),
 dict(kalem="bayi marji ust sinir (genel malz 52,3% x %4)",deger=round(-.523*.04,4)),dict(kalem="bayi marji alt sinir (genel malz x %1)",deger=round(-.523*.01,4))])
out.to_csv("data/varsayimsiz_ozet.csv",index=False);print(out)
