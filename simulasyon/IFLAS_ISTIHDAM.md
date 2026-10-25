# İflasları önleme ve korunan istihdam (varsayımsız)

Soru: Model iflasları durdurup istihdamı koruyor mu? Hesap [iflas_istihdam.py](iflas_istihdam.py), sonuç [data/iflas_istihdam.csv](data/iflas_istihdam.csv).

## Kaynaklı veriler
| Veri | Değer | Kaynak |
|---|---|---|
| Kapanan bina inşaatı firması, 2025 İlk yarı | 1.652 (862 şahıs, 691 Ltd, 99 AŞ) | TOBB (Konkordatohaber/Nefes) |
| Kapanan inşaat firması, Aralık 2025 | 1.175 (689 şirket/koop. + 486 şahıs) | TOBB (KOSGEB özeti) |
| İnşaatta konkordato dosyası, 2025 | 511 (toplam 6.361'in ~1/3'ü); tasdik oranı ~%2 | konkordatotakip.com derlemesi (Son Dakika) |
| İnşaatta konkordato başvurusu, 2025 Ocak–Ağustos | 268 (en yüksek sektör) | Odatv/T24, TBMM soru önergesi 33110 |
| İnşaat işyeri / sigortalı, 2024 | 229.550 / 1.991.728 → ~8,7 kişi/işyeri | SGK (ÇSGB) |
| İnşaat girişim ölüm oranı, 2022 | %10,6 | TÜİK Girişim Demografisi |
| İnşaat istihdamı, 2025 | 2.224.000 | TÜİK HİA |
| Backtest: zarar eden kohort | 87→15 ve 103→15 (%82,8–%85,4 azalma) | Bu repo, backtest |

## Hesap
Risk altındaki iş = yıllık kapanış/konkordato × 8,7 kişi. Korunan iş üst sınırı = risk altındaki iş × zarar azalması. Bu sınır, kapanışların tamamının sabit fiyat/maliyet zararından kaynaklandığını varsayar.

| Taban | Firma/yıl | Risk altındaki iş | Korunan iş, %100 kapsam | %10 kapsam | İnşaat istihdamına oranı |
|---|---|---|---|---|---|
| TOBB kapanış (1.652×2) | 3.304 | ~28.700 | **23.700–24.500** | 2.400–2.450 | %1,07–1,10 |
| Konkordato 2025 | 511 | ~4.400 | **3.700–3.800** | ~370–380 | %0,16–0,17 |
| **Alt sınır** | — | — | **0** | 0 | 0 |

## Neden alt sınır 0
- Zarar→iflas bağı kanıtlanmadı. Kapanışların hangi kısmının maliyet artışı zararından, hangisinin faiz, tahsilat, talep düşüşü ya da gönüllü tasfiyeden kaynaklandığını gösteren veri yok. Konkordato başvurularında yüksek faiz ve tahsilat sorunu öne çıkıyor; model bunları çözmüyor.
- Kapanan firmalar ortalamadan küçük olabilir (yarısı şahıs firması). Bu durumda 8,7 kişi fazla, yani üst sınır daha da düşük.
- Kapanış, işin yok olması demek değil. Proje ve işçi başka firmaya geçebilir; net iş kaybı verisi yok.
- Backtest 116–122 kohortluk bir simülasyon, gerçek firma iflas verisi değil.

## Hüküm (kullanıcı ölçütü: "iflasları durdurup istihdamı koruyorsa yeterli")
- **İflasları durdurur mu? Hayır, tamamen değil; kanıtlanmış olarak da değil.** Model iflas nedenlerinden yalnızca birini, sözleşme fiyatı ile maliyet arasındaki açığı, hedefliyor. Backtest'te bu nedenle zarar eden kohortları %83–85 azaltıyor. Faiz ve tahsilat kaynaklı iflaslara etkisi yok.
- **İstihdamı korur mu? Sınırlı ölçüde ve yalnızca üst sınır olarak.** Tam kapsamda en fazla yaklaşık 24 bin iş/yıl, yani inşaat istihdamının yaklaşık %1,1'i. %10 kapsamda yaklaşık 2,4 bin. Kanıtlanabilen alt sınır 0.
- **Ölçütü karşılıyor mu? Kanıtlı olarak hayır, potansiyel olarak kısmen.** Karşılandığını göstermek için gereken veri: kapanan ve konkordato ilan eden inşaat firmalarının neden kırılımı (maliyet zararı payı) ve çalışan sayısı (SGK işyeri kapanış kaydı).

## Güncelleme: dijital tahsilat sistemi eklendi
Ayrıntı: [TAHSILAT_SISTEMI.md](TAHSILAT_SISTEMI.md). İflasların ~%25'i tahsilat kaynaklı (Hazine 2018). Maliyet kuralı ile tahsilat sistemi birlikte uygulanınca korunan iş üst sınırı tam kapsamda **25.000–25.500 iş/yıl** (inşaat istihdamının %1,12–1,15'i), %10 kapsamda ~2.500; konkordato tabanında 3.900–4.000. **Alt sınır 0.**
- **Güncel hüküm:** Tahsilat sistemi faiz dışındaki ikinci büyük nedeni (alacak tahsilatı) kapsama alıyor. Ancak yurtdışında bu tür sistemlerin iflası azalttığı kanıtlanmadı. Ölçüt kanıtlı olarak yine karşılanmıyor, potansiyel olarak kısmen karşılanıyor. Faiz/finansman kaynaklı iflaslar hâlâ kapsam dışında.
