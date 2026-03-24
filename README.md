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

## 📡 КОНФИГУРАЦИЯ ДЛЯ MIHOMO

<details>
<summary>

### 🔽 Показать полный конфиг для копирования 🔽

</summary>


```yaml
mixed-port: 7890
allow-lan: true
lan-allowed-ips:
  - 127.0.0.0/8
  - 10.0.0.0/8
  - 172.16.0.0/12
  - 192.168.0.0/16
  - 10.95.0.8/32
  - 10.95.0.9/32
  - ::1/128
  - fc00::/7
tcp-concurrent: true
enable-process: true
find-process-mode: always
mode: rule
log-level: info
ipv6: false
keep-alive-interval: 30
unified-delay: true
profile:
  store-selected: true
  store-fake-ip: true

sniffer:
  enable: true
  force-dns-mapping: true
  parse-pure-ip: true
  skip-dst-address:
    - 0.0.0.0/8
    - 10.0.0.0/8
    - 100.64.0.0/10
    - 127.0.0.0/8
    - 169.254.0.0/16
    - 172.16.0.0/12
    - 192.0.0.0/24
    - 192.0.2.0/24
    - 192.88.99.0/24
    - 192.168.0.0/16
    - 198.51.100.0/24
    - 203.0.113.0/24
    - 224.0.0.0/3
    - 10.95.0.8/32
    - 10.95.0.9/32
    - ::/127
    - fc00::/7
    - fe80::/10
    - ff00::/8
  sniff:
    HTTP:
      ports:
        - 80
        - 8080-8880
      override-destination: true
    TLS:
      ports:
        - 443
        - 8443
    QUIC:
      ports:
        - 443

tun:
  enable: true
  stack: mixed
  auto-route: true
  auto-detect-interface: true
  dns-hijack:
    - any:53
    - tcp://any:53
  strict-route: false
  mtu: 1400
  route-exclude-address:
    - 0.0.0.0/8
    - 10.0.0.0/8
    - 100.64.0.0/10
    - 127.0.0.0/8
    - 169.254.0.0/16
    - 172.16.0.0/12
    - 192.0.0.0/24
    - 192.0.2.0/24
    - 192.88.99.0/24
    - 192.168.0.0/16
    - 198.51.100.0/24
    - 203.0.113.0/24
    - 224.0.0.0/3
    - 10.95.0.8/32
    - 10.95.0.9/32
    - ::/127
    - fc00::/7
    - fe80::/10
    - ff00::/8
  exclude-process:
    # === Cisco Secure Client (AnyConnect) ===
    - "vpnui.exe"
    - "vpnagent.exe"
    - "vpncli.exe"
    - "AnyConnect.exe"
    - "ac_helper.exe"
    - "ac_service.exe"
    - "posture.exe"
    - "ise_posture.exe"
    - "amp.exe"
    - "darts.exe"
    # Steam
    - "steam.exe"
    - "steamwebhelper.exe"
    - "steam_service.exe"
    # Epic Games
    - "EpicGamesLauncher.exe"
    - "EpicGamesClient.exe"
    # Battle.net
    - "Battle.net.exe"
    - "Battle.net Helper.exe"
    - "Agent.exe"
    # Riot Games
    - "RiotClientServices.exe"
    - "VALORANT.exe"
    - "LeagueOfLegends.exe"
    - "LeagueClient.exe"
    # EA / Origin
    - "EADesktop.exe"
    - "Origin.exe"
    # Ubisoft
    - "Uplay.exe"
    - "UbisoftConnect.exe"
    # GOG
    - "GalaxyClient.exe"
    # Популярные игры
    - "cs2.exe"
    - "csgo.exe"
    - "dota2.exe"
    - "Minecraft.exe"
    - "javaw.exe"
    - "WorldOfTanks.exe"
    - "WarThunder.exe"
    - "RocketLeague.exe"
    - "Fortnite.exe"
    - "FortniteClient.exe"
    - "ApexLegends.exe"
    - "r5apex.exe"
    - "Overwatch.exe"
    - "OverwatchLauncher.exe"
    - "Wow.exe"
    - "PUBG.exe"
    - "TslGame.exe"
    - "Rust.exe"
    - "GTAV.exe"
    - "GTA5.exe"
    - "RedDeadRedemption2.exe"
    - "PathOfExile.exe"
    - "FallGuys.exe"
    # Античиты
    - "EasyAntiCheat.exe"
    - "BattlEye.exe"
    - "beservice.exe"
    - "vgc.exe"
    - "vgtray.exe"

dns:
  enable: true
  prefer-h3: true
  use-hosts: true
  use-system-hosts: true
  listen: 127.0.0.1:6868
  ipv6: false
  enhanced-mode: fake-ip
  fake-ip-range: 198.18.0.1/16
  fake-ip-filter:
    - "*.lan"
    - "*.local"
    - "localhost"
    - "*.mvideo.ru"
    - "*.msftncsi.com"
    - "time.*.com"
    - "dns.msftncsi.com"
    - "www.msftconnecttest.com"
  
  default-nameserver:
    - https://1.1.1.1/dns-query#DIRECT
    - https://8.8.8.8/dns-query#DIRECT
    - tls://1.1.1.1:853#DIRECT
    - tls://8.8.8.8:853#DIRECT
  
  proxy-server-nameserver:
    - https://1.1.1.1/dns-query#DIRECT
    - https://8.8.8.8/dns-query#DIRECT
    - tls://1.1.1.1:853#DIRECT
    - tls://8.8.8.8:853#DIRECT
  
  direct-nameserver:
    - https://1.1.1.1/dns-query#DIRECT
    - https://77.88.8.8/dns-query#DIRECT
    - https://8.8.8.8/dns-query#DIRECT
    - tls://77.88.8.8:853#DIRECT
    - 77.88.8.8#DIRECT
  
  nameserver:
    - https://1.1.1.1/dns-query#🌍 VPN
    - https://8.8.8.8/dns-query#🌍 VPN
    - tls://1.1.1.1:853#🌍 VPN
    - tls://8.8.8.8:853#🌍 VPN

proxies:
  # LEAVE THIS LINE!

proxy-groups:
  - name: 🌍 VPN
    icon: https://cdn.jsdelivr.net/gh/Koolson/Qure@master/IconSet/Color/Hijacking.png  
    type: select
    proxies:
      - ⚡️ Fastest
      - 📶 First Available
      # LEAVE THIS LINE!
  - name: ▶️ YouTube
    icon: https://cdn.jsdelivr.net/gh/Koolson/Qure@master/IconSet/Color/YouTube.png  
    type: select
    proxies:
      - 🌍 VPN
      # LEAVE THIS LINE!
  - name: 💬 Discord
    icon: https://cdn.jsdelivr.net/gh/Koolson/Qure@master/IconSet/Color/Discord.png  
    type: select
    proxies:
      - 🌍 VPN
      # LEAVE THIS LINE!
  - name: ⚡️ Fastest
    icon: https://cdn.jsdelivr.net/gh/Koolson/Qure@master/IconSet/Color/Auto.png  
    type: url-test
    tolerance: 150
    url: https://cp.cloudflare.com/generate_204  
    interval: 300
    proxies:
      # LEAVE THIS LINE!
  - name: 📶 First Available
    icon: https://cdn.jsdelivr.net/gh/Koolson/Qure@master/IconSet/Color/Download.png  
    type: fallback
    url: https://cp.cloudflare.com/generate_204  
    interval: 300
    proxies:
      # LEAVE THIS LINE!

rule-providers:
  domain_list:
    type: http
    behavior: domain
    format: text
    url: https://github.com/Sn1pp1/mygeofiles/raw/main/files/domain.txt  
    path: ./rule-sets/domain_list.txt
    interval: 86400
    proxy: 🌍 VPN
  meta_domains:
    type: http
    behavior: domain
    format: mrs
    interval: 86400
    url: https://github.com/MetaCubeX/meta-rules-dat/raw/meta/geo/geosite/meta.mrs  
    path: ./rule-sets/meta.mrs
    proxy: 🌍 VPN
  telegram_ips:
    type: http
    behavior: ipcidr
    format: mrs
    interval: 86400
    url: https://github.com/MetaCubeX/meta-rules-dat/raw/meta/geo/geoip/telegram.mrs  
    path: ./rule-sets/telegram_ips.mrs
    proxy: 🌍 VPN
  telegram_domains:
    type: http
    behavior: domain
    format: mrs
    interval: 86400
    url: https://github.com/MetaCubeX/meta-rules-dat/raw/meta/geo/geosite/telegram.mrs  
    path: ./rule-sets/telegram_domains.mrs
    proxy: 🌍 VPN
  discord_domains:
    type: http
    behavior: domain
    format: mrs
    url: https://github.com/MetaCubeX/meta-rules-dat/raw/meta/geo/geosite/discord.mrs  
    path: ./rule-sets/discord_domains.mrs
    interval: 86400
    proxy: 🌍 VPN
  discord_voiceips:
    type: http
    behavior: ipcidr
    format: mrs
    url: https://github.com/legiz-ru/mihomo-rule-sets/raw/main/other/discord-voice-ip-list.mrs  
    path: ./rule-sets/discord_voiceips.mrs
    interval: 86400
    proxy: 🌍 VPN
  refilter_domains:
    type: http
    behavior: domain
    format: mrs
    url: https://github.com/legiz-ru/mihomo-rule-sets/raw/main/re-filter/domain-rule.mrs  
    path: ./rule-sets/refilter_domains.mrs
    interval: 86400
    proxy: 🌍 VPN
  refilter_ipsum:
    type: http
    behavior: ipcidr
    format: mrs
    url: https://github.com/legiz-ru/mihomo-rule-sets/raw/main/re-filter/ip-rule.mrs  
    path: ./rule-sets/refilter_ipsum.mrs
    interval: 86400
    proxy: 🌍 VPN
  youtube:
    type: http
    behavior: domain
    format: mrs
    url: https://github.com/MetaCubeX/meta-rules-dat/raw/meta/geo/geosite/youtube.mrs  
    path: ./rule-sets/youtube.mrs
    interval: 86400
    proxy: 🌍 VPN
  oisd_big:
    type: http
    behavior: domain
    format: mrs
    url: https://github.com/legiz-ru/mihomo-rule-sets/raw/main/oisd/big.mrs  
    path: ./rule-sets/oisd_big.mrs
    interval: 86400
    proxy: 🌍 VPN
  torrent-trackers:
    type: http
    behavior: domain
    format: mrs
    url: https://github.com/legiz-ru/mihomo-rule-sets/raw/main/other/torrent-trackers.mrs  
    path: ./rule-sets/torrent-trackers.mrs
    interval: 86400
    proxy: 🌍 VPN
  torrent-clients:
    type: http
    behavior: classical
    format: yaml
    url: https://github.com/legiz-ru/mihomo-rule-sets/raw/main/other/torrent-clients.yaml  
    path: ./rule-sets/torrent-clients.yaml
    interval: 86400
    proxy: 🌍 VPN
  ru-bundle:
    type: http
    behavior: domain
    format: mrs
    url: https://github.com/legiz-ru/mihomo-rule-sets/raw/main/ru-bundle/rule.mrs  
    path: ./rule-sets/ru-bundle.mrs
    interval: 86400
    proxy: 🌍 VPN

rules:
  - IP-CIDR,192.168.0.0/16,DIRECT,no-resolve
  - IP-CIDR,10.0.0.0/8,DIRECT,no-resolve
  - IP-CIDR,172.16.0.0/12,DIRECT,no-resolve
  - IP-CIDR,127.0.0.0/8,DIRECT,no-resolve
  - IP-CIDR,10.95.0.8/32,DIRECT,no-resolve
  - IP-CIDR,10.95.0.9/32,DIRECT,no-resolve
  - RULE-SET,oisd_big,REJECT
  - OR,((DOMAIN,ipwhois.app),(DOMAIN,ipwho.is),(DOMAIN,api.ip.sb),(DOMAIN,ipapi.co),(DOMAIN,ipinfo.io)),🌍 VPN
  - OR,((RULE-SET,torrent-clients),(RULE-SET,torrent-trackers)),DIRECT
  - RULE-SET,youtube,▶️ YouTube
  - OR,((RULE-SET,telegram_ips),(RULE-SET,telegram_domains)),🌍 VPN
  - OR,((RULE-SET,discord_domains),(RULE-SET,discord_voiceips),(PROCESS-NAME,Discord.exe)),💬 Discord
  - RULE-SET,domain_list,🌍 VPN
  - RULE-SET,meta_domains,🌍 VPN
  - RULE-SET,refilter_domains,🌍 VPN
  - RULE-SET,refilter_ipsum,🌍 VPN
  - RULE-SET,ru-bundle,🌍 VPN
  - MATCH,DIRECT
```
</details>

## 📌 Важные примечания

> [!NOTE]
> - ✅ **Автоматическое обновление** — файлы обновляются автоматически при изменениях в исходных репозиториях
> - ⚡ **jsDelivr CDN** — обеспечивает быструю загрузку через CDN, но может иметь небольшую задержку при обновлении
> - 📥 **Прямые ссылки** — все ссылки готовы к использованию в конфигурационных файлах

> [!TIP]
> Для X-Ray используйте **GitHub Releases** ссылки — они всегда указывают на последнюю стабильную версию.

> [!WARNING]
> При использовании jsDelivr CDN кэш может обновляться до 24 часов. Для критичных систем используйте GitHub Releases.
