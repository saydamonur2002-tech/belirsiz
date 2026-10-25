# Varsayımsız istihdam etkisi: yalnızca yayımlanmış kaynak değerlerle
L = 2_224_000          # TÜİK 2025 inşaat istihdamı (NACE F)
fiyat = (-0.05, -0.09) # VARSAYIMSIZ.md: alıcı USD bazında %5-9 az öder
esneklik = {"Solak&Kabadayi_2016": (-0.85, -0.95), "Ceritoglu_2017_TCMB(anlamsiz)": (0.0, 0.0)}
tip2 = 1.678           # Gül&Çakaloğlu: inşaat kesikli Tip II istihdam çarpanı, 2014
print("kaynak,fiyat,esneklik,talep_%,dogrudan_ust,toplam_tip2_ust,kapsam10_dogrudan")
for k,(e1,e2) in esneklik.items():
  for p in fiyat:
    for e in (e1,e2):
      d = p*e + 0.0
      print(f"{k},{p},{e},{abs(d)*100 if d else 0:.1f},{L*d:.0f},{L*d*tip2:.0f},{L*d*0.1:.0f}")
