"""Oynaklik araclari backtesti (orta olcek-yerlilestirme senaryosu uzerine). Tum parametreler VARSAYIM (OYNAKLIK_ARACLARI.md)."""
import pandas as pd,numpy as np,matplotlib;matplotlib.use("Agg");import matplotlib.pyplot as plt
src=open("girdi_gruplari.py").read().split("rows=[]")[0];ns={};exec(src,ns)
d,GIRDI,LAB,COST,MARJ=ns["d"],ns["GIRDI"],ns["LAB"],ns["COST"],ns["MARJ"]
W1,W2,W3,M2,M3=.70,.10,.20,.60,.50;WY=W2*M2+W3*M3
f=lambda m,s:(1 if m is None else (1-m)/.9)*(1-s)
m1,s1,y,my,sy=.179,.05,.65,.15,.05   # orta senaryo
import os;DELTA=float(os.environ.get("DELTA",".05"))      # VARSAYIM: koridor yari genisligi (6 aylik degisimde trend +-5 puan)
STOK=.50       # VARSAYIM: G1 icinde stoklanabilir pay (celik/cimento/agrega)
R_STOK=.07     # VARSAYIM: stok tasima maliyeti yillik reel (%5 reel finansman + %2 depolama)
STOK_AY=3      # VARSAYIM: tampon stok = 3 aylik tuketim
mz,fx,lc=d.malzeme,d.usdtry,d.iscilik
g3=.5*mz+.5*fx;yi=y*mz+(1-y)*fx
parts={"g1s":GIRDI*W1*f(m1,s1)*STOK*mz,"g1n":GIRDI*W1*f(m1,s1)*(1-STOK)*mz,
 "fx":GIRDI*(W2*(1-M2)*fx+W3*(1-M3)*g3),"y":GIRDI*WY*f(my,sy)*yi,"lab":LAB*lc}
base0={k:v.iloc[0] for k,v in parts.items()}
def idx(keys):  # Aralik 2019 agirlikli sepet
    return sum(parts[k]/parts[k].iloc[0]*base0[k] for k in keys)
CI=idx(parts)                 # tam maliyet endeksi (orta senaryo)
def trend(ser,t):  # son 24 ayin ortalama 6 aylik degisimi (veri gecmisi; en az 12 ay)
    h=[ser.iloc[j]/ser.iloc[j-6]-1 for j in range(max(6,t-24),t+1)]
    return np.mean(h) if t>=12 else None
def corridor(ser,i0,T=24):   # kohort bazli: her 6 ayda birikmis farki kapatmaya calisan, trend+-DELTA ile sinirli guncelleme
    b=[1.0];c=[1.0]
    for k in range(6,T+1,6):
        t=i0+k;tgt=ser.iloc[t]/ser.iloc[i0]
        g=tgt/b[-1]-1;tr=trend(ser,t-6)
        if tr is not None: g=float(np.clip(g,tr-DELTA,tr+DELTA))
        if k==T: g=tgt/b[-1]-1 if False else g
        b.append(b[-1]*(1+g));c.append(tgt)
    return np.array(b),np.array(c)
s_part=parts["g1s"]/parts["g1s"].iloc[0]*base0["g1s"]
fx_part=parts["fx"]+GIRDI*WY*f(my,sy)*(1-y)*fx
def path(ad,i0,T=24):
    ks=range(0,T+1,6);ci=np.array([CI.iloc[i0+k]/CI.iloc[i0] for k in ks])
    if ad=="orta (arac yok)": return ci
    if ad=="A1 koridor+istikrar fonu": return corridor(CI,i0)[0]
    if ad=="A2 tampon stok":
        sb,sc=corridor(s_part,i0);w=s_part.iloc[i0]/CI.iloc[i0];return ci-w*sc+w*sb
    if ad=="A3 kur forward hedge":  # kur bagli kisim bir onceki inceleme noktasinda forward ile sabitlenir; prim VARSAYIM=son 12 ay kur artisinin yarisi
        out=[1.0]
        for k in list(ks)[1:]:
            t=i0+k;r=t-6;prem=(fx.iloc[r]/fx.iloc[max(0,r-12)])**0.5
            fl=fx.iloc[r]*prem;v=(CI.iloc[t]-fx_part.iloc[t]+fx_part.iloc[t]*fl/fx.iloc[t])/CI.iloc[i0];out.append(v)
        return np.array(out)
    if ad=="A1+A2 kombinasyon":
        p2=path("A2 tampon stok",i0);b=[1.0]
        for j,k in enumerate(list(ks)[1:],1):
            g=p2[j]/b[-1]-1;tr=trend(CI,i0+k-6)
            if tr is not None:g=float(np.clip(g,tr-DELTA,tr+DELTA))
            b.append(b[-1]*(1+g))
        return np.array(b)
TOOLS=["orta (arac yok)","A1 koridor+istikrar fonu","A2 tampon stok","A3 kur forward hedge","A1+A2 kombinasyon"]
rows=[];upd=[];T=24
for ad in TOOLS:
  for i0 in range(len(d)-T):
    pb=path(ad,i0);ci=CI.iloc[i0:i0+T+1]/CI.iloc[i0];C=sum(COST/T*ci.iloc[k] for k in range(T))
    P0=(1+MARJ)*COST
    Pc=min(P0*ci.iloc[T],(1+MARJ)*C)                       # muteahhide odenen (maliyet bazli kural)
    Pb=Pc if ad=="orta (arac yok)" else Pc*pb[-1]/(CI.iloc[i0+T]/CI.iloc[i0])  # alici: maliyet bazli fiyat x (arac endeksi/maliyet endeksi); fark fondan
    stock=0
    if ad in("A2 tampon stok","A1+A2 kombinasyon"):
        stock=sum(COST/T*(s_part.iloc[i0+k]/CI.iloc[i0])*STOK_AY*R_STOK/12 for k in range(T))
    fon=Pc-Pb if ad!="orta (arac yok)" else 0
    rows.append(dict(arac=ad,baslangic=d.index[i0].date(),alici_fiyat=Pb/COST,muteahhit_marj=Pc/C-1,
       fon_net=fon/COST,stok_maliyet=stock/COST,platform_toplam=(fon+stock)/COST))
    for k in range(6,25,6): upd.append(dict(arac=ad,degisim=pb[k//6]/pb[k//6-1]-1))
bt=pd.DataFrame(rows);u=pd.DataFrame(upd)
o=bt.groupby("arac").agg(alici_fiyat=("alici_fiyat","mean"),alici_fiyat_std=("alici_fiyat","std"),
   muteahhit_marj=("muteahhit_marj","mean"),min_marj=("muteahhit_marj","min"),
   fon_net_ort=("fon_net","mean"),fon_max_odeme=("fon_net","max"),stok_maliyet=("stok_maliyet","mean"),platform_toplam=("platform_toplam","mean"))
v=u.groupby("arac").degisim.agg(ort="mean",std="std",p10=lambda x:x.quantile(.1),p90=lambda x:x.quantile(.9))
o=o.join(v);o["kohort_CV"]=o.alici_fiyat_std/o.alici_fiyat;o=o.loc[TOOLS]
o.round(4).to_csv("data/oynaklik_araclari_ozet.csv");bt.to_csv("data/oynaklik_araclari_backtest.csv",index=False)
print(o.round(4).T.to_string())
fig,ax=plt.subplots(1,2,figsize=(13,5))
ax[0].bar(range(len(TOOLS)),o["std"]*100,color=["gray","C0","C1","C2","C3"]);ax[0].set_xticks(range(len(TOOLS)),[a.split()[0] for a in TOOLS]);ax[0].set_title("6 aylik alici fiyat guncellemesi std (puan)")
for j,v in enumerate(o["std"]*100): ax[0].text(j,v+.1,f"{v:.1f}",ha="center")
ax[1].boxplot([u[u.arac==a].degisim*100 for a in TOOLS],tick_labels=[a.split()[0] for a in TOOLS]);ax[1].set_title("6 aylik guncelleme % dagilimi (24 ay teslim, Ara 2019-Ara 2025)")
fig.tight_layout();fig.savefig("grafik_oynaklik_araclari.png",dpi=120);fig.savefig("grafik_oynaklik_araclari.svg")
