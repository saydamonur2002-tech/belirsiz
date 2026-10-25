# Gelir vergisi istisnası ve sigorta dışı maliyet sübvansiyonu (2026)

**Kısa cevap:** İstisnayı yoksulluk sınırına çekmek, devletin **daha az** vergi toplaması demek. Geri dönüşler (KDV/ÖTV, kayıt dışılıktan çıkış) kaybın yalnızca %10–25'ini karşılıyor.
- **A1 (bekâr işçi yaşam maliyeti, 48.885 TL):** gelir vergisi kaybı yılda ~485 mrd TL; net kayıp ~374–431 mrd TL.
- **A2 (4 kişilik ailenin yoksulluk sınırı, 123.130 TL):** gelir vergisi kaybı ~1,24 trilyon TL; net kayıp ~1,03–1,12 trilyon TL.
- **Senaryo B (inşaatta gelir vergisi ve damga vergisini devletin üstlenmesi):** konut birim maliyeti %2,8–3,1 düşer; maliyeti yılda ~121 mrd TL. Yalnız platformdaki KOBİ'lerle sınırlı tutulursa ~12–24 mrd TL.

Kod: `vergi_subvansiyon.py`. Çıktılar: `data/vergi_oranlar.csv`, `data/vergi_mali_etki.csv`, `data/subvansiyon_B.csv`.

## 1. Kaynaklı parametreler
| Parametre | Değer | Kaynak / dönem |
|---|---|---|
| Ücret GV tarifesi | %15 (190 bin TL'ye kadar) / %20 (400 bin) / %27 (1,5 mn) / %35 (5,3 mn) / %40 | GİB 2026 tarifesi; EY 2026/1 sirküleri |
| Asgari ücret | Brüt 33.030 TL, net 28.075,50 TL. GV ve damga istisnası asgari ücret tutarı kadar | ÇSGB, PwC, EY (2026) |
| İşveren primi | SGK %21,75 − 2 puan indirim (imalatta 5 puan) + işsizlik %2 | PwC 2026; 7566 sayılı Kanun |
| Asgari ücret desteği | 1.270 TL/ay; yıllık maliyet 76,37 mrd TL (İşsizlik Sigortası Fonu'ndan) | SGK 2026; TBMM etki analizi (Ekonomi Gazetesi) |
| TÜRK-İŞ (Eylül 2026) | Açlık sınırı 37.800,92 TL; yoksulluk sınırı 123.130 TL; bekâr işçinin yaşam maliyeti 48.884,82 TL | TÜRK-İŞ, 30.09.2026 |
| 2026 bütçesi | GV 3,558 trilyon TL; KDV 3,993 trilyon; ÖTV 2,532 trilyon; GSYH 77,257 trilyon | SBB 2026 |
| Ücret dağılımı | 16,94 mn 4/a sigortalı, asgari ücret katı bantları | SGK 2025 yıllığı, tablo 1.18 |
| İnşaatta sigortalı | 2.126.760 kişi | SGK 2025 iş kazası istatistikleri |
| İnşaatta asgari ücret ve altı | %71,4 | TCMB 2021 |
| Uluslararası | OECD ortalamasında istisna/indirimler, ortalama ücretli bekârın vergi matrahının %15,9'u. Almanya'da temel muafiyet 12.348 € (2026); İngiltere'de kişisel muafiyet 12.570 £ (2026/27) | OECD Taxing Wages 2025; § 32a EStG; GOV.UK |

## 2. Senaryo A: net/brüt ve net/işveren maliyeti oranları
Aylık TL, yıllık kümülatif hesap. İşveren maliyeti = brüt × 1,2175 (asgari ücret desteği hariç).

| Asgari ücret katı | Brüt | Net (mevcut) | Net (A1) | Net (A2) | Net/brüt (mevcut → A1 → A2) | Net/işveren maliyeti (mevcut → A1 → A2) |
|---|---|---|---|---|---|---|
| 1,0 | 33.030 | 28.076 | 28.076 | 28.076 | 0,850 → 0,850 → 0,850 | 0,698 → 0,698 → 0,698 |
| 1,3 | 42.939 | 34.517 | 36.423 | 36.423 | 0,804 → 0,848 → 0,848 | 0,660 → 0,697 → 0,697 |
| 1,6 | 52.848 | 40.590 | 44.770 | 44.770 | 0,768 → 0,847 → 0,847 | 0,631 → 0,696 → 0,696 |
| 2,0 | 66.060 | 48.688 | 53.938 | 55.900 | 0,737 → 0,817 → 0,846 | 0,605 → 0,671 → 0,695 |
| 2,5 | 82.575 | 58.810 | 64.061 | 69.813 | 0,712 → 0,776 → 0,845 | 0,585 → 0,637 → 0,694 |

Asgari ücretli zaten vergi ödemiyor, bu yüzden düzenleme ona bir şey kazandırmıyor. Kazanç 1,3–2,5 kat ücret alanlara gidiyor. A2'de istisna her çalışana aynı tutarda uygulanıyor, dolayısıyla yüksek ücretliler de aynı TL kazancı elde ediyor.

## 3. Mali etki (mrd TL/yıl, 2026)
| Senaryo | Kapsam | GV kaybı | KDV/ÖTV geri dönüşü | Kayıtlılıktan prim | Net (düşük → yüksek geri dönüş) |
|---|---|---|---|---|---|
| A1 | Ekonomi geneli | 484,7 | 40,9–61,4 | 12,3–49,4 | −431 → −374 |
| A1 | İnşaat | 33,2 | 2,8–4,2 | 1,5–6,2 | −29 → −23 |
| A2 | Ekonomi geneli | 1.238,7 | 104,6–156,9 | 12,3–49,4 | −1.122 → −1.033 |
| A2 | İnşaat | 86,0 | 7,3–10,9 | 1,5–6,2 | −77 → −69 |

- **Kısa vade:** tam kayıp. Kaybın 2026 bütçesindeki GV tahminine oranı: A1 %13,6, A2 %34,8.
- **Dinamik:** geri dönüşler ancak %10–25 karşılıyor. Kendi kendini finanse etmiyor.
- **Kontrol:** modelin hesapladığı mevcut ücret GV'si 1,69 trilyon TL. Bütçedeki toplam GV 3,56 trilyon, ama içinde ücret dışı gelirler de var. Ücret stopajının gerçek payını kaynaklı olarak bulamadım (boşluk).

## 4. Senaryo B: sigorta dışı maliyetler
- **Tanım:** sigorta dışı kesintiler gelir vergisi ve damga vergisidir. İşsizlik primi bir sigorta primi olduğu için kapsam dışında tutuldu.
- **Asgari ücrette:** bu kalemler zaten sıfır. Mevcut destekler de prim tarafında: 1.270 TL asgari ücret desteği (76,37 mrd TL/yıl), 2 ve 5 puanlık prim indirimi, 4447 sayılı Kanun teşvikleri. 2026 için indirim ve 4447 teşviklerinin toplam maliyetini kaynaklı olarak bulamadım (boşluk).
- **İnşaat:** GV ve damga, işveren maliyetinin ağırlıklı ortalama %7,46'sı. İnşaatta net ücret üzerinden anlaşma yapıldığı varsayılırsa (VARSAYIM) bu tutarı devletin üstlenmesi doğrudan işveren maliyetini düşürür. İşçilik payı %38–42 olduğunda konut birim maliyeti %2,83–3,13 düşer.
- **Maliyet:** tüm inşaat için ~121,4 mrd TL/yıl. Yalnız platformdaki KOBİ'ler için, platform payı %10–20 varsayımıyla (VARSAYIM) ~12–24 mrd TL.

## 5. Varsayımlar (VARSAYIM)
1. SGK'nın 2025 bant dağılımı asgari ücret katı olarak 2026'ya taşındı. Bant orta noktaları kullanıldı; 7,5 kat üstü 10 kat kabul edildi.
2. İnşaatta çalışanların %71,4'ü 1 kat asgari ücrette; kalan kısım ekonominin 1,1 kat üstü dağılımına göre yayıldı.
3. Yeni istisna, kişi bazında "istisna tutarı kadar matrahın kümülatif vergisi" olarak uygulandı (mevcut mekanizmanın aynısı).
4. Marjinal tüketim eğilimi 0,6 / 0,8 / 0,9.
5. Efektif dolaylı vergi oranı %14,1 = (KDV + ÖTV) / (özel tüketim = GSYH'nin %60'ı varsayımı).
6. Kayıtlı istihdam artışı %0,5 / 1 / 2. Bu oranlar Betcherman, Daysal ve Pagés'in (2010) Türkiye'deki bölgesel prim teşviklerinde bulduğu %5–15 etkiden çok daha küçük tutuldu, çünkü buradaki maliyet değişimi daha küçük. Yeni kayıtlılar asgari ücretli kabul edildi.
7. Asgari ücret desteği ve indirim farkları ihmal edildi. Tüm sektörlere 2 puanlık indirim uygulandı.

## 6. Boşluklar
- TÜİK göreli yoksulluk bülteni okunamadı (JavaScript gerekiyor).
- DİSK-AR'ın yoksulluk sınırı rakamı kullanılmadı.
- Ücret stopajının gerçek tutarı bulunamadı.
- 4447 ve prim indirimlerinin 2026 maliyeti bulunamadı.
- İnşaatın ücret dağılımı 2021 verisine dayanıyor.

## 7. Kaynaklar
- https://cdn.gib.gov.tr/api/gibportal-file/file/getFileResources?objectKey=arsiv%2Fyardim-kaynaklar%2Fyararli-bilgiler%2Fgelir-vergisi-tarifeleri%2Fgelir-vergisi-tarifesi-2026.pdf
- https://www.ey.com/tr_tr/services/tax/sosyal-guvenlikte-gundem/sirkuler/2026/sirkuler-no-1
- https://www.ey.com/tr_tr/insights/tax/2026-asgari-ucret
- https://www.pwc.com.tr/tr/medya/kose-yazilari/celal-ozcan/2026-yili-asgari-ucreti-ve-sektorlere-gore-isveren-maliyeti.html
- https://www.sgk.gov.tr/Content/Post/c52f99f0-da6c-4029-9b9a-a0d6f96a6a42/Guncel-Sigorta-Primi-Tesvik-Destek-ve-Indirimleri-2026-08-04-10-29-55
- https://www.ekonomigazetesi.com/ekonomi/asgari-ucret-desteginin-yillik-maliyeti-763-milyar-tl-69598
- https://www.cnbce.com/veriler/turk-is-acikladi-aclik-siniri-37-bin-801-tlye-yukseldi-h38367
- https://www.sbb.gov.tr/wp-content/uploads/2025/12/3a-Genel-Butceli-Kamu-Idarelerinin-2026-Yili-Gelirleri-ile-2027-2028-Donemi-Gelir-Tahminleri.pdf
- https://asgariucret.co/asgari-ucretle-calisan-orani (SGK yıllığı, tablo 1.18)
- https://ilketv.com.tr/sgk-2025-yili-is-kazasi-ve-meslek-hastaliklari-istatistikleri/
- https://www.oecd.org/en/publications/2025/04/taxing-wages-2025_20d1a01d.html
- https://www.gesetze-im-internet.de/estg/__32a.html
- https://www.gov.uk/income-tax-rates
- https://ideas.repec.org/a/eee/labeco/v17y2010i4p710-722.html
