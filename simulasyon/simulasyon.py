"""Konut platformu fiyat kurali backtest simulasyonu.
Kural: satis fiyati = 1.30 x USD maliyet; ilk 6 ay USD/TRY'ye endeksli, sonra TL sabit."""
import json, pandas as pd, numpy as np, matplotlib
matplotlib.use("Agg"); import matplotlib.pyplot as plt
D="data/"
fx=pd.Series({k:v["TRY"] for k,v in json.load(open(D+"usdtry.json"))["rates"].items()})
fx.index=pd.to_datetime(fx.index); fx=fx.resample("MS").mean().rename("usdtry")
cpi=pd.read_csv(D+"TURCPIALLMINMEI.csv",index_col=0,parse_dates=True).iloc[:,0].rename("tufe")
hpi=pd.read_csv(D+"QTRN628BIS.csv",index_col=0,parse_dates=True).iloc[:,0].rename("konut_endeks")
hpi=hpi.resample("MS").interpolate()
df=pd.concat([fx,cpi,hpi],axis=1).loc["2019-01":]
df.to_csv(D+"birlesik_aylik.csv")
# VARSAYIMLAR
COST=100_000; MAT=0.65; LAB=0.35; MARJ=0.30; ENDEKS_AY=6
def kohort(t0,T,fxs,cps):
    """T: teslim (insaat) suresi ay. Maliyet T aya esit yayilir. Gelir teslimde tahsil."""
    i0=fxs.index.get_loc(t0)
    if i0+T>=len(fxs) or i0+max(T,ENDEKS_AY)>=len(fxs): return None
    lock=fxs.iloc[i0+ENDEKS_AY]
    price_tl=(1+MARJ)*COST*(fxs.iloc[i0+T] if T<ENDEKS_AY else lock)
    c=0
    for k in range(T):
        c+=MAT*COST/T*fxs.iloc[i0+k]+LAB*COST/T*fxs.iloc[i0]*cps.iloc[i0+k]/cps.iloc[i0]
    return dict(fiyat_tl=price_tl,maliyet_tl=c,marj_nominal=price_tl/c-1,
                marj_usd=price_tl/fxs.iloc[i0+T]/COST-1)
rows=[]
d2=df.dropna(subset=["usdtry","tufe"])
for t0 in d2.index:
    for T in [6,12,18,24]:
        r=kohort(t0,T,d2.usdtry,d2.tufe)
        if r is None: continue
        h=df.konut_endeks; i0=df.index.get_loc(t0); tT=df.index[i0+T]
        piyasa=(1+MARJ)*COST*df.usdtry[t0]*h[tT]/h[t0] if pd.notna(h.get(tT)) else np.nan
        r.update(baslangic=t0.date(),teslim_ay=T,piyasa_fiyat_tl=piyasa,
                 alici_tasarruf=1-r["fiyat_tl"]/piyasa if piyasa==piyasa else np.nan)
        rows.append(r)
bt=pd.DataFrame(rows); bt.to_csv(D+"backtest_kohortlar.csv",index=False)
# Senaryolar: sentetik aylik kur artisi; TUFE aylik = kur artisi*0.9 (varsayim)
sc=[]
for ad,g in [("dusuk",0.01),("baz",0.025),("yuksek",0.04)]:
    idx=pd.date_range("2027-01-01",periods=40,freq="MS")
    f=pd.Series(40*(1+g)**np.arange(40),idx); c=pd.Series((1+0.9*g)**np.arange(40),idx)
    for T in [6,12,18,24,30]:
        r=kohort(idx[0],T,f,c); sc.append(dict(senaryo=ad,aylik_kur_artisi=g,teslim_ay=T,**r))
sc=pd.DataFrame(sc); sc.to_csv(D+"senaryolar.csv",index=False)
# Grafikler
fig,ax=plt.subplots(figsize=(10,5))
for T in [6,12,18,24]:
    s=bt[bt.teslim_ay==T]; ax.plot(pd.to_datetime(s.baslangic),s.marj_nominal*100,label=f"teslim {T} ay")
ax.axhline(0,c="k",lw=.8); ax.axhline(30,c="gray",ls="--",lw=.8)
ax.set_title("Muteahhit nominal TL marji - satisa cikis ayina gore (backtest)"); ax.set_ylabel("%"); ax.legend(); fig.tight_layout(); fig.savefig("grafik_marj_backtest.png",dpi=120); fig.savefig("grafik_marj_backtest.svg")
fig,ax=plt.subplots(figsize=(10,5))
for T in [6,12,18,24]:
    s=bt[bt.teslim_ay==T].dropna(subset=["alici_tasarruf"]); ax.plot(pd.to_datetime(s.baslangic),s.alici_tasarruf*100,label=f"teslim {T} ay")
ax.axhline(0,c="k",lw=.8); ax.set_title("Alici tasarrufu: platform fiyati vs konut fiyat endeksine gore piyasa (backtest)"); ax.set_ylabel("%"); ax.legend(); fig.tight_layout(); fig.savefig("grafik_alici_tasarruf.png",dpi=120); fig.savefig("grafik_alici_tasarruf.svg")
fig,ax=plt.subplots(figsize=(8,5))
for ad in ["dusuk","baz","yuksek"]:
    s=sc[sc.senaryo==ad]; ax.plot(s.teslim_ay,s.marj_nominal*100,marker="o",label=ad)
ax.axhline(0,c="k",lw=.8); ax.set_xlabel("teslim suresi (ay)"); ax.set_ylabel("nominal marj %"); ax.set_title("Duyarlilik: kur senaryosu x teslim suresi"); ax.legend(); fig.tight_layout(); fig.savefig("grafik_duyarlilik.png",dpi=120); fig.savefig("grafik_duyarlilik.svg")
fig,ax=plt.subplots(figsize=(10,5)); n=df/df.iloc[0]*100
n.plot(ax=ax); ax.set_title("Endeksler (2019-01=100): USD/TRY, TUFE, konut fiyat endeksi"); fig.tight_layout(); fig.savefig("grafik_veriler.png",dpi=120); fig.savefig("grafik_veriler.svg")
# Ozet
o=bt.groupby("teslim_ay").agg(ort_marj=("marj_nominal","mean"),min_marj=("marj_nominal","min"),max_marj=("marj_nominal","max"),
  zarar_kohort=("marj_nominal",lambda x:(x<0).sum()),kohort=("marj_nominal","size"),ort_usd_marj=("marj_usd","mean"),
  ort_tasarruf=("alici_tasarruf","mean"),min_tasarruf=("alici_tasarruf","min"),max_tasarruf=("alici_tasarruf","max"))
o.to_csv(D+"ozet.csv"); print(o.round(3).to_string()); print(sc.round(3).to_string())
print("zarar baslangiclari:",bt[bt.marj_nominal<0].groupby("teslim_ay").baslangic.agg(["min","max"]).to_string())
print(df.dropna().index.min(),df.dropna().index.max(), df.usdtry.last_valid_index(), df.tufe.last_valid_index(), df.konut_endeks.last_valid_index())
