<div align="center">

# 🌍 GeoSite & GeoIP Files

**Актуальные базы GeoSite и GeoIP для X-Ray**

</div>

---
  
## 📋 Быстрое копирование всех ссылок

### GitHub Releases

**📥 geosite.dat**
```text
https://github.com/Sn1pp1/mygeofiles/releases/download/latest/geosite.dat
```

**📥 geoip.dat**
```text
https://github.com/Sn1pp1/mygeofiles/releases/download/latest/geoip.dat
```

---

### jsDelivr CDN

**📥 geosite.dat**
```text
https://cdn.jsdelivr.net/gh/Sn1pp1/mygeofiles@main/geosite.dat
```

**📥 geoip.dat**
```text
https://cdn.jsdelivr.net/gh/Sn1pp1/mygeofiles@main/geoip.dat
```

## 📡 КОНФИГУРАЦИЯ SING-BOX ДЛЯ HAPP

<details>
<summary>

### 🔽 Показать полный конфиг для копирования 🔽

</summary>


```json
{
  "log": {
    "level": "info",
    "timestamp": true
  },
  "dns": {
    "servers": [
      {
        "tag": "dns-direct",
        "address": "8.8.8.8",
        "detour": "direct"
      },
      {
        "tag": "dns-remote",
        "address": "8.8.8.8",
        "detour": "proxy"
      }
    ],
    "rules": [
      {
        "outbound": "direct",
        "server": "dns-direct"
      }
    ],
    "final": "dns-remote",
    "strategy": "ipv4_only",
    "disable_cache": false,
    "disable_expire": true,
    "independent_cache": true,
    "cache_capacity": 1000
  },
  "inbounds": [
    {
      "type": "tun",
      "tag": "tun-in",
      "interface_name": "happ-tun",
      "address": ["172.18.0.1/30"],
      "mtu": 1400,
      "auto_route": true,
      "strict_route": false,
      "stack": "gvisor",
      "sniff": true,
      "sniff_override_destination": true
    }
  ],
  "outbounds": [
    {
      "type": "socks",
      "tag": "proxy",
      "server": "127.0.0.1",
      "server_port": 10808
    },
    {
      "type": "direct",
      "tag": "direct"
    }
  ],
  "route": {
    "rules": [
      {
        "protocol": "dns",
        "action": "hijack-dns"
      },
      {
        "process_name": [
          "vpnagent.exe",
          "vpnui.exe",
          "Cisco Secure Client.exe",
          "csc_ui.exe",
          "csc_service.exe",
          "xray.exe",
          "sing-box.exe",
          "antifilter.exe",
          "xray",
          "sing-box",
          "antifilter"
        ],
        "outbound": "direct"
      },
      {
        "ip_cidr": [
          "127.0.0.0/8",
          "224.0.0.0/4",
          "255.255.255.255/32",
          "10.0.0.0/8",
          "172.16.0.0/12",
          "192.168.0.0/16",
          "10.95.0.8/32",
          "10.95.0.9/32"
        ],
        "outbound": "direct"
      }
    ],
    "final": "proxy",
    "auto_detect_interface": true
  }
}
```
</details>

---

## 📌 Важные примечания

> [!NOTE]
> - ✅ **Автоматическое обновление** — файлы обновляются автоматически при изменениях в исходных репозиториях
> - ⚡ **jsDelivr CDN** — обеспечивает быструю загрузку через CDN, но может иметь небольшую задержку при обновлении
> - 📥 **Прямые ссылки** — все ссылки готовы к использованию в конфигурационных файлах

> [!TIP]
> Для X-Ray используйте **GitHub Releases** ссылки — они всегда указывают на последнюю стабильную версию.

> [!WARNING]
> При использовании jsDelivr CDN кэш может обновляться до 24 часов. Для критичных систем используйте GitHub Releases.
