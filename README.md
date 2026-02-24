<div align="center">

# 🌍 GeoSite & GeoIP Files

**Актуальные базы GeoSite и GeoIP для X-Ray и Sing-Box**

</div>

---

<div align="center">
  
## 📋 Быстрое копирование всех ссылок

</div>


## 📡 Для X-Ray

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

---

## 📡 Для Sing-Box

<details>
<summary>

### 🔽 КОНФИГУРАЦИЯ SING-BOX ДЛЯ HAPP 🔽

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
        "address": "https://1.1.1.1/dns-query",
        "detour": "direct"
      },
      {
        "tag": "dns-direct-backup",
        "address": "https://8.8.8.8/dns-query",
        "detour": "direct"
      },
      {
        "tag": "dns-remote",
        "address": "https://1.1.1.1/dns-query",
        "detour": "proxy"
      },
      {
        "tag": "dns-remote-backup",
        "address": "https://8.8.8.8/dns-query",
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
    },
    {
      "type": "block",
      "tag": "block"
    }
  ],
  "route": {
    "rule_set": [
      {
        "tag": "block-rules",
        "type": "remote",
        "format": "binary",
        "url": "https://raw.githubusercontent.com/Sn1pp1/mygeofiles/main/files/block.srs",
        "download_detour": "proxy"
      },
      {
        "tag": "direct-rules",
        "type": "remote",
        "format": "binary",
        "url": "https://raw.githubusercontent.com/Sn1pp1/mygeofiles/main/files/direct.srs",
        "download_detour": "proxy"
      },
      {
        "tag": "games-rules",
        "type": "remote",
        "format": "binary",
        "url": "https://raw.githubusercontent.com/Sn1pp1/mygeofiles/main/files/games.srs",
        "download_detour": "proxy"
      }
    ],
    "rules": [
      {
        "protocol": "dns",
        "action": "hijack-dns"
      },
      {
        "rule_set": "block-rules",
        "outbound": "block"
      },
      {
        "domain_suffix": [".ru", ".su", ".рф", ".xn--p1ai"],
        "outbound": "direct"
      },
      {
        "rule_set": "games-rules",
        "outbound": "direct"
      },
      {
        "rule_set": "direct-rules",
        "outbound": "direct"
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


**📥 block.srs**
```text
https://raw.githubusercontent.com/Sn1pp1/mygeofiles/main/files/block.srs
```

**📥 direct.srs**
```text
https://raw.githubusercontent.com/Sn1pp1/mygeofiles/main/files/direct.srs
```

**📥 games.srs**
```text
https://raw.githubusercontent.com/Sn1pp1/mygeofiles/main/files/games.srs
```
---

## 📌 Важные примечания

> [!NOTE]
> - ✅ **Автоматическое обновление** — файлы обновляются автоматически при изменениях в исходных репозиториях
> - ⚡ **jsDelivr CDN** — обеспечивает быструю загрузку через CDN, но может иметь небольшую задержку при обновлении
> - 📥 **Прямые ссылки** — все ссылки готовы к использованию в конфигурационных файлах
> - 🎯 **Sing-Box .srs файлы** — это rule sets в бинарном формате для максимальной производительности

> [!TIP]
> Для X-Ray используйте **GitHub Releases** ссылки — они всегда указывают на последнюю стабильную версию.

> [!WARNING]
> При использовании jsDelivr CDN кэш может обновляться до 24 часов. Для критичных систем используйте GitHub Releases.
