# RoadCraft (2025) - Remote Sand Refill & Speed Mod

Mod e toolchain di reverse engineering per **Roadcraft** (Saber Interactive Engine).

---

## 🎯 Obiettivi della Mod

1. **Ricarica Sabbia Globale**: Permette a qualsiasi camion con cassone ribaltabile (*dump truck*) di caricare sabbia in qualunque punto della mappa, eliminando i vincoli di prossimità fisica alle cave.
2. **Velocità di Riempimento Accelerata (\\times$)**: Quintuplica la velocità di caricamento della sabbia nel cassone per ridurre i tempi morti di attesa.
3. **Costo di Attivazione Azzerato**: Rende l\'approvvigionamento accessibile senza vincoli di carburante/monete.

---

## ⚙️ Architettura Tecnica (Saber Engine)

Il motore di gioco (evoluzione del Saber Engine di SnowRunner/Expeditions) archivia i file di configurazione in archivi .pak situati in:

oot\\paks\\client\\default\\default_other.pak

### Il problema della verifica bidirezionale di distanza
Nei file originali, la restrizione di ricarica è implementata su due livelli indipendenti:
- **Lato Cava (ssl/game/buildings/sand/)**: definisce distance, sandDistance, sandReceivingDistance e il check geometrico OBB (isOBBCheck).
- **Lato Camion (ssl/game/truck/)**: ciascun veicolo ribaltabile possiede un modulo prop_load_volume_controller con un proprio parametro sandDistance (impostato a 20-50 metri). Se il camion dista più di 35m da una cava, è il veicolo stesso a rifiutare il trigger.

### Ricostruzione della Tabella Binaria .pak.cache
Saber Interactive associa a ciascun archivio .pak un file binario .pak.cache contenente record fissi da 34 byte con CRC32, offset esatti e lunghezze dei file compressi. Modificare il PAK senza ricreare la cache causa crash all\'avvio. Il nostro script patch_roadcraft.py ricostruisce sia il PAK sia la tabella binaria .pak.cache con precisione byte-per-byte.

---

## 📁 Struttura

`	ext
RoadCraft/
├── README.md               # Questa documentazione
├── docs/
│   └── technical_notes.md  # Log completo, percorsi e dettagli di reverse engineering
└── scripts/
    └── patch_roadcraft.py  # Script di patch automatica e rigenerazione binaria della cache
`

---

## 🛠️ Come Applicare la Mod

1. Assicurati che il gioco sia chiuso.
2. Esegui lo script di patch:
   `ash
   python scripts/patch_roadcraft.py
   `
3. Lo script:
   - Crea un backup di sicurezza (default_other.pak.bak e .pak.cache.bak).
   - Modifica i 21 file .cls e il file .prop delle cave.
   - Modifica i 14 file .cls dei camion da trasporto e il controller del volume.
   - Ricostruisce il file di indice binario .pak.cache.
   - Verifica l\'integrità dei dati.

---

## 🔄 Ripristino (Rollback)

In qualsiasi momento è possibile tornare alla versione originale:
1. Vai in 
oot\\paks\\client\\default\\.
2. Elimina default_other.pak e default_other.pak.cache.
3. Rinomina i file .bak rimuovendo l\'estensione .bak.\n