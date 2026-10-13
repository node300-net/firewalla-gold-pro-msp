# ⚙️ Konfigurationsbeispiele

> Zurück zur [README](../README.md)

> [!CAUTION]
> Firewalla wird über **App/MSP** konfiguriert. Die Dateien hier sind **Planungs- und Dokumentationsartefakte** (Source of Truth in Git) bzw. Konfigurationen für die **Gegenstellen** (Linux, Node 3, Switch). Es gibt **kein offizielles Importformat** für Firewalla-Regeln. Platzhalter: `<<PLACEHOLDER>>`, RFC1918-Netze, `203.0.113.0/24` (TEST-NET-3).

| Pfad | Inhalt | Ziel |
|---|---|---|
| [`network/vlan-plan.md`](network/vlan-plan.md) | VLAN-Plan, Port-Map Gold Pro, Routen, NAT | Mensch |
| [`network/vlan-plan.yaml`](network/vlan-plan.yaml) | Derselbe Plan maschinenlesbar (z. B. für Ansible/Doku-Generatoren) | Tooling |
| [`rules/ruleset-concept.yaml`](rules/ruleset-concept.yaml) | Regelwerk-Konzept (Firewalla-Semantik: Block/Allow, Scope, Target) | Mensch + MSP-API-Skripte |
| [`rules/README.md`](rules/README.md) | Erklärung des Regelwerks & Reihenfolge | Mensch |
| [`wireguard/site-to-site.md`](wireguard/site-to-site.md) | Firewalla↔Firewalla & Firewalla↔Linux-Gegenstelle | Mensch |
| [`wireguard/remote-site-linux-server.conf.example`](wireguard/remote-site-linux-server.conf.example) | WireGuard-Server auf Linux/OPNsense-Seite | Gegenstelle |
| [`wireguard/firewalla-client-import.conf.example`](wireguard/firewalla-client-import.conf.example) | Profil zum Import in Firewalla „VPN Client → WireGuard“ | Firewalla-App |
| [`integration/node3-suricata-syslog.md`](integration/node3-suricata-syslog.md) | Was offiziell geht – und was nicht; Architektur Node 3 | Mensch |
| [`integration/huawei-span.example`](integration/huawei-span.example) | Port-Mirroring Uplink → Node 3 (⚠️ Syntax prüfen) | Switch |
| [`integration/suricata-node3.yaml.snippet`](integration/suricata-node3.yaml.snippet) | af-packet + eve-log → syslog | Node 3 |
| [`integration/rsyslog-node3.conf`](integration/rsyslog-node3.conf) | Empfang & Ablage | Node 3 |
| [`integration/msp-alarms-to-syslog.py`](integration/msp-alarms-to-syslog.py) | MSP-API-Poller → Syslog (JSON) | Node 3 |
| [`integration/msp-alarms-to-syslog.service`](integration/msp-alarms-to-syslog.service) · [`.timer`](integration/msp-alarms-to-syslog.timer) | systemd-Units | Node 3 |
