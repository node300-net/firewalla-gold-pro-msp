# 🧱 Regelwerk-Konzept – Lesehilfe

> Datei: [`ruleset-concept.yaml`](ruleset-concept.yaml) · Hintergrund: [docs/features.md → Regel-Engine](../../docs/features.md#-3-regel-engine--zero-trust)

## 🧠 Prinzipien

1. 🚪 **Default Deny Ingress** – die Firewalla-Ingress-Firewall bleibt; Ausnahmen nur über Port-Forwards.
2. 🧅 **Defense in Depth** – jede Lab-Isolationsregel existiert **doppelt**: hier (Perimeter) und in den nftables von Node 0 ([Companion `edge.nft`](https://github.com/node300-net/sovereign-datacenter/tree/main/configs/nftables)).
3. 🍯 **Honeypot ≠ Sprungbrett** – Cowrie darf hereingelassen werden, aber kaum hinaus.
4. 🧾 **Git ist die Source of Truth** – weil Firewalla kein Config-Export-Format bietet ([RC-1](../../docs/reality-check.md#rc-1)).

## 🔢 Reihenfolge & Priorität

> ⚠️ Firewalla dokumentiert Prioritäten zwischen Allow- und Block-Regeln in eigenen Help-Artikeln; die genaue Auswertung (spezifischer Scope vs. global, Allow vs. Block) **vor dem Produktivsetzen in der App testen** – z. B. mit `curl` aus VLAN 50 und Blick in *Flows → Matched By* (MSP).

| Schritt | Regeln | Test |
|---|---|---|
| 1 | R-000, R-010 | Von extern `nc -vz <WAN-IP> 22` → Cowrie-Banner |
| 2 | R-100 | Aus VLAN 60: `curl -m5 https://example.com` → Timeout |
| 3 | R-110/R-111 | Aus VLAN 50: `apt update` ✅, `curl https://example.com` ❌ |
| 4 | R-120 | Aus VLAN 50/60: `nc -vz 10.10.10.10 8006` ❌ |
| 5 | R-200/R-210 | Von WG-Admin: Proxmox-GUI ✅; Node 3: MSP-API ✅ |

## 🗂️ Mapping YAML → App

| YAML | Firewalla-App / MSP |
|---|---|
| `action: block/allow` | Rule → Block / Allow |
| `scope.network_cidr` | Rule „Apply to“ → Network bzw. (bei gerouteten Netzen) Target-Bedingung auf IP-Range ⚠️ |
| `target_list` | Target Lists (MSP: 100 × 2000) |
| `schedule` | Rule → Schedule |
| `controls.*` | Controls-Center |
| `protect.*` | Protect → Active Protect / Suricata / DAP |
