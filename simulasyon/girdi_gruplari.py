"""Grup bazli endeksleme ile simulasyon. Grup agirliklari VARSAYIMDIR."""
import json,pandas as pd,numpy as np,matplotlib
matplotlib.use("Agg");import matplotlib.pyplot as plt
idx=pd.read_csv("data/girdi_endeks_aralik2019_100.csv",parse_dates=["tarih"]).set_index("tarih")
fx=pd.Series({k:v["TRY"] for k,v in json.load(open("data/usdtry.json"))["rates"].items()});fx.index=pd.to_datetime(fx.index);fxm=fx.resample("MS").mean()
m=np.exp(np.log(idx[["malzeme","iscilik"]]).resample("MS").interpolate())
d=pd.concat([fxm.rename("usdtry"),m],axis=1).loc["2019-12":"2025-12"].dropna()
COST=100_000;GIRDI=.65;LAB=.35;MARJ=.30
# VARSAYIM: girdi (iscilik haric) icindeki grup paylari
W={"G1_olcekli":.70,"G2_ithal_makine":.10,"G3_sinirli_yerli":.20}
def senaryo(i0,T,mode):
    fx0=d.usdtry.iloc[i0];f=d.usdtry/fx0;mz=d.malzeme/d.malzeme.iloc[i0];lc=d.iscilik/d.iscilik.iloc[i0]
    if mode=="tek_endeks_malzeme": g=mz
    elif mode=="tek_endeks_kur": g=f
    else: g=W["G1_olcekli"]*mz+W["G2_ithal_makine"]*f+W["G3_sinirli_yerli"]*(.5*mz+.5*f)
    c=sum(GIRDI*COST/T*fx0*g.iloc[i0+k]+LAB*COST/T*fx0*lc.iloc[i0+k] for k in range(T))
    if mode=="grup_bazli_fiyat":  # ONERI: 6. ayda kilitlenen fiyatin yarisi, teslime kadar grup bazli maliyet endeksine (girdi+iscilik) baglanir
        k=min(T,6);lock=(1+MARJ)*COST*d.usdtry.iloc[i0+k]
        ce=GIRDI*g+LAB*lc;p=lock*(0.5+0.5*ce.iloc[i0+T]/ce.iloc[i0+k])
    else:
        p=(1+MARJ)*COST*(d.usdtry.iloc[i0+T] if T<6 else d.usdtry.iloc[i0+6])
    return p/c-1
rows=[]
for i0,t0 in enumerate(d.index):
  for T in [6,12,18,24]:
    if i0+max(T,6)>=len(d):continue
    for mode in ["tek_endeks_kur","tek_endeks_malzeme","grup_bazli_maliyet","grup_bazli_fiyat"]:
      rows.append(dict(baslangic=t0.date(),teslim_ay=T,model=mode,marj_nominal=senaryo(i0,T,mode)))
bt=pd.DataFrame(rows);bt.to_csv("data/backtest_grup_bazli.csv",index=False)
o=bt.groupby(["teslim_ay","model"]).marj_nominal.agg(kohort="size",ort="mean",min="min",zarar=lambda x:(x<0).sum())
o.round(4).to_csv("data/ozet_grup_bazli.csv");print(o.round(3).to_string())
# grup endeksleri dolar bazinda
g1=d.malzeme/d.malzeme.iloc[0];g2=d.usdtry/d.usdtry.iloc[0];g3=.5*g1+.5*g2
fig,ax=plt.subplots(figsize=(10,5))
for T,c in [(12,"tab:blue"),(24,"tab:red")]:
  for mode,ls in [("tek_endeks_malzeme","--"),("grup_bazli_maliyet","-"),("grup_bazli_fiyat",":")]:
    s=bt[(bt.teslim_ay==T)&(bt.model==mode)];ax.plot(pd.to_datetime(s.baslangic),s.marj_nominal*100,c=c,ls=ls,label=f"{T} ay - {mode}")
ax.axhline(0,c="k",lw=.8);ax.axhline(30,c="gray",lw=.6,ls="--");ax.set_ylabel("nominal marj %")
ax.set_title("Grup bazli endeksleme: mevcut kural vs grup endeksli fiyat (oneri)");ax.legend(fontsize=7);fig.tight_layout()
fig.savefig("grafik_grup_bazli_marj.png",dpi=120);fig.savefig("grafik_grup_bazli_marj.svg")
