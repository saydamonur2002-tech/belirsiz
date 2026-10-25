"""TUIK Insaat Maliyet Endeksi (malzeme/iscilik) yillik degisimleri ile girdi analizi ve simulasyonun yeniden calistirilmasi."""
import json,pandas as pd,numpy as np,matplotlib
matplotlib.use("Agg");import matplotlib.pyplot as plt
# TUIK haber bultenleri (Aralik ayi, onceki yilin ayni ayina gore %), kaynaklar GIRDI_VERILERI.md'de
yoy=pd.DataFrame({"yil":[2020,2021,2022,2023,2024,2025],
 "toplam":[25.02,67.74,78.40,67.31,34.27,24.50],
 "malzeme":[30.34,85.77,75.93,54.26,26.18,21.47],
 "iscilik":[13.74,24.01,87.41,111.83,54.35,30.67]})
yoy.to_csv("data/ime_aralik_yillik_degisim.csv",index=False)
idx=pd.DataFrame({"tarih":pd.to_datetime([f"{y}-12-01" for y in range(2019,2026)])})
for k in ["toplam","malzeme","iscilik"]:
    idx[k]=100*np.concatenate([[1],np.cumprod(1+yoy[k]/100)])
fx=pd.Series({k:v["TRY"] for k,v in json.load(open("data/usdtry.json"))["rates"].items()});fx.index=pd.to_datetime(fx.index)
fxm=fx.resample("MS").mean()
idx["usdtry_aralik_ort"]=fxm.reindex(idx.tarih).values
for k in ["toplam","malzeme","iscilik"]:
    idx[k+"_usd"]=idx[k]/(idx.usdtry_aralik_ort/idx.usdtry_aralik_ort.iloc[0])
# kontrol: hakedis.org toplam endeks seviyeleri (2015=100) Aralik
lvl={2019:192.25,2020:240.35,2021:403.16,2022:719.25,2023:1203.41,2024:1615.82,2025:2011.76}
idx["toplam_seviye_kontrol"]=[100*lvl[y]/lvl[2019] for y in range(2019,2026)]
idx.round(2).to_csv("data/girdi_endeks_aralik2019_100.csv",index=False);print(idx.round(1).to_string())
# Grafik
fig,ax=plt.subplots(figsize=(9,5))
for k,l in [("malzeme_usd","Malzeme (USD)"),("iscilik_usd","Iscilik (USD)"),("toplam_usd","Toplam (USD)")]:ax.plot(idx.tarih.dt.year,idx[k],marker="o",label=l)
ax.axhline(100,c="k",lw=.8);ax.set_title("TUIK Insaat Maliyet Endeksi - dolar bazinda (Aralik 2019=100)");ax.set_ylabel("endeks");ax.legend();fig.tight_layout()
fig.savefig("grafik_girdi_usd.png",dpi=120);fig.savefig("grafik_girdi_usd.svg")
fig,ax=plt.subplots(figsize=(9,5))
for k,l in [("malzeme","Malzeme (TL)"),("iscilik","Iscilik (TL)")]:ax.plot(idx.tarih.dt.year,idx[k],marker="o",label=l)
ax.plot(idx.tarih.dt.year,100*idx.usdtry_aralik_ort/idx.usdtry_aralik_ort.iloc[0],marker="s",ls="--",label="USD/TRY")
ax.set_yscale("log");ax.set_title("Malzeme ve iscilik endeksi vs kur (TL, Aralik 2019=100, log)");ax.legend();fig.tight_layout()
fig.savefig("grafik_girdi_tl_vs_kur.png",dpi=120);fig.savefig("grafik_girdi_tl_vs_kur.svg")
# Simulasyonu gercek endekslerle yeniden calistir: aylik geometrik enterpolasyon (Aralik noktalari arasi)
m=idx.set_index("tarih")[["malzeme","iscilik"]];m=np.exp(np.log(m).resample("MS").interpolate())
d=pd.concat([fxm.rename("usdtry"),m],axis=1).loc["2019-12":"2025-12"].dropna()
COST=100_000;MAT=.65;LAB=.35;MARJ=.30
rows=[]
for i0,t0 in enumerate(d.index):
  for T in [6,12,18,24]:
    if i0+max(T,6)>=len(d):continue
    price=(1+MARJ)*COST*(d.usdtry.iloc[i0+T] if T<6 else d.usdtry.iloc[i0+6])
    for ad,mc in [("eski_girdi=kur",d.usdtry/d.usdtry.iloc[i0]),("yeni_girdi=TUIK_malzeme",d.malzeme/d.malzeme.iloc[i0])]:
      lc=d.iscilik/d.iscilik.iloc[i0]
      c=sum(MAT*COST/T*d.usdtry.iloc[i0]*mc.iloc[i0+k]+LAB*COST/T*d.usdtry.iloc[i0]*lc.iloc[i0+k] for k in range(T))
      rows.append(dict(baslangic=t0.date(),teslim_ay=T,model=ad,marj_nominal=price/c-1,marj_usd=price/d.usdtry.iloc[i0+T]/COST-1))
bt=pd.DataFrame(rows);bt.to_csv("data/backtest_gercek_girdi.csv",index=False)
o=bt.groupby(["teslim_ay","model"]).agg(kohort=("marj_nominal","size"),ort_marj=("marj_nominal","mean"),min_marj=("marj_nominal","min"),zarar=("marj_nominal",lambda x:(x<0).sum()),ort_usd=("marj_usd","mean"))
o.round(4).to_csv("data/ozet_gercek_girdi.csv");print(o.round(3).to_string())
fig,ax=plt.subplots(figsize=(10,5))
for (T,mdl),s in bt[bt.teslim_ay.isin([12,24])].groupby(["teslim_ay","model"]):
  ax.plot(pd.to_datetime(s.baslangic),s.marj_nominal*100,ls="-" if "TUIK" in mdl else "--",label=f"{T} ay - {mdl}")
ax.axhline(0,c="k",lw=.8);ax.set_title("Muteahhit nominal marji: girdi=kur vs girdi=TUIK malzeme endeksi (iscilik=TUIK iscilik)");ax.set_ylabel("%");ax.legend(fontsize=8);fig.tight_layout()
fig.savefig("grafik_marj_gercek_girdi.png",dpi=120);fig.savefig("grafik_marj_gercek_girdi.svg")
