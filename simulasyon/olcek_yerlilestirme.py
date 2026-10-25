"""Olcek modeline yerlilestirilen kalemlerin eklenmesi. Tum paylar/oranlar VARSAYIM etiketlidir (bkz. OLCEK_YERLILESTIRME.md)."""
import pandas as pd,numpy as np,matplotlib;matplotlib.use("Agg");import matplotlib.pyplot as plt
src=open("girdi_gruplari.py").read().split("rows=[]")[0];ns={};exec(src,ns)
d,GIRDI,LAB,COST,MARJ=ns["d"],ns["GIRDI"],ns["LAB"],ns["COST"],ns["MARJ"]
# girdi icindeki paylar (VARSAYIM): G1 %70, G2 %10, G3 %20; yerlilestirilen: G2'nin %60'i, G3'un %50'si
W1,W2,W3=.70,.10,.20;M2,M3=.60,.50;WY=W2*M2+W3*M3
SC={ # ad: (G1 mevcut marj, G1 olcek, Y-kalem yerlilik, Y mevcut marj, Y olcek)
 "temel (mevcut yapi)":None,
 "dusuk":(.136,0,.55,None,0),
 "orta":(.179,.05,.65,.15,.05),
 "yuksek":(.259,.10,.75,.20,.10)}
f=lambda m,s:(1 if m is None else (1-m)/.9)*(1-s)
def ci_series(i0,p):
    fx=d.usdtry/d.usdtry.iloc[i0];mz=d.malzeme/d.malzeme.iloc[i0];lc=d.iscilik/d.iscilik.iloc[i0];g3=.5*mz+.5*fx
    if p is None: g=W1*mz+W2*fx+W3*g3
    else:
        m1,s1,y,my,sy=p;yi=y*mz+(1-y)*fx
        g=W1*f(m1,s1)*mz+W2*(1-M2)*fx+W3*(1-M3)*g3+WY*f(my,sy)*yi
    return GIRDI*g+LAB*lc
rows=[];upd=[]
for ad,p in SC.items():
  for T in [12,18,24,30]:
    for i0 in range(len(d)-T):
      ci=ci_series(i0,p);C=sum(COST/T*ci.iloc[i0+k] for k in range(T))
      P0=(1+MARJ)*COST*ci.iloc[i0];r=(T//6)*6;P=min(P0*ci.iloc[i0+r]/ci.iloc[i0],(1+MARJ)*C)
      rows.append(dict(senaryo=ad,teslim_ay=T,baslangic=d.index[i0].date(),marj=P/C-1,alici_fiyat=P/COST,
        fiyat_carpani=P/P0,birim_maliyet_t0=ci.iloc[i0]))
      if T==24:
        for k in range(6,25,6): upd.append(dict(senaryo=ad,degisim=ci.iloc[i0+k]/ci.iloc[i0+k-6]-1))
bt=pd.DataFrame(rows);bt.to_csv("data/backtest_olcek_yerlilestirme.csv",index=False)
u=pd.DataFrame(upd)
o=bt.groupby(["senaryo","teslim_ay"]).agg(ort_marj=("marj","mean"),min_marj=("marj","min"),zarar=("marj",lambda x:int((x<0).sum())),
   alici_fiyat=("alici_fiyat","mean"),fiyat_carpani_ort=("fiyat_carpani","mean"),fiyat_carpani_std=("fiyat_carpani","std"))
o["kohort_yayilim_CV"]=o.fiyat_carpani_std/o.fiyat_carpani_ort
v=u.groupby("senaryo").degisim.agg(ort="mean",std="std",p10=lambda x:x.quantile(.1),p90=lambda x:x.quantile(.9))
b=o.xs("temel (mevcut yapi)",level=0).alici_fiyat
o["alici_fiyat_temele_gore"]=o.alici_fiyat/o.index.get_level_values(1).map(b)-1
o.round(4).to_csv("data/ozet_olcek_yerlilestirme.csv");v.round(4).to_csv("data/oynaklik_6ay_guncelleme.csv")
st={ad:(GIRDI*((W1*(f(p[0],p[1])-1))+WY*(f(p[3],p[4])-1)) if p else 0) for ad,p in SC.items()}
pd.Series(st,name="t0_birim_maliyet_degisimi").round(4).to_csv("data/statik_maliyet_dususu.csv")
print(o.round(3).to_string());print(v.round(4));print(st)
fig,ax=plt.subplots(1,2,figsize=(12,4.8))
for ad in SC: s=o.loc[ad];ax[0].plot(s.index,s.alici_fiyat_temele_gore*100,"o-",label=ad)
ax[0].set_title("Alici fiyati, temel senaryoya gore % (6 aylik maliyet bazli kural)");ax[0].set_xlabel("teslim ay");ax[0].legend(fontsize=7);ax[0].axhline(0,c="k",lw=.6)
ax[1].boxplot([u[u.senaryo==ad].degisim*100 for ad in SC],tick_labels=list(SC));ax[1].set_title("6 aylik fiyat guncellemesi % dagilimi (24 ay teslim)");ax[1].tick_params(labelsize=7)
fig.tight_layout();fig.savefig("grafik_olcek_yerlilestirme.png",dpi=120);fig.savefig("grafik_olcek_yerlilestirme.svg")
