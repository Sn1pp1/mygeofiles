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
bind-address: "*"
lan-allowed-ips: # Разрешенные ip для подключения к lan
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
ipv6: false # true - если используйте ipv6
keep-alive-interval: 30
unified-delay: true

profile:
  store-selected: true
  store-fake-ip: true

sniffer:
  enable: true
  force-dns-mapping: true
  parse-pure-ip: true
  override-destination: true
  sniff:
    HTTP:
      ports:
        - 80
        - 8080-8880
    TLS:
      ports:
        - 443
        - 8443

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

tun:
  enable: true
  stack: gvisor
  auto-route: true
  auto-detect-interface: true
  dns-hijack:
    - any:53
    - tcp://any:53
  strict-route: true
  route-exclude-address:
    # Не пускаем адреса (служебные, приватные) в TUN
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

dns:
  enable: true
  prefer-h3: false
  use-hosts: true
  use-system-hosts: true
  ipv6: false #true - если хотите резолвить в ipv6
  enhanced-mode: fake-ip
  fake-ip-range: 198.18.0.1/16
  fake-ip-filter:
    - rule-set:geosite-private
    - "*.lan"
    - "*.msftncsi.com"
  # ----
  # Опционально выбираем DNS сервера - меняйте на ваш вкус.
  default-nameserver:
    # DNS для доменов DNS серверов
    - https://1.1.1.1/dns-query#DIRECT      # DoH Cloudflare (основной)
    - https://8.8.8.8/dns-query#DIRECT      # DoH Google (основной)
    - tls://1.1.1.1:853#DIRECT              # DoT Cloudflare (fallback)
    - tls://8.8.8.8:853#DIRECT              # DoT Google (fallback)
  proxy-server-nameserver:
    # DNS для доменов прокси из раздела proxies
    - https://1.1.1.1/dns-query#DIRECT
    - https://8.8.8.8/dns-query#DIRECT
  direct-nameserver:
    # DNS для сайтов идущих через DIRECT
    - https://1.1.1.1/dns-query#DIRECT      # DoH Cloudflare (основной)
    - https://77.88.8.8/dns-query#DIRECT    # DoH Яндекс (резерв)
    - https://8.8.8.8/dns-query#DIRECT      # DoH Google (резерв)
    - tls://77.88.8.8:853#DIRECT            # DoT Яндекс (fallback)
    - 77.88.8.8#DIRECT                      # Plain UDP (последний резерв)
  nameserver:
    # Сервер по умолчанию, DNS запросы будут идти через то, что выбрано в "Остальные сайты"
    - https://1.1.1.1/dns-query#🌍 Остальные сайты   # DoH CF (приоритет 1)
    - https://8.8.8.8/dns-query#🌍 Остальные сайты   # DoH Google (приоритет 2)
    - tls://1.1.1.1:853#🌍 Остальные сайты           # DoT CF (fallback 1)
    - tls://8.8.8.8:853#🌍 Остальные сайты           # DoT Google (fallback 2)
  nameserver-policy:
    # Блокировка рекламы (опционально)
    rule-set:oisd_big:
      - rcode://refused # Код отклонённого DNS
    # DNS для сайтов с файлами правил
    raw.githubusercontent.com,cdn.jsdelivr.net,github.com:
      - https://1.1.1.1/dns-query#🚫 Недоступные сайты
      - https://8.8.8.8/dns-query#🚫 Недоступные сайты
      - tls://1.1.1.1:853#🚫 Недоступные сайты
    # DNS для заблоченных ресурсов, DNS запросы будут идти через то, что выбрано в "Недоступные сайты"
    rule-set:ru-inside,refilter_domains,ru-inline-banned,category-porn,ai,google-deepmind,speedtest-net:
      - https://1.1.1.1/dns-query#🚫 Недоступные сайты
      - https://8.8.8.8/dns-query#🚫 Недоступные сайты
      - tls://1.1.1.1:853#🚫 Недоступные сайты
    # DNS для Discord, DNS запросы будут идти через то, что выбрано в "Discord"
    rule-set:discord_domains:
      - https://1.1.1.1/dns-query#💬 Discord
      - https://8.8.8.8/dns-query#💬 Discord
      - tls://1.1.1.1:853#💬 Discord
    # DNS для доменов Youtube, DNS запросы будут идти через то, что выбрано в "Youtube"
    rule-set:youtube:
      - https://1.1.1.1/dns-query#▶️ YouTube
      - https://8.8.8.8/dns-query#▶️ YouTube
      - tls://1.1.1.1:853#▶️ YouTube
    # DNS для доменов Telegram, DNS запросы будут идти через то, что выбрано в "Telegram"
    rule-set:telegram-domains,additional-telegram-domains:
      - https://1.1.1.1/dns-query#➤ Telegram
      - https://8.8.8.8/dns-query#➤ Telegram
      - tls://1.1.1.1:853#➤ Telegram
    # DNS для RU сайтов, DNS запросы будут через DNS указанные в direct-nameserver, если конечные ресурсы попадают в DIRECT.
    # Если вы добавите в селектор "⚪🔵🔴 RU сайты" какой-то прокси, то DNS запросы будут идти через указанные тут DNS сервера через этот прокси.
    rule-set:ru-inline,geosite-ru:
      - https://77.88.8.8/dns-query#⚪🔵🔴 RU сайты
      - https://1.1.1.1/dns-query#⚪🔵🔴 RU сайты
      - https://8.8.8.8/dns-query#⚪🔵🔴 RU сайты
      - tls://77.88.8.8:853#⚪🔵🔴 RU сайты
      - 77.88.8.8#⚪🔵🔴 RU сайты

proxies:
  - name: "🇷🇺 Без VPN"
    type: direct
    udp: true
  - name: DNS-OUT
    type: dns

proxy-groups:
  - name: 🚫 Недоступные сайты
    icon: https://cdn.jsdelivr.net/gh/remnawave/templates@main/icons/Blocked.png
    type: select
    proxies:
      - 🎲 Любой доступный сервер
      - 🇷🇺 Без VPN # Опционально

  - name: ▶️ YouTube
    icon: https://cdn.jsdelivr.net/gh/Koolson/Qure@master/IconSet/Color/YouTube.png
    type: select
    proxies:
      - 🚫 Недоступные сайты

  - name: 💬 Discord
    icon: https://cdn.jsdelivr.net/gh/remnawave/templates@main/icons/Discord.png
    type: select
    proxies:
      - 🚫 Недоступные сайты

  - name: ➤ Telegram
    icon: https://cdn.jsdelivr.net/gh/Koolson/Qure@master/IconSet/Color/Telegram.png
    type: select
    proxies:
      - 🚫 Недоступные сайты
      - 🇷🇺 Без VPN

  - name: ⚪🔵🔴 RU сайты
    icon: https://cdn.jsdelivr.net/gh/Koolson/Qure@master/IconSet/Color/Russia.png
    type: select
    remnawave: # Кастомное поле используемое только в Remnawave
      include-proxies: false # Опционально, если поставить true, прокси будут включены в эту группу
    proxies:
      - 🇷🇺 Без VPN

  - name: 🌍 Остальные сайты
    icon: https://cdn.jsdelivr.net/gh/Koolson/Qure@master/IconSet/Color/Global.png
    type: select
    proxies:
      - 🇷🇺 Без VPN
      - 🚫 Недоступные сайты

  - name: PROXY
    remnawave: # Кастомное поле используемое только в Remnawave
      include-proxies: true
    type: select
    hidden: true
    proxies:
      - 🚫 Недоступные сайты

  - name: 🎲 Любой доступный сервер
    type: fallback
    remnawave: # Кастомное поле используемое только в Remnawave
      include-proxies: true
      shuffle-proxies-order: true
    url: "https://www.gstatic.com/generate_204"
    interval: 300
    hidden: true
    lazy: true

rule-providers:
  ru-inline-banned:
    type: inline
    payload:
      - DOMAIN-SUFFIX,habr.com
      - DOMAIN-SUFFIX,seasonvar.ru
      - DOMAIN-SUFFIX,lib.social
      - DOMAIN-SUFFIX,kemono.su
      - DOMAIN-SUFFIX,jut.su
      - DOMAIN-SUFFIX,kara.su
      - DOMAIN-SUFFIX,theins.ru
      - DOMAIN-SUFFIX,tvrain.ru
      - DOMAIN-SUFFIX,echo.msk.ru
      - DOMAIN-SUFFIX,the-village.ru
      - DOMAIN-SUFFIX,snob.ru
      - DOMAIN-SUFFIX,novayagazeta.ru
      - DOMAIN-SUFFIX,moscowtimes.ru
      - DOMAIN-SUFFIX,natribu.org
      - DOMAIN-SUFFIX,kpapp.link
      - DOMAIN-SUFFIX,api.srvkp.com
      - DOMAIN-SUFFIX,digital-cdn.net
      - DOMAIN-SUFFIX,api.ios-kp.store
      - DOMAIN-SUFFIX,m.pushbr.com
      - DOMAIN-SUFFIX,karing.app
      - DOMAIN-SUFFIX,telepost.me
      - DOMAIN-SUFFIX,happ-proxy.com
      - DOMAIN-SUFFIX,happ.su
      - DOMAIN-SUFFIX,routing.happ.su
      - DOMAIN-SUFFIX,usher.ttvnw.net
      - DOMAIN-SUFFIX,gql.twitch.tv
      - DOMAIN-SUFFIX,ads.twitch.tv
      - DOMAIN-SUFFIX,playlist.ttvnw.net
      - DOMAIN-SUFFIX,static-cdn.jtvnw.net
      - DOMAIN-SUFFIX,boberlogs.top
      - DOMAIN-SUFFIX,uwu-logs.xyz
      - DOMAIN-SUFFIX,cdn-wow.mmoui.com
      - DOMAIN-SUFFIX,wowinterface.com
      - DOMAIN-SUFFIX,tampermonkey.net
      - DOMAIN-SUFFIX,userscript.zone
      - DOMAIN-SUFFIX,openuserjs.org
      - DOMAIN-SUFFIX,curseforge.com
      - DOMAIN-SUFFIX,forgecdn.net
      - DOMAIN-SUFFIX,geekuninstaller.com
      - DOMAIN-SUFFIX,iplist.opencck.org
      - DOMAIN-SUFFIX,browserleaks.com
      - DOMAIN-SUFFIX,dnsleaktest.com
      - DOMAIN-SUFFIX,dnsperf.com
      - DOMAIN-SUFFIX,tracklock.gg
      - DOMAIN-SUFFIX,cron-job.org
      - DOMAIN-SUFFIX,render.com
      - DOMAIN-SUFFIX,log.rw
      - DOMAIN-SUFFIX,utils.docs.rw
      - DOMAIN-SUFFIX,mobatek.net
      - DOMAIN-SUFFIX,norton.com
      - DOMAIN-SUFFIX,nortonlifelock.com
      - DOMAIN-SUFFIX,symantec.com
      - DOMAIN-SUFFIX,avast.com
      - DOMAIN-SUFFIX,avg.com
      - DOMAIN-SUFFIX,avira.com
      - DOMAIN-SUFFIX,eset.com
      - DOMAIN-SUFFIX,bitdefender.com
      - DOMAIN-SUFFIX,mcafee.com
      - DOMAIN-SUFFIX,trellix.com
      - DOMAIN-SUFFIX,sophos.com
      - DOMAIN-SUFFIX,hitmanpro.com
      - DOMAIN-SUFFIX,gdata.de
      - DOMAIN-SUFFIX,vipre.com
      - DOMAIN-SUFFIX,av-test.org
      - DOMAIN-SUFFIX,brave.com
      - DOMAIN-SUFFIX,bravesoftware.com
      - DOMAIN-SUFFIX,basicattentiontoken.org
      - DOMAIN-KEYWORD,yummyanime
      - DOMAIN-KEYWORD,yummy-anime
      - DOMAIN-KEYWORD,animeportal
      - DOMAIN-KEYWORD,anime-portal
      - DOMAIN-KEYWORD,animedub
      - DOMAIN-KEYWORD,anidub
      - DOMAIN-KEYWORD,animelib
      - DOMAIN-KEYWORD,ikianime
      - DOMAIN-KEYWORD,anilibria
    behavior: classical
  ru-inline:
    type: inline
    payload:
      - DOMAIN-SUFFIX,2ip.ru
      - DOMAIN-SUFFIX,yastatic.net
      - DOMAIN-SUFFIX,yandex.net
      - DOMAIN-SUFFIX,yandex.kz
      - DOMAIN-SUFFIX,yandex.com
      - DOMAIN-SUFFIX,yadi.sk
      - DOMAIN-SUFFIX,mycdn.me
      - DOMAIN-SUFFIX,jivosite.com
      - DOMAIN-SUFFIX,vk.com
      - DOMAIN-SUFFIX,avira.com
      - DOMAIN-SUFFIX,.ru
      - DOMAIN-SUFFIX,.su
      - DOMAIN-SUFFIX,.by
      - DOMAIN-SUFFIX,.ru.com
      - DOMAIN-SUFFIX,.ru.net
      - DOMAIN-SUFFIX,kudago.com
      - DOMAIN-SUFFIX,kinescope.io
      - DOMAIN-SUFFIX,redheadsound.studio
      - DOMAIN-SUFFIX,plplayer.online
      - DOMAIN-SUFFIX,lomont.site
      - DOMAIN-SUFFIX,remanga.org
      - DOMAIN-SUFFIX,shopstory.live
      - DOMAIN-KEYWORD,avito
      - DOMAIN-KEYWORD,miradres
      - DOMAIN-KEYWORD,premier
      - DOMAIN-KEYWORD,shutterstock
      - DOMAIN-KEYWORD,2gis
      - DOMAIN-KEYWORD,diginetica
      - DOMAIN-KEYWORD,kinescopecdn
      - DOMAIN-KEYWORD,researchgate
      - DOMAIN-KEYWORD,springer
      - DOMAIN-KEYWORD,nextcloud
      - DOMAIN-KEYWORD,kaspersky
      - DOMAIN-KEYWORD,stepik
      - DOMAIN-KEYWORD,likee
      - DOMAIN-KEYWORD,snapchat
      - DOMAIN-KEYWORD,yappy
      - DOMAIN-KEYWORD,pikabu
      - DOMAIN-KEYWORD,okko
      - DOMAIN-KEYWORD,wink
      - DOMAIN-KEYWORD,kion
      - DOMAIN-KEYWORD,ozon
      - DOMAIN-KEYWORD,wildberries
      - DOMAIN-KEYWORD,aliexpress
    behavior: classical
  geosite-ru:
    type: http
    behavior: domain
    format: mrs
    url: https://raw.githubusercontent.com/Davoyan/mihomo-rule-sets/main/rules/category-ru.mrs
    path: ./rule-sets/geosite-ru.mrs
    interval: 86400
    proxy: 🚫 Недоступные сайты
  ai:
    type: http
    behavior: domain
    format: mrs
    url: https://raw.githubusercontent.com/MetaCubeX/meta-rules-dat/meta/geo/geosite/category-ai-!cn.mrs
    path: ./rule-sets/ai.mrs
    interval: 86400
    proxy: 🚫 Недоступные сайты
  category-porn:
    type: http
    behavior: domain
    format: mrs
    url: https://raw.githubusercontent.com/MetaCubeX/meta-rules-dat/meta/geo/geosite/category-porn.mrs
    path: ./rule-sets/category-porn.mrs
    interval: 86400
    proxy: 🚫 Недоступные сайты
  geoip-for-ru:
    type: http
    behavior: ipcidr
    format: mrs
    url: https://raw.githubusercontent.com/Davoyan/mihomo-rule-sets/main/ip-for-ru/lists/ips-for-ru.mrs
    path: ./rule-sets/geoip-for-ru.mrs
    interval: 86400
    proxy: 🚫 Недоступные сайты
  geosite-private:
    type: http
    behavior: domain
    format: mrs
    url: https://raw.githubusercontent.com/MetaCubeX/meta-rules-dat/meta/geo/geosite/private.mrs
    path: ./rule-sets/geosite-private.mrs
    interval: 86400
    proxy: 🚫 Недоступные сайты
  geoip-private:
    type: inline
    payload:
      - IP-CIDR,0.0.0.0/8
      - IP-CIDR,10.0.0.0/8
      - IP-CIDR,100.64.0.0/10
      - IP-CIDR,127.0.0.0/8
      - IP-CIDR,169.254.0.0/16
      - IP-CIDR,172.16.0.0/12
      - IP-CIDR,192.0.0.0/24
      - IP-CIDR,192.0.2.0/24
      - IP-CIDR,192.88.99.0/24
      - IP-CIDR,192.168.0.0/16
      - IP-CIDR,198.18.0.0/15
      - IP-CIDR,198.51.100.0/24
      - IP-CIDR,203.0.113.0/24
      - IP-CIDR,224.0.0.0/3
      - IP-CIDR,::/127
      - IP-CIDR,fc00::/7
      - IP-CIDR,fe80::/10
      - IP-CIDR,ff00::/8
    behavior: classical
  discord_domains:
    type: http
    behavior: domain
    format: mrs
    url: https://raw.githubusercontent.com/MetaCubeX/meta-rules-dat/meta/geo/geosite/discord.mrs
    path: ./rule-sets/discord_domains.mrs
    interval: 86400
    proxy: 🚫 Недоступные сайты
  speedtest-net:
    type: http
    behavior: domain
    format: mrs
    url: https://raw.githubusercontent.com/MetaCubeX/meta-rules-dat/meta/geo/geosite/speedtest.mrs
    path: ./rule-sets/speedtest-net.mrs
    interval: 86400
    proxy: 🚫 Недоступные сайты
  remote-control:
    type: http
    behavior: domain
    format: mrs
    url: https://raw.githubusercontent.com/MetaCubeX/meta-rules-dat/meta/geo/geosite/category-remote-control.mrs
    path: ./rule-sets/remote-control.mrs
    interval: 86400
    proxy: 🚫 Недоступные сайты
  inline-blocked-ips:
    type: inline
    payload:
      - IP-CIDR,172.232.25.131/32 #IP для чата Warframe (Пример)
    behavior: classical
  discord_voiceips:
    type: http
    behavior: ipcidr
    format: mrs
    url: https://raw.githubusercontent.com/legiz-ru/mihomo-rule-sets/main/other/discord-voice-ip-list.mrs
    path: ./rule-sets/discord_voiceips.mrs
    interval: 86400
    proxy: 🚫 Недоступные сайты
  discord_vc:
    type: inline
    payload:
      - AND,((IP-CIDR,138.128.136.0/21),(NETWORK,udp),(DST-PORT,50000-50100))
      - AND,((IP-CIDR,162.158.0.0/15),(NETWORK,udp),(DST-PORT,50000-50100))
      - AND,((IP-CIDR,172.64.0.0/13),(NETWORK,udp),(DST-PORT,50000-50100))
      - AND,((IP-CIDR,34.0.0.0/15),(NETWORK,udp),(DST-PORT,50000-50100))
      - AND,((IP-CIDR,34.2.0.0/15),(NETWORK,udp),(DST-PORT,50000-50100))
      - AND,((IP-CIDR,35.192.0.0/12),(NETWORK,udp),(DST-PORT,50000-50100))
      - AND,((IP-CIDR,35.208.0.0/12),(NETWORK,udp),(DST-PORT,50000-50100))
      - AND,((IP-CIDR,5.200.14.128/25),(NETWORK,udp),(DST-PORT,50000-50100))
      - AND,((IP-CIDR,66.22.192.0/18),(NETWORK,udp),(DST-PORT,50000-50100))
    behavior: classical
  refilter_domains:
    type: http
    behavior: domain
    format: mrs
    url: https://raw.githubusercontent.com/legiz-ru/mihomo-rule-sets/main/re-filter/domain-rule.mrs
    path: ./rule-sets/refilter.mrs
    interval: 86400
    proxy: 🚫 Недоступные сайты
  refilter_ipsum:
    type: http
    behavior: ipcidr
    format: mrs
    url: https://github.com/legiz-ru/mihomo-rule-sets/raw/main/re-filter/ip-rule.mrs
    path: ./re-filter/ip-rule.mrs
    interval: 86400
    proxy: 🚫 Недоступные сайты
  youtube:
    type: http
    behavior: domain
    format: mrs
    interval: 86400
    proxy: 🚫 Недоступные сайты
    url: https://raw.githubusercontent.com/MetaCubeX/meta-rules-dat/meta/geo/geosite/youtube.mrs
    path: ./rule-sets/youtube.mrs
  google-deepmind:
    type: http
    behavior: domain
    format: mrs
    interval: 86400
    proxy: 🚫 Недоступные сайты
    url: https://raw.githubusercontent.com/MetaCubeX/meta-rules-dat/meta/geo/geosite/google-deepmind.mrs
    path: ./rule-sets/google-deepmind.mrs
  telegram-ips:
    type: http
    behavior: ipcidr
    format: mrs
    interval: 86400
    proxy: 🚫 Недоступные сайты
    url: https://raw.githubusercontent.com/MetaCubeX/meta-rules-dat/meta/geo/geoip/telegram.mrs
    path: ./rule-sets/telegram-ips.mrs
  telegram-domains:
    type: http
    behavior: domain
    format: mrs
    interval: 86400
    proxy: 🚫 Недоступные сайты
    url: https://raw.githubusercontent.com/MetaCubeX/meta-rules-dat/meta/geo/geosite/telegram.mrs
    path: ./rule-sets/telegram-domains.mrs
  additional-telegram-domains:
    type: inline
    payload:
      - DOMAIN-SUFFIX,exteragram.app
      - DOMAIN-SUFFIX,swiftgram.app
      - DOMAIN-KEYWORD,nicegram
      - DOMAIN-SUFFIX,stel.com
      - DOMAIN-SUFFIX,legra.ph
    behavior: classical
  oisd_big:
    type: http
    behavior: domain
    format: mrs
    url: https://raw.githubusercontent.com/legiz-ru/mihomo-rule-sets/main/oisd/big.mrs
    path: ./rule-sets/oisd_big.mrs
    interval: 86400
    proxy: 🚫 Недоступные сайты
  torrent-trackers:
    type: http
    behavior: domain
    format: mrs
    url: https://raw.githubusercontent.com/legiz-ru/mihomo-rule-sets/main/other/torrent-trackers.mrs
    path: ./rule-sets/torrent-trackers.mrs
    interval: 86400
    proxy: 🚫 Недоступные сайты
  torrent-clients:
    type: http
    behavior: classical
    format: yaml
    url: https://raw.githubusercontent.com/legiz-ru/mihomo-rule-sets/main/other/torrent-clients.yaml
    path: ./rule-sets/torrent-clients.yaml
    interval: 86400
    proxy: 🚫 Недоступные сайты
  ru-apps:
    type: http
    behavior: classical
    format: yaml
    url: https://raw.githubusercontent.com/legiz-ru/mihomo-rule-sets/main/other/ru-app-list.yaml
    path: ./rule-sets/ru-apps.yaml
    interval: 86400
    proxy: 🚫 Недоступные сайты
  ru-inside:
    type: http
    behavior: classical
    format: text
    url: https://raw.githubusercontent.com/itdoginfo/allow-domains/main/Russia/inside-clashx.lst
    path: ./rule-sets/ru-inside.lst
    interval: 86400
    proxy: 🚫 Недоступные сайты
  cloudflare-ips:
    type: http
    behavior: ipcidr
    format: mrs
    url: https://raw.githubusercontent.com/MetaCubeX/meta-rules-dat/meta/geo/geoip/cloudflare.mrs
    path: ./rule-sets/cloudflare-ips.mrs
    interval: 86400
    proxy: 🚫 Недоступные сайты
  quic:
    type: inline
    behavior: classical
    payload:
      - AND,((NETWORK,udp),(DST-PORT,443))

rules:
  # DNS HIJACK
  - DST-PORT,53,DNS-OUT

  # Сервисные правила
  - IP-CIDR,10.95.0.8/32,DIRECT,no-resolve
  - IP-CIDR,10.95.0.9/32,DIRECT,no-resolve

  # Локальную сеть в директ
  - RULE-SET,geoip-private,DIRECT,no-resolve
  - RULE-SET,geosite-private,DIRECT

  # ВПН и всякие Anydesk, Rustdesk, Teamviewer в директ (опционально)
  - PROCESS-NAME-REGEX,(?i).*tailscale.*,DIRECT
  - PROCESS-NAME-REGEX,(?i).*wireguard.*,DIRECT
  - PROCESS-NAME-REGEX,(?i).*netbird.*,DIRECT
  - PROCESS-NAME-REGEX,(?i).*anydesk.*,DIRECT
  - PROCESS-NAME-REGEX,(?i).*rustdesk.*,DIRECT
  - PROCESS-NAME-REGEX,(?i).*teamviewer.*,DIRECT
  - RULE-SET,remote-control,DIRECT

  # Блокировка рекламы (опционально)
  - RULE-SET,oisd_big,REJECT # Списки скомпилированные Legiz

  # Отправляем торренты в DIRECT (опционально)
  - RULE-SET,torrent-clients,DIRECT
  - RULE-SET,torrent-trackers,DIRECT
  - PROCESS-NAME-REGEX,(?i).*torrent.*,DIRECT

  # Делаем REJECT QUIC
  - RULE-SET,quic,REJECT

  # Определялки IP пускаем в прокси, чтобы пользователь видел
  - DOMAIN,ipwho.is,🚫 Недоступные сайты
  - DOMAIN,api.myip.com,🚫 Недоступные сайты
  - DOMAIN,ipapi.co,🚫 Недоступные сайты
  - DOMAIN,ident.me,🚫 Недоступные сайты
  - DOMAIN,ip-api.com,🚫 Недоступные сайты
  - DOMAIN,ipinfo.io,🚫 Недоступные сайты
  - DOMAIN,api.ip.sb,🚫 Недоступные сайты
  - DOMAIN,2ip.io,🚫 Недоступные сайты
  - DOMAIN,2ipcore.com,🚫 Недоступные сайты

  # -----

  # ▶️ YouTube
  - RULE-SET,youtube,▶️ YouTube
  - PROCESS-NAME-REGEX,(?i).*youtube.*,▶️ YouTube

  # ➤ Telegram
  - RULE-SET,telegram-ips,➤ Telegram
  - RULE-SET,telegram-domains,➤ Telegram
  - RULE-SET,additional-telegram-domains,➤ Telegram
  - IP-CIDR,5.28.192.0/18,➤ Telegram,no-resolve # Vodaphone, точно есть
  - IP-CIDR,91.108.0.0/16,➤ Telegram,no-resolve # Более широкий оригинал
  - IP-CIDR,109.239.140.0/24,➤ Telegram,no-resolve # Telegram Network (RU)
  - IP-CIDR,2001:b28:f23c::/47,➤ Telegram,no-resolve # Более широкий оригинал
  - IP-CIDR,2a0a:f280::/29,➤ Telegram,no-resolve # Более широкий оригинал
  - PROCESS-NAME-REGEX,(?i).*ayugram.*,➤ Telegram
  - PROCESS-NAME-REGEX,(?i).*telegram.*,➤ Telegram
  - PROCESS-NAME-REGEX,(?i).*nekogram.*,➤ Telegram
  - PROCESS-NAME-REGEX,(?i).*nagram.*,➤ Telegram
  - PROCESS-NAME-REGEX,(?i).*nekox.*,➤ Telegram

  # 💬 Discord
  - AND,((RULE-SET,cloudflare-ips),(NETWORK,udp),(DST-PORT,19200-19500)),💬 Discord
  - AND,((RULE-SET,cloudflare-ips),(NETWORK,udp),(DST-PORT,50000-50100)),💬 Discord
  - AND,((RULE-SET,discord_voiceips),(NETWORK,udp),(DST-PORT,50000-50100)),💬 Discord
  - RULE-SET,discord_vc,💬 Discord
  - RULE-SET,discord_domains,💬 Discord
  - PROCESS-NAME-REGEX,(?i).*discord.*,💬 Discord
  - PROCESS-NAME-REGEX,(?i).*vesktop.*,💬 Discord

  # 🚫 Недоступные сайты
  - RULE-SET,ru-inside,🚫 Недоступные сайты # ITDog списки доменов недоступные из РФ
  - RULE-SET,refilter_domains,🚫 Недоступные сайты # Re:Filter списки доменов недоступные из РФ
  - RULE-SET,refilter_ipsum,🚫 Недоступные сайты
  - RULE-SET,ru-inline-banned,🚫 Недоступные сайты # Домены набитые вручную (смотрите выше)
  - RULE-SET,inline-blocked-ips,🚫 Недоступные сайты # IP набитые вручную (смотрите выше)
  - RULE-SET,category-porn,🚫 Недоступные сайты # Опционально
  - RULE-SET,ai,🚫 Недоступные сайты # Нейросети
  - RULE-SET,google-deepmind,🚫 Недоступные сайты # Google Gemini и AI Studio
  - RULE-SET,speedtest-net,🚫 Недоступные сайты # speedtest.net

  # ⚪🔵🔴 RU сайты
  - RULE-SET,ru-inline,⚪🔵🔴 RU сайты # Списки набитые вручную (смотрите выше в rule-providers)
  - RULE-SET,ru-apps,⚪🔵🔴 RU сайты # Списки РУ приложений от Legiz

  # geosite-ru включает в себя и собирается автоматически тут (https://github.com/Davoyan/mihomo-rule-sets) -
  # 1. category-ru из репозитория geosite MetacubeX - https://raw.githubusercontent.com/MetaCubeX/meta-rules-dat/meta/geo/geosite/category-ru.list
  # 2. itdoginfo списки Russia outside  - https://raw.githubusercontent.com/itdoginfo/allow-domains/main/Russia/outside-raw.lst
  # 3. hydraponique category-ru списки - https://raw.githubusercontent.com/hydraponique/roscomvpn-geosite/master/data/category-ru
  # 4. yandex, mailru, drweb, kaspersky списки из репозитория geosite MetacubeX
  - RULE-SET,geosite-ru,⚪🔵🔴 RU сайты

  # geo-ip-for-ru (https://github.com/Davoyan/mihomo-rule-sets/tree/main/ip-for-ru/lists)
  # Компилируется из двух гео баз - Ipinfo и Maxmind
  # В список входят IP, если в одной из баз страна подсети RU или BY.
  # А так же зарубежные подсети российских CDN и некоторых провайдеров (например Yandex)
  # Warning! В список входит так же подсети AS, которые могут быть ограничены в России. Например у Cloudflare есть ip адреса с гео RU.
  - RULE-SET,geoip-for-ru,⚪🔵🔴 RU сайты

  # 🌍 Остальные сайты
  - MATCH,🌍 Остальные сайты
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
