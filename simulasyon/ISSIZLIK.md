# İşsizlik Etkisi

Script: `issizlik.py`, çıktı: `data/issizlik.csv`. Net iş rakamları [ISTIHDAM.md](ISTIHDAM.md), [ISTIHDAM_SEKTOREL.md](ISTIHDAM_SEKTOREL.md) ve [ISTIHDAM_MODULER.md](ISTIHDAM_MODULER.md)'den alındı.

## Baz: TÜİK İşgücü İstatistikleri, Ağustos 2026 (mevsimsellikten arındırılmış, 30.09.2026)
| Gösterge | Değer |
|---|---|
| İşgücü | 35.247.000 |
| İşsiz | 2.740.000 |
| İşsizlik oranı | %7,8 |
| İstihdam | 32.507.000 |
| Atıl işgücü oranı (geniş tanım) | %31,0 |

Kaynak: [TÜİK bülteni 57987](https://veriportali.tuik.gov.tr/tr/press/57987), aktaran [G24](https://www.g24borsa.com/tuik-acikladi-issizlik-dustu-atil-isgucu-yukseldi/).

## Yeni iş, işsizlikte eşit düşüş demek değildir
- **Mekanik üst sınır (1:1):** Her yeni işi bir işsiz doldurur.
- **Akım tabanlı kaba tahmin (~%40):** SBB (2022) "Türkiye İşgücü Piyasasında Hareketlilik" çalışmasına göre işsizlerin bir yıl içinde iş bulma olasılığı yaklaşık %43, işgücü dışındakilerin hareket oranı %10,3. İşgücü dışındaki havuz (~32 milyon) işsiz havuzunun (~2,7 milyon) yaklaşık 12 katı. Bu yüzden yeni işlerin büyük kısmı işgücü dışından gelenlerle dolar; işsizlerden dolan pay kabaca %40'tır. Bu benim türetmem, yayımlanmış bir katsayı değil. Türkiye için doğrudan "yeni işin işsizlerden dolan payı" tahmini bulamadım.
- **Göçmenler ve kayıt dışı akış:** Ölçülemiyor. İşsizlikteki düşüşü daha da azaltır.

## Tablo: işsizlik oranındaki değişim (puan)
| Senaryo | Net iş (tüm sektör) | Tüm sektör, 1:1 | Tüm sektör, ~%40 | %10 kapsam, 1:1 | %10 kapsam, ~%40 |
|---|---|---|---|---|---|
| Normal (varsayımsız) | 0 – 127–255 bin | 0 / −0,36 – −0,72 | 0 / −0,16 – −0,32 | 0 / −0,04 – −0,07 | 0 / −0,02 – −0,03 |
| Modüler düşük | +94 bin | −0,27 | −0,12 | −0,03 | −0,01 |
| Modüler orta | +234 bin | −0,66 | −0,30 | −0,07 | −0,03 |
| Modüler yüksek | +374 bin | −1,06 | −0,47 | −0,11 | −0,05 |
| Modüler, talep artışı yok | −170 bin | +0,48 | +0,19 | +0,05 | +0,02 |

İşsiz sayısındaki değişim örneği: modüler orta senaryo, tüm sektörde 1:1 varsayımıyla −234 bin, ~%40 varsayımıyla −94 bin. Diğer satırların sayıları CSV'de.

## Geçiş işsizliği (şantiyeden fabrikaya)
- Modüler orta senaryoda şantiyeden çıkan **brüt iş yaklaşık 479 bindir**: fabrikaya kayan 353 bin ile verimlilikle yok olan 126 bin. Net değişim −183 bindir, ancak brüt hareket bunun yaklaşık 2,6 katıdır.
- Fabrika işleri farklı il, vardiya ve beceri ister. Şantiye işçisinin yaşı, eğitimi ve göçmen/kayıt dışı payı bu geçişi zorlaştırır. Bu tür beceri ve yer uyumsuzluğu, net iş pozitif olsa bile geçici işsizliği artırır. Süresi ve boyutu Türkiye verisiyle ölçülemiyor; pilot gerektirir.
- BETAM (2023) bulguları: Türkiye'de işçi devri OECD ortalamasının yaklaşık 2 katı. İşsizlikten yeni işe girenlerin ücret kaybı, işten işe geçenlerden daha büyük. Geçiş maliyeti gerçek.
- Öneri: Fabrikaları şantiye bölgelerine yakın kurmak, İŞKUR mesleki eğitimi ve geçiş döneminde KOBİ işçilik desteğini önce geçiş yapan işçilere vermek.

## Atıl işgücü
Atıl işgücü oranı %31. Yeni işlerin bir kısmı eksik istihdamdakileri ve potansiyel işgücünü (iş aramayan ama çalışmaya hazır olanları) emer. Bu, dar tanımlı işsizlikten çok geniş tanımlı göstergeyi düşürür. Ayrıştırma verisi yok.
