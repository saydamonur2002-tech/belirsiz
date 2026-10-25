"""G1 KOBI mekanizmasi: G1 fiyatinin mevcut marjdan %10 marja inmesi + olcek kademesine bagli birim maliyet dususu.
Mevcut marjlar = FAVOK marji (kaynakli, 2025) satis fiyatindaki pay olarak VARSAYILIR; olcek dususleri VARSAYIM."""
import pandas as pd,numpy as np,matplotlib;matplotlib.use("Agg");import matplotlib.pyplot as plt
import importlib.util,sys
spec=importlib.util.spec_from_file_location("gg","girdi_gruplari.py")
src=open("girdi_gruplari.py").read().split("rows=[]")[0];ns={};exec(src,ns)
d,W,GIRDI,LAB,COST,MARJ=ns["d"],ns["W"],ns["GIRDI"],ns["LAB"],ns["COST"],ns["MARJ"]
MARJLAR={"mevcut (degisiklik yok)":None,"hazir beton FAVOK %6,2 (Oyak 2025)":.062,"Akcansa FAVOK %13,6 (2025)":.136,
 "Cimsa FAVOK %17,9 (2025)":.179,"Oyak konsolide FAVOK %25,9 (2025)":.259,"Oyak cimento FAVOK %37,9 (2025)":.379}
OLCEK=[0,.05,.10]
def faktor(m0,s): return 1.0 if m0 is None else (1-m0)/0.9*(1-s)
def marj(i0,T,f):
    fx0=d.usdtry.iloc[i0];mz=d.malzeme/d.malzeme.iloc[i0];fr=d.usdtry/fx0;lc=d.iscilik/d.iscilik.iloc[i0]
    g=W["G1_olcekli"]*f*mz+W["G2_ithal_makine"]*fr+W["G3_sinirli_yerli"]*(.5*mz+.5*fr)
    c=sum(GIRDI*COST/T*fx0*g.iloc[i0+k]+LAB*COST/T*fx0*lc.iloc[i0+k] for k in range(T))
    return (1+MARJ)*COST*d.usdtry.iloc[i0+6]/c-1
rows=[]
for ad,m0 in MARJLAR.items():
  for s in (OLCEK if m0 is not None else [0]):
    f=faktor(m0,s);r=dict(senaryo=ad,olcek_dusus=s,g1_fiyat_carpani=round(f,4),
      konut_maliyet_degisimi=round(GIRDI*W["G1_olcekli"]*(f-1),4))
    for T in [18,24]:
      ms=[marj(i0,T,f) for i0 in range(len(d)-T)]
      r[f"marj_ort_{T}"]=round(np.mean(ms),4);r[f"marj_min_{T}"]=round(min(ms),4);r[f"zarar_{T}"]=int(sum(m<0 for m in ms));r[f"kohort_{T}"]=len(ms)
    rows.append(r)
o=pd.DataFrame(rows);o.to_csv("data/g1_kobi_senaryolar.csv",index=False);print(o.to_string())
fig,ax=plt.subplots(1,2,figsize=(12,5))
for j,T in enumerate([18,24]):
  for s,c in zip(OLCEK,["tab:gray","tab:blue","tab:green"]):
    sub=o[(o.olcek_dusus==s)&o.senaryo.str.contains("FAVOK")]
    ax[j].plot([x.split(" (")[0] for x in sub.senaryo],sub[f"marj_ort_{T}"]*100,"o-",c=c,label=f"olcek dususu %{int(s*100)} (varsayim)")
  b=o[o.senaryo.str.startswith("mevcut")][f"marj_ort_{T}"].iloc[0]*100
  ax[j].axhline(b,c="r",ls="--",label="mevcut (G1 degisiklik yok)");ax[j].axhline(0,c="k",lw=.6)
  ax[j].set_title(f"{T} ay teslim - ort. muteahhit marji %");ax[j].tick_params(axis="x",rotation=30,labelsize=7);ax[j].legend(fontsize=7)
fig.suptitle("G1 %10 marj tavani + olcek kademesi: mevcut G1 marj senaryosuna gore");fig.tight_layout()
fig.savefig("grafik_g1_kobi.png",dpi=120);fig.savefig("grafik_g1_kobi.svg")
