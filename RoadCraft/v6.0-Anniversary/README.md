# RoadCraft: 1-Year Anniversary Edition (v6.0) - Mod Suite

Mod suite definitiva e toolchain di reverse engineering per **RoadCraft: 1-Year Anniversary Edition (v6.0)** (Saber Interactive Engine).

---

## 🎯 Funzionalità Incluse

1. **Sabbia Infinita Nativa (`volumeChangeMult = 0.0`)**:
   - I cassoni ribaltabili (*dump truck*) non esauriscono mai la sabbia durante la posa su strada o il riempimento di fondamenta.
   - La fisica del terreno e i trigger di missione funzionano al 100% normalmente.
   - Tutti i camion spawnano con cassone pieno (`spawnFull = True`) e il consumo fittizio è azzerato (`fakeSandConsumption = 0.0`).
   - Se il veicolo si ribalta a cassone aperto, continua a produrre sabbia all'infinito.
2. **Coppia Motore Decuplicata (10x Wheel Torque)**:
   - Aumento di un fattore 10 della coppia su tutti i 298 camion e veicoli del gioco per superare fango, pendenze ripide e carichi pesanti senza alcuno sforzo.
3. **Rullo Compattatore a Raggio Esteso**:
   - Larghezza di rullaggio e compattazione estesa a **15.3 m** e **10.0 m** (asfalta un'intera carreggiata in una singola passata).
4. **Asfaltatrici (Paver) Allargate**:
   - Larghezza di stesa asfalto estesa a **10.6 m** e **10.4 m**, con spessore di posa `asphaltHeight = 0.065`.
5. **Wheel Loader & Dozer con Lama da 12 Metri**:
   - Raggio di spianamento della sabbia e terra portato a **12.0 m**.
6. **Risoluzione Bug Blocco Caricamento Infinito (Infinite Loading)**:
   - Diagnosi e fix del crash/blocco causato dai vecchi hack di cava (`maxSand = 99999`) che saturavano la UI Flash/Scaleform con ~10.000 widget.

---

## 📁 Struttura

```text
v6.0-Anniversary/
├── README.md               # Questa documentazione
├── docs/
│   └── technical_notes.md  # Analisi reverse engineering, strutture Saber e disassembly
└── scripts/
    └── patch_v6_roadcraft.py  # Script Python per applicare le mod e rigenerare .pak.cache
```

---

## 🚀 Come Applicare la Mod

1. Assicurati che il gioco sia chiuso.
2. Esegui lo script:
   ```bash
   python scripts/patch_v6_roadcraft.py
   ```
3. Lo script:
   - Crea un backup completo dei file originali (`default_other.pak.bak` e `.pak.cache.bak`).
   - Inietta la proprietà nativa `volumeChangeMult = 0.0` e `spawnFull = True` nei camion e nei file `.prop`.
   - Modifica i parametri di coppia su 298 veicoli.
   - Allarga rulli, asfaltatrici e pale operatrici.
   - Ripristina i file cava a valori puliti vanilla.
   - Rigenera byte-per-byte l'archivio ZIP e la tabella binaria `.pak.cache` a 34 byte.

---

## 🔄 Ripristino (Rollback)

In qualunque momento è possibile ripristinare il gioco vanilla al 100%:
1. Vai in `E:\Giochi\RoadCraft\root\paks\client\default\`.
2. Cancella `default_other.pak` e `default_other.pak.cache`.
3. Rinomina `default_other.pak.bak` e `default_other.pak.cache.bak` rimuovendo l'estensione `.bak`.
