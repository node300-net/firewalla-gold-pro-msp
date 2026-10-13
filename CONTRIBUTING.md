# 🤝 Beitragen

Danke für dein Interesse an **Firewalla Gold Pro + MSP**! Companion-Repo: [node300-net/sovereign-datacenter](https://github.com/node300-net/sovereign-datacenter).

## Grundsätze

1. **Ehrlich bleiben.** Keine erfundenen Benchmarks oder Preise. Jede Zahl braucht einen **Link** oder die Markierung **⚠️ Schätzung/Annahme** mit Begründung.
2. **Datum nennen.** Preise und Features ändern sich schnell (Firewalla-App, MSP-Releases). Bei Änderungen den **Recherchestand** aktualisieren.
3. **Herstellerneutral.** Kein Affiliate-Link, keine Werbesprache. Schwächen gehören in den [Reality Check](docs/reality-check.md) – auch die der Konkurrenz.
4. **Platzhalter klar markieren.** `<<PLACEHOLDER>>`, RFC1918-Netze, `203.0.113.0/24` (TEST-NET-3).
5. **Keine Secrets.** Keine MSP-Tokens, WireGuard-Keys, öffentlichen IPs, MSP-Domains oder Box-GIDs.
6. **Sprache.** Dokumentation auf **Deutsch**; Fachbegriffe (IDS/IPS, WireGuard, Smart Queue …) dürfen Englisch bleiben.

## Workflow

```bash
git checkout -b docs/kurze-beschreibung
# Änderungen …
git add -A
git commit -m "docs: MSP-Preise auf Stand 2026-11 aktualisiert"   # docs:/feat:/fix:/chore:
# Pull Request mit Quellen-Links + Hinweis, welche Tabellen betroffen sind
```

## Besonders willkommen

- 📏 **Eigene Messungen** (iperf3, Suricata an/aus, PPPoE, CAKE) **mit Methodik**
- 🔌 Erfahrungen mit **10GBASE-T-SFP+-Modulen** an Huawei S220S / Intel X710
- 🧾 Aktuelle **Angebotspreise** (anonymisiert) für FortiGate/Sophos/Palo Alto in CH/FL/EU
- 🐍 Verbesserungen am MSP-API-Poller (Schema-Änderungen, Webhook-Receiver)

## Lizenz

Mit deinem Beitrag akzeptierst du: Code/Configs unter **MIT**, Doku unter **CC BY-SA 4.0** (siehe [LICENSE](LICENSE)).
