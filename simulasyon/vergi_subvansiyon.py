"""Gelir vergisi istisnasini yoksulluk sinirina yukseltme (A) ve sigorta disi isgucu maliyeti subvansiyonu (B). 2026 parametreleri kaynakli; dagilim/egilimler VARSAYIM (VERGI_SUBVANSIYON.md)."""
import pandas as pd,numpy as np
MW=33030.0;SGK_I=.15;SGK_E=.1975+.02;DAMGA=.00759   # GIB/CSGB 2026; isveren %21,75-2 puan + issizlik %2
BR=[(190000,.15),(400000,.20),(1500000,.27),(5300000,.35),(1e18,.40)]
def tax(c):  # kumulatif yillik matrah icin vergi (ucret tarifesi 2026)
    t=0;lo=0
    for hi,r in BR:
        if c>lo: t+=(min(c,hi)-lo)*r
        lo=hi
    return t
def annual(gross_m,ex_base_m):
    """yillik GV (istisna sonrasi). Istisna = ex_base_m matrahinin kumulatif vergisi, kisi vergisini asmaz (ay ay)."""
    g=0;e=0;GV=0
    for m in range(12):
        b=gross_m*(1-SGK_I);g_prev,e_prev=g,e;g+=b;e+=ex_base_m
        GV+=max(0,(tax(g)-tax(g_prev))-(tax(e)-tax(e_prev)))
    dam=max(0,gross_m-MW)*DAMGA*12
    return GV,dam
SC={"Mevcut (istisna=asgari ucret)":MW*(1-SGK_I),"A1 istisna=bekar yasam maliyeti (48.885 TL)":48884.82,"A2 istisna=yoksulluk siniri (123.130 TL)":123130.0}
rows=[]
for k in [1,1.3,1.6,2,2.5]:
    G=k*MW
    for s,eb in SC.items():
        gv,dm=annual(G,eb);net=G*12*(1-SGK_I)-gv-dm;cost=G*12*(1+SGK_E)
        rows.append(dict(kat=k,brut_ay=round(G),senaryo=s,net_ay=round(net/12),gv_ay=round(gv/12),damga_ay=round(dm/12),net_brut=round(net/(G*12),4),net_isveren=round(net/cost,4)))
r=pd.DataFrame(rows);r.to_csv("data/vergi_oranlar.csv",index=False);print(r.to_string())
# SGK 2025 yil sonu dagilimi (asgari ucret kati, pay) -> 2026'ya kat olarak tasindi (VARSAYIM); bant orta noktasi
D=[(1,.405),(1.1,.085),(1.4,.138),(1.85,.088),(2.3,.064),(2.75,.045),(3.25,.041),(3.7,.029),(4.15,.024),(4.6,.018),(5.05,.010),(5.55,.008),(6,.006),(6.45,.005),(6.95,.004),(7.35,.003),(10,.030)]
N=16.94e6;NC=2126760
def construction_dist():  # VARSAYIM: insaatta %71,4 asgari ucret civari (TCMB 2021), kalan ekonominin >1,1 dagilimi ile
    rest=[(k,p) for k,p in D if k>1.1];s=sum(p for _,p in rest)
    return [(1,.714)]+[(k,p/s*.286) for k,p in rest]
def total(dist,n,eb):
    T=0;netgain=0;base=0
    for k,p in dist:
        gv0,dm0=annual(k*MW,SC["Mevcut (istisna=asgari ucret)"]);gv1,_=annual(k*MW,eb)
        T+=(gv0-gv1)*p*n;base+=gv0*p*n
    return T,base
out=[]
MPC=(0.6,0.8,0.9);ETAX=(6.952e12*0+3.993e12+2.532e12)/(.60*77.2574e12)   # KDV+OTV 2026 butce / (VARSAYIM ozel tuketim=GSYH %60)
REG=(0.005,0.01,0.02)  # VARSAYIM: kayitli istihdam artisi (dusuk/orta/yuksek); Betcherman vd. 2010 bolgesel tesviklerde %5-15 (cok daha buyuk maliyet dusuşu)
PRIM=(SGK_I+SGK_E)*MW*12   # asgari ucretli yeni kayitli calisan basi yillik prim
for s in list(SC)[1:]:
    eb=SC[s]
    for ad,dist,n in [("ekonomi geneli",D,N),("insaat",construction_dist(),NC)]:
        L,B=total(dist,n,eb)
        for j,lab in enumerate(["dusuk","orta","yuksek"]):
            vat=L*MPC[j]*ETAX;reg=n*REG[j]*PRIM*(1 if ad=="ekonomi geneli" else 1)
            out.append(dict(senaryo=s,kapsam=ad,geri_donus=lab,ucret_GV_model_mevcut_mrd=round(B/1e9,1),GV_kaybi_mrd=round(L/1e9,1),
              KDV_OTV_geri_donus_mrd=round(vat/1e9,1),kayitlilik_prim_mrd=round(reg/1e9,1),net_mali_etki_mrd=round((-L+vat+reg)/1e9,1),
              kayip_GV_butcesi_orani=round(L/3.55811e12,4)))
o=pd.DataFrame(out);o.to_csv("data/vergi_mali_etki.csv",index=False);print(o.to_string());print("ETAX",round(ETAX,4))
# Senaryo B: insaatta sigorta disi kesintiler (GV+damga) devlet tarafindan; net ucret sozlesmesi varsayimi -> isveren maliyeti duser
LAB=(.38,.42)
bd=[];tot=0
for k,p in construction_dist():
    gv,dm=annual(k*MW,SC["Mevcut (istisna=asgari ucret)"]);cost=k*MW*12*(1+SGK_E);bd.append((k,p,(gv+dm)/cost));tot+=(gv+dm)*p*NC
share=sum(p*s*k for k,p,s in bd)/sum(p*k for k,p,_ in bd)
print("B: vergi/isveren maliyeti agirlikli",round(share,4),"konut maliyet etkisi",[round(-share*l,4) for l in LAB],"mali maliyet insaat mrd",round(tot/1e9,1))
pd.DataFrame([dict(kalem="insaat GV+damga / isveren maliyeti (agirlikli)",deger=round(share,4)),
 dict(kalem="konut birim maliyet etkisi (isclik payi %38)",deger=round(-share*.38,4)),dict(kalem="konut birim maliyet etkisi (iscilik payi %42)",deger=round(-share*.42,4)),
 dict(kalem="mali maliyet, tum insaat (mrd TL/yil)",deger=round(tot/1e9,1)),
 dict(kalem="mali maliyet, platform KOBI %10 (VARSAYIM)",deger=round(tot*.10/1e9,1)),dict(kalem="mali maliyet, platform KOBI %20 (VARSAYIM)",deger=round(tot*.20/1e9,1))]).to_csv("data/subvansiyon_B.csv",index=False)
