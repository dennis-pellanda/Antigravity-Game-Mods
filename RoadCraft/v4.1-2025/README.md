# RoadCraft (v4.1 - 2025 Edition) - Sand Refill Speed & Zero Cost Mod

Mod e toolchain di reverse engineering per **Roadcraft** build 2025 (`4.1.PATCH.529928 / 529983`, Saber Interactive Engine).

---

## 🎯 Obiettivi della Mod

1. **Velocità di Riempimento Accelerata ($5\times$)**: Quintuplica la velocità di caricamento della sabbia nei cassoni ribaltabili (`refillSpeed = 5.0`) per ridurre drasticamente i tempi morti di attesa presso le cave.
2. **Costo di Attivazione Azzerato**: Rende l'approvvigionamento accessibile senza vincoli di carburante/monete (`fuelCoinsForActivate = 0`).
3. **Analisi e Limiti di Prossimità (v4.1)**: Nella build 4.1, i tentativi di ricarica remota ovunque sulla mappa tramite modifica dei parametri `sandDistance` non funzionano, in quanto la logica di attivazione del caricamento è vincolata internamente dall'engine alla presenza fisica del veicolo nell'area della cava. *(La possibilità di operare con sabbia infinita ovunque è stata poi resa possibile nella versione v6.0 tramite l'override nativo `volumeChangeMult = 0.0`).*

---

## ⚙️ Architettura Tecnica (Saber Engine)

Il motore di gioco archivia i file di configurazione in archivi `.pak` situati in:
`root\paks\client\default\default_other.pak`

### Ricostruzione della Tabella Binaria `.pak.cache`
Saber Interactive associa a ciascun archivio `.pak` un file binario `.pak.cache` contenente record fissi da 34 byte con CRC32, offset esatti e lunghezze dei file compressi. Modificare il PAK senza ricreare la cache causa crash all'avvio. Lo script `patch_roadcraft.py` ricostruisce sia il PAK sia la tabella binaria `.pak.cache` con precisione byte-per-byte.

---

## 📁 Struttura

```text
v4.1-2025/
├── README.md               # Questa documentazione
├── docs/
│   └── technical_notes.md  # Log completo, percorsi e dettagli tecnici
└── scripts/
    └── patch_roadcraft.py  # Script di patch automatica e rigenerazione binaria della cache
```

---

## 🛠️ Come Applicare la Mod

1. Assicurati che il gioco sia chiuso.
2. Esegui lo script di patch:
   ```bash
   python scripts/patch_roadcraft.py
   ```
3. Lo script:
   - Crea un backup di sicurezza (`default_other.pak.bak` e `.pak.cache.bak`).
   - Modifica i parametri di costo e parametri cava nei 21 file `.cls` e nel file `.prop`.
   - Modifica la velocità di riempimento nei 14 file `.cls` dei camion da trasporto e nel controller del volume.
   - Ricostruisce il file di indice binario `.pak.cache`.
   - Verifica l'integrità dei dati.

---

## 🔄 Ripristino (Rollback)

In qualsiasi momento è possibile tornare alla versione originale:
1. Vai in `root\paks\client\default\`.
2. Elimina `default_other.pak` e `default_other.pak.cache`.
3. Rinomina i file `.bak` rimuovendo l'estensione `.bak`.