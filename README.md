# Hava Durumu

[![hacs_badge](https://img.shields.io/badge/HACS-Custom-orange.svg)](https://github.com/custom-components/hacs)

Türkiye Meteoroloji Genel Müdürlüğü (MGM) verilerini kullanan Home Assistant entegrasyonu.

## Özellikler

- 🌡️ Anlık hava durumu bilgileri
- 📅 5 günlük tahmin
- ⏰ Saatlik tahmin
- 💧 10 farklı sensör (nem, rüzgar, basınç, yağış, vb.)
- ⚠️ Meteorolojik uyarılar ve bildirimler
- 🇹🇷 Türkçe ve İngilizce dil desteği

## Kurulum

### HACS ile (Önerilen)

1. HACS → Entegrasyonlar → Sağ üst menü → Özel Depolar
2. Depo URL'sini ekleyin: `https://github.com/KULLANICI_ADI/hava-durumu`
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

- `sensor.ILCE_IL_nem` - Nem oranı (%)
- `sensor.ILCE_IL_ruzgar_hizi` - Rüzgar hızı (km/h)
- `sensor.ILCE_IL_ruzgar_yonu` - Rüzgar yönü (°)
- `sensor.ILCE_IL_basinc` - Hava basıncı (hPa)
- `sensor.ILCE_IL_gorus_mesafesi` - Görüş mesafesi (m)
- `sensor.ILCE_IL_yagis_1_saat` - Son 1 saat yağış (mm)
- `sensor.ILCE_IL_yagis_24_saat` - Son 24 saat yağış (mm)
- `sensor.ILCE_IL_bulutluluk` - Bulutluluk (okta)
- `sensor.ILCE_IL_hissedilen_sicaklik` - Hissedilen sıcaklık (°C)
- `sensor.ILCE_IL_hava_durumu` - Hava durumu açıklaması

### Uyarı Otomasyonu

```yaml
alias: Hava Durumu Uyarısı
trigger:
  - platform: state
    entity_id: binary_sensor.ILCE_IL_hava_durumu_uyarisi
    to: "on"
action:
  - service: notify.mobile_app
    data:
      title: "⚠️ Hava Durumu Uyarısı"
      message: "{{ state_attr('binary_sensor.ILCE_IL_hava_durumu_uyarisi', 'last_alert') }}"
```

## Veri Kaynağı

Veriler T.C. Çevre, Şehircilik ve İklim Değişikliği Bakanlığı Meteoroloji Genel Müdürlüğü'nden alınmaktadır.

## Lisans

MIT License
