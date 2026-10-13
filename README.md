# Antigravity Game Mods

Raccolta centralizzata di mod, toolchain di reverse engineering, script di compilazione e documentazione tecnica per giochi PC.

---

## 🎮 Giochi Supportati

| Gioco | Versione Target | Mod & Funzionalità Principali |
| :--- | :--- | :--- |
| **[RoadCraft (2025)](./RoadCraft)** | `4.1.PATCH.529928 / 529983` (Saber Interactive) | Ricarica sabbia globale ovunque sulla mappa, velocità di riempimento $5\times$, costo attivazione zero, rigenerazione binaria `.pak.cache`. |
| **[SimCity 4 Deluxe](./SimCity4)** | `1.1.641.0` (EA App / Maxis) | Pacchetto Ordinanze con pannello in-game a spunte (fondi infiniti, energia, acqua, inquinamento zero, RCI max), sblocco Extra Cheats DLL, fix 2K/4K dgVoodoo2. |

---

## 📁 Struttura del Repository

```text
Antigravity-Game-Mods/
├── RoadCraft/                  # Mod e tool per RoadCraft (2025)
│   ├── README.md               # Guida utente e spiegazione tecnica
│   ├── docs/
│   │   └── technical_notes.md  # Log completo, percorsi e dettagli Saber Engine
│   └── scripts/
│       └── patch_roadcraft.py  # Script Python per patchare default_other.pak e ricreare .pak.cache
├── SimCity4/                   # Mod e tool per SimCity 4 Deluxe Edition
│   ├── README.md               # Guida utente, elenco ordinanze e fix grafico
│   ├── docs/
│   │   └── technical_notes.md  # Log diagnostica, crash 0x00884fe1, fix DirectX 7
│   ├── plugins/                # Mod pronte per l'installazione in Plugins
│   │   ├── Antigravity_Ordinances.dat
│   │   └── SimCity 4 Extra Cheats Plugin.dll
│   └── scripts/
│       └── build_ordinances.py # Script Python per compilare pacchetti DBPF (.dat)
├── .gitignore
└── README.md                   # Questo file
```

---

## 🛡️ Filosofia e Sicurezza

Tutte le mod in questo repository sono state progettate per:
1. **Preservare l'integrità dei giochi**: Creazione automatica di backup prima di qualunque modifica.
2. **Modularità e Rollback**: Tutte le modifiche possono essere rimosse all'istante ripristinando i file originali o eliminando i file `.dat`/`.dll` dalle cartelle `Plugins`.
3. **Tracciabilità Totale**: Ogni modifica ha le proprie note tecniche approfondite conservate nella cartella `docs/`.
