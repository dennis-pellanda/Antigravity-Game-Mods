# Antigravity Game Mods

Raccolta centralizzata di mod, toolchain di reverse engineering, script di compilazione e documentazione tecnica per giochi PC.

---

## 🎮 Giochi Supportati

| Gioco | Versioni Target | Mod & Funzionalità Principali | Cartella |
| :--- | :--- | :--- | :--- |
| **RoadCraft** | `v6.0` (*Anniversary*)<br>`v4.1` (*2025*) | **v6.0**: Sabbia infinita nativa (`volumeChangeMult = 0.0`), coppia 10x su 298 camion, rulli 15.3m, asfaltatrici 10.6m, lame 12m, fix caricamento.<br>**v4.1**: Ricarica remota ovunque, velocità $5\times$, attivazione zero. | [**RoadCraft**](./RoadCraft) |
| **SimCity 4 Deluxe Edition** | `1.1.641.0` (EA App / Maxis) | Pacchetto Ordinanze con pannello in-game a spunte (fondi infiniti, energia, acqua, inquinamento zero, RCI max), sblocco Extra Cheats DLL, fix 2K/4K dgVoodoo2, fix crash `0x00884fe1`. | [**SimCity 4 Deluxe Edition**](./SimCity%204%20Deluxe%20Edition) |

---

## 📁 Struttura del Repository

```text
Antigravity-Game-Mods/
├── RoadCraft/                      # Mod e toolchain per RoadCraft (Saber Engine)
│   ├── README.md                   # Panoramica unificata RoadCraft
│   ├── v6.0-Anniversary/           # Mod Suite v6.0 (Anniversary Edition)
│   │   ├── README.md
│   │   ├── docs/technical_notes.md
│   │   └── scripts/patch_v6_roadcraft.py
│   └── v4.1-2025/                  # Mod Suite v4.1 (2025 Edition)
│       ├── README.md
│       ├── docs/technical_notes.md
│       └── scripts/patch_roadcraft.py
├── SimCity 4 Deluxe Edition/       # Mod e tool per SimCity 4 Deluxe Edition
│   ├── README.md                   # Guida utente, elenco ordinanze e fix grafico
│   ├── docs/technical_notes.md     # Log diagnostica, crash 0x00884fe1, fix DirectX 7
│   ├── plugins/                    # Mod pronte per l'installazione in Plugins
│   │   ├── Antigravity_Ordinances.dat
│   │   └── SimCity 4 Extra Cheats Plugin.dll
│   └── scripts/build_ordinances.py # Script Python per compilare pacchetti DBPF (.dat)
├── .gitignore
└── README.md                       # Questo file
```

---

## 🛡️ Filosofia e Sicurezza

Tutte le mod in questo repository sono state progettate per:
1. **Preservare l'integrità dei giochi**: Creazione automatica di copie di backup (`.bak`) prima di qualunque modifica.
2. **Modularità e Rollback**: Tutte le modifiche possono essere rimosse all'istante ripristinando i file originali o eliminando i file `.dat`/`.dll` dalle cartelle `Plugins`.
3. **Tracciabilità Totale**: Ogni modifica ha le proprie note tecniche approfondite conservate nelle relative cartelle `docs/technical_notes.md`.
