# RoadCraft - Mod Suite & Reverse Engineering

Raccolta completa di mod, script di automazione e analisi tecnica per il videogioco **RoadCraft** (sviluppato da Saber Interactive).

---

## 🎮 Versioni Supportate

| Versione | Percorso Tipico | Caratteristiche Principali | Cartella |
| :--- | :--- | :--- | :--- |
| **v6.0 (1-Year Anniversary Edition)** | `E:\Giochi\RoadCraft` | Sabbia infinita nativa (`volumeChangeMult = 0.0`), 10x torque su 298 veicoli, rulli 15.3m, asfaltatrici 10.6m, dozer 12m, fix blocco caricamento. | [**v6.0-Anniversary**](./v6.0-Anniversary) |
| **v4.1 (2025 Edition)** | `E:\Giochi\RoadCraft (2025)\RoadCraft` | Ricarica remota globale da qualunque punto della mappa, velocità di caricamento quintuplicata ($5\times$), costo attivazione zero. | [**v4.1-2025**](./v4.1-2025) |

---

## 🏗️ Architettura del Saber Interactive Engine

Il motore di RoadCraft organizza le configurazioni, i veicoli e gli edifici in archivi `.pak` situati in:
`root\paks\client\default\default_other.pak`

### La Tabella Binaria `.pak.cache`
Saber Interactive associa a ciascun archivio `.pak` un indice binario ad accesso rapido (`default_other.pak.cache`). Ciascun file all'interno dell'archivio è rappresentato da un record fisso di 34 byte con metadati binari (versione 6, flag 0x3F, offset a 64 bit, dimensioni e CRC32). Qualsiasi modifica diretta ai file PAK senza la rigenerazione sincronizzata della cache impedisce l'avvio del gioco o causa il fallimento nel caricamento delle classi.

Gli script di automazione inclusi in questo repository si occupano di estrarre, applicare le modifiche e ricompilare sia il `.pak` che il `.pak.cache` in totale sicurezza.

---

## 📂 Struttura della Cartella RoadCraft

```text
RoadCraft/
├── README.md               # Questo file (guida unificata)
├── v6.0-Anniversary/       # Mod Suite per RoadCraft v6.0 (Anniversary Edition)
│   ├── README.md           # Guida specifica v6.0
│   ├── docs/
│   │   └── technical_notes.md  # Log completo, analisi Scaleform UI e volumeChangeMult
│   └── scripts/
│       └── patch_v6_roadcraft.py  # Script di patch automatica e cache builder
└── v4.1-2025/              # Mod Suite per RoadCraft v4.1 (2025)
    ├── README.md           # Guida specifica v4.1
    ├── docs/
    │   └── technical_notes.md  # Note su sandDistance e verifica bidirezionale
    └── scripts/
        └── patch_roadcraft.py     # Script di patch per v4.1
```
