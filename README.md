# Hava Durumu

[![hacs_badge](https://img.shields.io/badge/HACS-Custom-orange.svg)](https://github.com/custom-components/hacs)

Türkiye Meteoroloji Genel Müdürlüğü (MGM) verilerini kullanan Home Assistant entegrasyonu.

## Özellikler

- 🌡️ Anlık hava durumu bilgileri
- 📅 5 günlük tahmin (min/max sıcaklık)
- ⏰ Saatlik tahmin
- 💧 16 farklı sensör (sıcaklık, nem, rüzgar, basınç, yağış, tahminler, uyarılar, vb.)
- ⚠️ Meteorolojik uyarılar ve otomatik bildirimler
- ⚙️ Yapılandırılabilir güncelleme sıklığı (5-60 dakika)
- 🇹🇷 Türkçe ve İngilizce dil desteği
- 🔮 Bugün ve yarın hava durumu tahminleri

## Kurulum

### HACS ile (Önerilen)

1. HACS → Entegrasyonlar → Sağ üst menü → Özel Depolar
2. Depo URL'sini ekleyin: `https://github.com/ahamitd/hava-durumu`
3. Kategori: Integration
4. "Hava Durumu" entegrasyonunu arayın ve yükleyin
5. Home Assistant'ı yeniden başlatın

### Manuel Kurulum

1. `custom_components/hava_durumu` klasörünü Home Assistant'ın `config/custom_components/` dizinine kopyalayın
2. Home Assistant'ı yeniden başlatın

## Yapılandırma

1. **Ayarlar** → **Cihazlar ve Servisler** → **Entegrasyon Ekle**
2. "Hava Durumu" arayın
3. İl seçin
4. İlçe seçin
5. Kurulum tamamlandı!

## Kullanım

### Weather Kartı

```yaml
type: weather-forecast
entity: weather.ILCE_IL
show_forecast: true
```

### Sensörler

Entegrasyon aşağıdaki sensörleri oluşturur:

- `sensor.ILCE_IL_sicaklik` - Sıcaklık (°C)
- `sensor.ILCE_IL_nem` - Nem oranı (%)
- `sensor.ILCE_IL_ruzgar_hizi` - Rüzgar hızı (km/h)
- `sensor.ILCE_IL_ruzgar_yonu` - Rüzgar yönü (K, KB, D, GD, G, GB, B, KB)
- `sensor.ILCE_IL_basinc` - Hava basıncı (hPa)
- `sensor.ILCE_IL_gorus_mesafesi` - Görüş mesafesi (m)
- `sensor.ILCE_IL_precipitation_current` - Anlık yağış (mm)
- `sensor.ILCE_IL_yagis_1_saat` - Son 1 saat yağış (mm)
- `sensor.ILCE_IL_yagis_24_saat` - Son 24 saat yağış (mm)
- `sensor.ILCE_IL_bulutluluk` - Bulutluluk (okta)
- `sensor.ILCE_IL_hissedilen_sicaklik` - Hissedilen sıcaklık (°C)
- `sensor.ILCE_IL_hava_durumu` - Hava durumu açıklaması
- `sensor.ILCE_IL_uyari_sayisi` - Aktif uyarı sayısı
- `sensor.ILCE_IL_uyari_detaylari` - Uyarı detayları
- `sensor.ILCE_IL_forecast_today` - Bugün hava tahmini (Güneşli, Yağmurlu, Karlı vb.)
- `sensor.ILCE_IL_forecast_tomorrow` - Yarın hava tahmini

### Hava Durumu Uyarıları

Entegrasyon, MGM'den gelen meteorolojik uyarıları otomatik olarak takip eder ve bildirim gönderir.

#### Binary Sensor

`binary_sensor.ILCE_IL_hava_durumu_uyarisi` - Aktif uyarı olduğunda **ON** durumuna geçer.

**Attributes (Özellikler):**
- `alert_count`: Toplam aktif uyarı sayısı
- `last_alert`: En son uyarının başlığı
- `alerts`: Tüm uyarıların detaylı listesi

#### Uyarı Detaylarını Görmek

**1. Basit Yöntem:**
- Sensöre tıklayın → **Attributes** sekmesine bakın

**2. Lovelace Kartı ile:**

```yaml
type: markdown
content: |
  {% if is_state('binary_sensor.ILCE_IL_hava_durumu_uyarisi', 'on') %}
  ## 🚨 Aktif Hava Durumu Uyarıları
  
  **Toplam:** {{ state_attr('binary_sensor.ILCE_IL_hava_durumu_uyarisi', 'alert_count') }} uyarı
  
  ---
  
  {% for alert in state_attr('binary_sensor.ILCE_IL_hava_durumu_uyarisi', 'alerts') %}
  ### ⚠️ {{ alert.title }}
  - **Tür:** {{ alert.type }}
  - **Tarih:** {{ alert.date }}
  {% if alert.description %}
  - **Açıklama:** {{ alert.description }}
  {% endif %}
  
  ---
  {% endfor %}
  {% else %}
  ## ✅ Aktif Uyarı Yok
  {% endif %}
title: Hava Durumu Uyarıları
```

#### Otomatik Bildirimler

Entegrasyon, yeni uyarı geldiğinde **otomatik olarak** Home Assistant bildirimi oluşturur:
- 🔔 Kalıcı bildirim (manuel kapatılana kadar kalır)
- 📱 Bildirim başlığı: "🌩️ Hava Durumu Uyarısı - İlçe, İl"
- 📝 İlk 3 uyarının detayları gösterilir

**Bildirimleri görmek için:**
Ayarlar → Bildirimler (veya sağ üst köşedeki zil ikonu)

#### Mobil Bildirim Otomasyonu

```yaml
automation:
  - alias: "Hava Durumu Uyarısı - Mobil Bildirim"
    trigger:
      - platform: state
        entity_id: binary_sensor.ILCE_IL_hava_durumu_uyarisi
        to: "on"
    action:
      - service: notify.mobile_app_your_phone
        data:
          title: "⚠️ Hava Durumu Uyarısı"
          message: >
            {{ state_attr('binary_sensor.ILCE_IL_hava_durumu_uyarisi', 'last_alert') }}
          data:
            priority: high
            ttl: 0
```

## Ayarlar

### Güncelleme Sıklığı

Entegrasyon ayarlarından güncelleme sıklığını değiştirebilirsiniz:

1. **Ayarlar** → **Cihazlar ve Servisler** → **Hava Durumu**
2. **Yapılandır** butonuna tıklayın
3. Güncelleme sıklığını seçin (5, 10, 15, 30, 60 dakika)
4. Kaydet

**Not:** Varsayılan güncelleme sıklığı 30 dakikadır.

## Sık Sorulan Sorular (SSS)

### Bazı sensörler neden "bilinmeyen" veya "unavailable" gösteriyor?

MGM API'si tüm meteoroloji istasyonlarında aynı sensörleri sağlamıyor. Bazı konumlarda belirli sensörler (örneğin basınç, görüş mesafesi, bulutluluk) mevcut değil veya veri gelmiyor.

**Normal Davranış:**
- ✅ Sensör "bilinmeyen" gösteriyorsa: MGM o konum için bu veriyi sağlamıyor
- ✅ Sensör geçerli bir değer gösteriyorsa: Veri mevcut

**Önceki Sürümlerde:**
- ❌ Basınç: `-9999 hPa` (hatalı)
- ❌ Görüş mesafesi: `-9999 m` (hatalı)

**v1.5.1 ve Sonrası:**
- ✅ Geçersiz değerler filtreleniyor
- ✅ Sensör "bilinmeyen" gösteriyor (doğru)

### Hangi sensörler her zaman mevcut?

Aşağıdaki sensörler genellikle tüm konumlarda mevcuttur:
- Sıcaklık
- Nem
- Rüzgar hızı ve yönü
- Hava durumu açıklaması
- Tahmin sensörleri (bugün/yarın)

### Konumumu değiştirirsem ne olur?

Entegrasyonu kaldırıp yeniden ekleyerek farklı bir il/ilçe seçebilirsiniz. Her konum için farklı sensörler mevcut olabilir.

## Veri Kaynağı

Veriler T.C. Çevre, Şehircilik ve İklim Değişikliği Bakanlığı Meteoroloji Genel Müdürlüğü'nden alınmaktadır.

## Lisans

MIT License
