{% if installed %}
## ✅ Kurulum Tamamlandı!

Entegrasyon başarıyla yüklendi. Şimdi yapılandırabilirsiniz:

1. **Ayarlar** → **Cihazlar ve Servisler** → **Entegrasyon Ekle**
2. "Hava Durumu" arayın
3. İl ve ilçe seçin

{% endif %}

{% if pending_update %}
## 🔄 Güncelleme Mevcut

Yeni bir sürüm mevcut. Güncellemek için HACS'den güncelleyin.

{% endif %}

## 📖 Hakkında

Türkiye Meteoroloji Genel Müdürlüğü (MGM) resmi verilerini kullanarak Home Assistant'a hava durumu bilgisi sağlar.

### Özellikler

- 🌡️ **Anlık Hava Durumu**: Sıcaklık, nem, rüzgar, basınç
- 📅 **5 Günlük Tahmin**: Detaylı günlük tahminler
- ⏰ **Saatlik Tahmin**: 12 saatlik tahminler
- 💧 **10 Sensör**: Nem, rüzgar hızı/yönü, basınç, görüş mesafesi, yağış (1h/24h), bulutluluk, hissedilen sıcaklık
- ⚠️ **Uyarı Sistemi**: MGM ve MeteoAlarm uyarıları + otomatik bildirimler
- 🇹🇷 **Türkçe/İngilizce**: Tam dil desteği

### Kullanım

Weather kartı ekleyin:

```yaml
type: weather-forecast
entity: weather.ILCE_IL
show_forecast: true
```

Sensörleri kullanın:

```yaml
type: entities
entities:
  - sensor.ILCE_IL_nem
  - sensor.ILCE_IL_ruzgar_hizi
  - sensor.ILCE_IL_basinc
```

### Destek

Sorun bildirmek veya öneride bulunmak için [GitHub Issues](https://github.com/KULLANICI_ADI/hava-durumu/issues) kullanın.
