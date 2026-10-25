# İstihdam: Normal (varsayımsız) ve Modüler Sistem (varsayımlı)

- **Normal senaryo:** [ISTIHDAM.md](ISTIHDAM.md) + [ISTIHDAM_SEKTOREL.md](ISTIHDAM_SEKTOREL.md). Varsayım içermez.
- **Modüler senaryo:** `istihdam_moduler.py`, çıktı `data/istihdam_moduler.csv`. Aynı veriyi kullanır: TÜİK 2025 inşaat istihdamı 2.224.000, WIOD 2014 Türkiye G-Ç tablosu ve SEA istihdamı.
- **Kapsam:** Tüm rakamlar platformun bütün sektörü kapsadığı durum içindir. Her %10 kapsam için 10'a bölün.

## 1. Varsayımlar (düşük / orta / yüksek)
| # | Varsayım | Değer | Dayanak |
|---|---|---|---|
| 1 | Alıcı fiyatındaki düşüş | %4,8 / 14,8 / 29,9 | MODULER_AG.md katman 1–6 (kendisi de varsayımlı). Yüksek değeri kanıt desteklemiyor |
| 2 | Talep esnekliği | −0,90 | Solak & Kabadayı (2016), −0,85/−0,95 ortası. TCMB (Ceritoğlu 2017) anlamsız buluyor |
| 3 | Platform konutlarında modüler/prefabrik payı | %10 / 25 / 40 | İsveç çok katlı konutta ~%45 prefabrik eleman (U of Toronto School of Cities 2024) |
| 4 | Modüler birimde toplam işçilik azalması | %10 / 20 / 30 | McKinsey (2019) "Modular construction": süre −%20–50, maliyet 0–%20. Türkiye verisi yok |
| 5 | Modüler birimde fabrikaya kayan iş payı | %60 / 70 / 85 | BoKlok'ta üretimin %85'i fabrikada (U Toronto 2024) |
| 6 | Fabrika işinin dağılımı | C16 / C23 / C25 eşit | Varsayım (ahşap, beton/prekast, çelik) |
| 7 | İnşaata bağlı toptan ticaret işinden kalkan pay | %10 / 25 / 50 | Bayi marjı %1–5 (ALTSO). İş karşılığı bilinmiyor, saf varsayım |
| 8 | İnşaata bağlı perakende işinden kalkan pay | %0 / 10 / 25 | Saf varsayım |
| 9 | Y kalemlerinde yerlilik artışı (2 yıl) | +0 / +10 / +20 puan (%55 → %55/65/75) | OLCEK_YERLILESTIRME.md |
| 10 | Y kalemlerinin girdi payı | %16 | OLCEK_YERLILESTIRME.md. İkame, inşaatın ithal ara girdisine (%28,5, WIOD 2014) uygulandı; iş C22/C27/C28'e eşit dağıtıldı |
| 11 | İnşaatta kayıt dışılık | %25 / 30 / 35 | TÜİK inşaata özgü oran yayımlamıyor. Tarım dışı ortalama %15,9 (2025 Ç4) |
| 12 | KOBİ desteğinin kayıtlı istihdama etkisi | +%5 / 9 / 13 | Betcherman, Daysal & Pagés (2010, *Labour Economics*): 5084 sayılı Kanun SGK prim teşviki, kayıtlı istihdamda +%5–13 |

## 2. Karşılaştırma (tüm sektör, 2025 bazı)
| Kalem | Normal (varsayımsız) | Modüler düşük | Modüler orta | Modüler yüksek |
|---|---|---|---|---|
| Talep artışı | %0 – 4,2–8,5 | %4,3 | %13,3 | %26,9 |
| İnşaat şantiye işi (net) | 0 – +94.520–190.152 | −52.408 | −182.608 | −411.969 |
| Fabrikaya kayan iş (C16/C23/C25) | 0 | +125.284 | +352.833 | +671.750 |
| Modüler verimlilik nedeniyle yok olan iş | 0 | −23.201 | −126.012 | −338.697 |
| Aracı tasfiyesi kaybı (G46+G47) | 0 | −12.132 | −44.061 | −105.356 |
| Yerlileştirme kaynaklı yeni imalat işi | hesaplanamaz | 0 | +5.925 | +13.271 |
| İnşaat dışı toplam (fabrika dahil) | 0 – +32.171–65.108 | +146.242 | +416.726 | +785.790 |
| **Net toplam (Tip I)** | **0 – +126.691–255.260** | **+93.834** | **+234.118** | **+373.821** |
| Kayıtlıya geçen iş (net toplamdan ayrı; mevcut işin kaydı) | hesaplanamaz | 83.400 | 140.112 | 187.928 |

## 3. Sektörel (modüler; normal değerler ISTIHDAM_SEKTOREL.md'de)
| Sektör | Normal (tüm sektör) | Düşük | Orta | Yüksek |
|---|---|---|---|---|
| C23 Çimento, seramik, cam | 0 – 4.547–9.202 | 46.438 | 132.031 | 253.048 |
| C25 Fabrikasyon metal | 0 – 1.240–2.511 | 43.037 | 121.545 | 231.865 |
| C16 Ağaç ürünleri | 0 – 1.234–2.498 | 43.031 | 121.526 | 231.825 |
| C24 Ana metal | 0 – 712–1.441 | 732 | 2.258 | 4.561 |
| C22 Plastik/PVC | 0 – 514–1.040 | 529 | 3.616 | 7.741 |
| C27 Elektrikli teçhizat | 0 – 254–514 | 261 | 2.606 | 5.659 |
| C28 Makine | 0 – 261–528 | 268 | 2.966 | 6.462 |
| C20 Kimya | 0 – 166–336 | 171 | 527 | 1.065 |
| B Madencilik | 0 – 573–1.160 | 589 | 1.817 | 3.672 |
| D35 Enerji | 0 – 357–723 | 368 | 1.133 | 2.290 |
| H49 Kara taşımacılığı | 0 – 1.962–3.970 | 2.018 | 6.221 | 12.568 |
| G46 Toptan ticaret | 0 – 5.129–10.381 | −6.856 | −16.811 | −41.591 |
| G47 Perakende | 0 – 4.258–8.617 | 4.379 | 2.520 | −3.621 |
| K64 Finans | 0 – 849–1.718 | 873 | 2.692 | 5.439 |
| N İdari destek | 0 – 908–1.837 | 934 | 2.879 | 5.816 |

## 4. Okuma
- Modüler senaryoda iş **şantiyeden fabrikaya kayar**. İnşaat istihdamı (NACE F) düşerken imalat (C16/C23/C25) artar. Net etki pozitif, ancak bunun ana kaynağı varsayım 1, yani fiyat düşüşü ve ondan doğan talep artışı.
- **Talep artışını sıfırlarsak** (esneklik anlamsız) geriye yalnız kayma kalır: verimlilik kaybı ve aracı kaybı. Orta senaryoda net yaklaşık −170 bin olur. Bu hesap script'te ayrıca yapılmadı; değer, verimlilik kaybı ve aracı kaybından kaba bir türetmedir.
- Yüksek senaryo (−%30 fiyat, +%27 talep) kanıtla desteklenmez. Gerçekçi bant düşük ile orta arasıdır.
- Kayıtlıya geçiş yeni iş değildir. Mevcut işin SGK'ya girmesidir.
- Tip II (uyarılmış tüketim) etkisi dahil değildir.
