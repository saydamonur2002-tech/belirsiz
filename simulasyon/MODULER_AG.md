# Modüler uzman firma ağı ve aracıların tasfiyesi

**Karar (pt18u):** Sistem tek bir üretim firması olarak kurulmaz. Modüler ve uzmanlaşmış firmalardan oluşan bir ağ olarak kurulur. Platform, üretici ve uzman firmalarla doğrudan çalışır.
- **Mevcut zincir:** üretici → ana bayi → alt bayi/toptancı → müteahhit → taşeron → alt taşeron.
- **Yeni zincir:** üretici veya uzman firma → platform kataloğu → müteahhit/alıcı.

Kod: `moduler_ag.py`. Çıktı: `data/moduler_ag_katmanlar.csv`.

## 1. Yapı
- **İş paketleri:** kaba yapı, prefabrik bileşen, doğrama, tesisat, elektrik, yalıtım, ince iş.
- **Her pakette birden çok onaylı uzman firma** çalışır. Rekabetçi kota uygulanır: tek firmanın paket içindeki payı sınırlıdır (öneri: bölge bazında ≤%30–40, VARSAYIM).
- **Standart arayüzler ve katalog:** ölçü/modül koordinasyonu, bağlantı detayları ve performans beyanı tanımlanır. Böylece aynı katalog kalemi için fiyatlar karşılaştırılabilir olur.
- **Doğrudan sözleşme ve ödeme:** platform üzerinden sözleşme yapılır, hakedişe bağlı ödeme emanet hesapla doğrudan uzman firmaya gider. Ara bayi vadesi ve finansman maliyeti ortadan kalkar.
- **Koordinasyon:** paketler arasındaki arayüz sorumluluğunu platformdaki paket koordinatörü üstlenir; sorumluluk matrisi sözleşmeye yazılır.

## 2. Kaynaklı aracı payı bulguları
| Konu | Bulgu | Kaynak |
|---|---|---|
| Bayi brüt marjı, kaba malzeme | Demir, çimento, hazır beton, tuğla için %1–4. Kum/çakıl/tuğla/çimento/beton %1–2, demir %1–5, seramik %2,5–5 (2005–2008) | ALTSO karlılık komitesi kararları (2004, 2010) |
| Bayi marjı, ince iş malzemesi | Seramik, vitrifiye, sıhhi tesisat için %2–15 | ALTSO (2004) |
| Toplu projelerde bayi | Büyük alımlarda bayi devre dışı bırakılıyor ya da %1–2 kâra razı ediliyor; vadeler 120–270 gün | Emlakkulisi (2011) |
| Demir/çimento bayisi | Brüt marj %8–15 (sektör blogu, düşük güvenilirlik) | adaptedijital.com |
| Müteahhit kârı ve genel gider | Kamu birim fiyatlarında %25 = %10 kâr + %15 genel gider | ÇŞB SSS; YFK yazısı (1955 kararı) |
| Taşeron kârı | Mikro ölçekli alt yükleniciler %16–20 kâr hedefliyor, gerçekleşen kâr çoğunlukla %1–10 | İTÜ tezi, Okay (2014) |
| Modüler yapım | Doğru koşullarda %20'ye varan maliyet tasarrufu, ancak "bugün kural değil istisna"; süre %20–50 kısalıyor | McKinsey (2019) |
| İngiltere MMC | Konut üreticilerinin %44'ü, konut kooperatiflerinin %27'si maliyet tasarrufu gördüğünü söylüyor. NAO: modern yöntemlerin ortalama maliyeti geleneksel yöntemden yüksek. 12 vakadan 2'si daha pahalı çıkmış | NHBC/Buildoffsite (2016); NAO; MDPI (2022) |
| İsveç / Japonya | İsveç'te çok katlı konutların ~%45'i prefabrik eleman kullanıyor; BoKlok'ta üretimin %85'i fabrikada. Japonya'da yılda 70 binden fazla prefabrik yapı; müstakil konut stokunun %15'i modüler. Sekisui House'a özgü bir maliyet rakamı **bulunamadı** | U of Toronto School of Cities (2024) |

Sonuç: Türkiye'de bayi marjı ince ama gerçek. Asıl potansiyel taşeron zincirinde, ancak gerçekleşen taşeron kârı düşük. Modüler tasarruf uluslararası kanıtta karışık; McKinsey'in ifadesiyle "0 ile %20 arası".

## 3. Katmanlı konut birim maliyeti düşüşü
Kümülatif değerler çarpımsal olarak hesaplandı.

| Katman | Düşük | Orta | Yüksek | Kümülatif (düşük / orta / yüksek) |
|---|---|---|---|---|
| 1. Ölçek + yerlileştirme + G1 %10 KOBİ marjı | −1,8% | −7,1% | −13,9% | −1,8 / −7,1 / −13,9 |
| 2. Bayi/toptancı marjının tasfiyesi | −0,3% | −1,4% | −4,2% | −2,1 / −8,4 / −17,5 |
| 3. Taşeron zincirinin kısalması (koordinasyon maliyeti düşülmüş) | +0,2% | −2,0% | −7,5% | −1,9 / −10,2 / −23,7 |
| 4. Modüler uzman ağ verimliliği | 0% | −2,0% | −5,0% | −1,9 / −12,0 / −27,5 |
| 5. Hedefli GV + damga desteği (platform KOBİ) | −2,8% | −3,0% | −3,1% | −4,7 / −14,6 / −29,8 |
| 6. Karma oynaklık araçları (alıcı fiyatı) | −0,2% | −0,2% | −0,2% | **−4,8 / −14,8 / −29,9** |
| 7. 6 aylık maliyet bazlı güncelleme + %30 tavan | 0 | 0 | 0 | Birim maliyeti düşürmez; marjı korur, zarar eden kohortu önler |

**Okuma:** orta senaryoda toplam düşüş yaklaşık %15; yeni ağ yapısının (katman 2–4) bu düşüşe katkısı yaklaşık 5,4 puan. Yüksek senaryodaki ~%30 iyimser bir üst sınırdır ve kaynaklardaki kanıt bunu desteklemez.

## 4. Varsayımlar (VARSAYIM)
- **Bayi kanalı:** girdinin %60 / 75 / 90'ı bayi üzerinden geçiyor. Kaynaklı bant içinden marj %1,5 / 4 / 8 seçildi. Platformun bu marjın yakalayabildiği kısım %50 / 70 / 90 (lojistik ve vade maliyeti platformda kalıyor).
- **Taşeron:** işin %40 / 60 / 80'i taşeronla yapılıyor. Kaldırılan ara katmanın payı %2 / 5 / 10; bu, gerçekleşen kâr bandı (%1–10) ve ÇŞB'deki %10 kâr oranıyla tutarlı. Koordinasyon maliyeti +%1 / 1 / 0,5.
- **Modüler:** maliyetin %30 / 40 / 50'si modüler üretime uygun; bu kısımda tasarruf %0 / 5 / 10. Taşeron marjı 3. katmanda sayıldığı için burada yeniden sayılmadı (McKinsey de tasarrufun bir kısmını taşeron marjına bağlıyor).
- **Etkileşim:** katmanlar arasındaki etkileşim, örneğin modülerleşmeyle şantiye işçiliğinin azalıp vergi desteği tabanının küçülmesi, modellenmedi.

## 5. Riskler
- **Koordinasyon maliyeti:** çok sayıda paket ve arayüz var; 3. katmanda düşük senaryoda maliyet artışı bu yüzden çıkıyor.
- **Sorumluluk dağınıklığı:** kusurun hangi pakete ait olduğu belirsizleşebilir. Gerekenler: sorumluluk matrisi, paket bazlı mesleki sorumluluk sigortası, platform koordinatörü.
- **Mevcut bayi ağının direnci:** TOBB'un sektör raporu bayi kanalının ağırlığını koruyacağını öngörüyor. Üreticiler riski paylaşmak için bayiyi kullanmaya devam ediyor. Bayilerin lojistik ve depo hizmet sağlayıcısına dönüşmesi için bir geçiş yolu tanımlanmalı.

## 6. Eksikler
- Türkiye için güncel ve resmî bir bayi marjı istatistiği bulunamadı; ALTSO verisi 2004–2010'a ait.
- Taşeron zincirinin toplam maliyet içindeki payını ölçen kaynak bulunamadı.
- Sekisui House'a özgü maliyet verisi bulunamadı.
- İsveç için tasarruf yüzdesi bulunamadı; yalnızca yaygınlık verisi var.

## 7. Kaynaklar
- https://www.altso.org.tr/bilgi-hizmetleri/sektorlere-gore-karlilik-oranlari/
- https://emlakkulisi.com/toplu-konut-projelerinde-bayiler-devreden-cikariliyor/60964
- https://adaptedijital.com/yapi-market/insaat-demir-cimento-kar-marji/
- http://www.tobb.org.tr/Documents/yayinlar/T%C3%BCrkiye%20%C4%B0n%C5%9Faat%20Malzemeleri%20Sekt%C3%B6r%20G%C3%B6r%C3%BCn%C3%BCm%20Raporu.pdf
- https://csb.gov.tr/sss-detay/52
- https://webdosya.csb.gov.tr/db/yfk/editordosya/2011135.pdf
- https://polen.itu.edu.tr/items/42eefb83-cf4d-463b-b318-70834abc2473
- https://www.mckinsey.com/capabilities/operations/our-insights/modular-construction-from-projects-to-products
- https://www.buildoffsite.com/content/uploads/2016/07/NF70-MMC-WEB.pdf
- https://www.nao.org.uk/reports/using-modern-methods-of-construction-to-build-homes-more-quickly-and-efficiently/
- https://www.mdpi.com/2412-3811/7/12/164
- https://schoolofcities.utoronto.ca/wp-content/uploads/2024/11/Scaling-up-Modular-Construction-EN_August-2024_1.pdf
