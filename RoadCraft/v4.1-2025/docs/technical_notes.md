# Roadcraft - Documentazione Modifiche & Log Antigravity

Questo documento tiene traccia delle analisi, delle richieste dell'utente e di tutte le modifiche tecniche apportate all'installazione di **Roadcraft**.

---

## 1. Dati Installazione & Versione Identificata

- **Cartella Principale di Gioco**: `E:\Giochi\RoadCraft (2025)\RoadCraft`
- **Eseguibile**: `E:\Giochi\RoadCraft (2025)\RoadCraft\root\bin\pc\Roadcraft - Retail.exe`
- **Versione Gioco**: `4.1.PATCH.529928 / 529983` (Versione EXE `4.1.0.1`, SteamDB Build `19809550`, Release 08/09/2025, RUNE/ByXatab)
- **Altre Installazioni Rilevate sul PC**:
  - `E:\Giochi\RoadCraft - VECCHIO` (Build `1.6.DEV.462699` - archiviata)
  - `C:\Program Files (x86)\Steam\steamapps\common\RoadCraft Demo` (Build `0.1.DEV.310563` - Demo Steam)
- **Cartella Salvataggi**:
  - `C:\Users\denni\AppData\Local\Saber\RoadCraftGame\storage\steam\user\76561197960271872\Main\save\SLOT_0`

---

## 2. Richieste dell'Utente

1. **Localizzazione e Verifica Versione**:
   - Individuare dove e quale versione del videogioco Roadcraft fosse installata sul PC.
   - Ripristinare il collegamento sul Desktop che puntava a un vecchio percorso non più valido.
2. **Ricarica di Sabbia Globale (Ovunque sulla mappa)**:
   - Risolvere il problema delle mod/tabelle Cheat Engine che non funzionavano o davano errori.
   - Permettere di riempire i cassoni dei camion con la sabbia in qualunque punto della mappa, in qualsiasi momento.
3. **Velocità di Riempimento Aumentata**:
   - Accelerare sensibilmente il tempo necessario per caricare la sabbia nei cassoni.
4. **Risoluzione Errore "Entrare nel raggio di una cava"**:
   - Dopo la prima modifica delle sole cave, il gioco continuava a mostrare l'avviso di distanza non valida.
5. **Opzione Futura (Tenuta in considerazione)**:
   - Cassone con sabbia infinita / senza svuotamento continuo (annotato per futuri sviluppi).

---

## 3. Analisi Tecnica del Saber Interactive Engine

Roadcraft utilizza il motore proprietario di Saber Interactive (evoluzione del motore di SnowRunner / Expeditions).
I file di configurazione del gioco, dei veicoli e degli edifici risiedono in archivi compatti `.pak` situati in `root\paks\client\default\`.

### Architettura dei file `.pak` e `.pak.cache`:
1. **`default_other.pak`**: Archivio in formato standard PKZip / Deflate contenente file di classe (`.cls`), file di proprietà (`.prop`), script (`.ssl`), e definizioni SSO.
2. **`default_other.pak.cache`**: File binario proprietario di indicizzazione rapida.
   - Ogni file presente nel PAK è mappato con un record binario da 34 byte:
     `version (uint32=6) + flag (0x3F) + nome_len (uint32) + nome + data_offset (uint64) + uncompressed_size (uint64) + compressed_size (uint64) + compression_method (uint16) + crc32 (uint32)`.
   - **Nota Critica**: Se si modifica un file compresso all'interno del PAK alterandone i byte o gli offset senza rigenerare byte-per-byte il `.pak.cache`, il gioco crasha all'avvio o non trova più gli asset.

### Perché la prima modifica dava "Entrare nel raggio di una cava":
Nel motore Saber la verifica di prossimità è **doppia e bidirezionale**:
1. **Lato Cava (Edificio)**: La cava definisce un raggio di erogazione (`distance`, `sandDistance`, `sandReceivingDistance`).
2. **Lato Camion (Veicolo)**: Ogni singolo camion con cassone ribaltabile possiede un modulo `prop_load_volume_controller` con un proprio parametro `sandDistance` (tipicamente impostato a 20-50 metri) e un controllo OBB (`isOBBCheck`). Se il camion si trova a più di 35 metri da un punto cava, è il camion stesso a bloccare l'interazione sul controller del volume di carico, mostrando l'avviso a schermo.

---

## 4. Modifiche Applicate

Tutte le modifiche sono state implementate ricompilando `default_other.pak` e ricostruendo integralmente `default_other.pak.cache` tramite script Python dedicato.

### A. Cave di Sabbia (21 file `.cls` + 1 file `.prop`):
- File modificati:
  - `ssl/game/buildings/sand/prop_sand_quarry.prop`
  - Tutti i 21 file `sand_quarry_*.cls` e varianti in `ssl/game/buildings/sand/`
- Valori impostati:
  - `distance = 999999` (raggio globale su tutta la mappa)
  - `sandDistance = 999999`
  - `sandReceivingDistance = 999999`
  - `isOBBCheck = False` (disattivato controllo del bounding box geometrico)
  - `fuelCoinsForActivate = 0` (costo attivazione azzerato)
  - `maxSand = 99999`

### B. Camion con Cassone Ribaltabile (14 file `.cls` + 1 file `.prop`):
- File modificati:
  - `ssl/game/truck/prop_load_volume_controller.prop`
  - Tutti i 14 file `.cls` dei camion da trasporto sabbia in `ssl/game/truck/heavy_dump/`, `medium_dump/`, `light_dump/`, ecc.
- Valori impostati:
  - `sandDistance = 999999` (il camion accetta sabbia a distanza infinita)
  - `focusDistance = 999999`
  - `refillSpeed = 5.0` (velocità di riempimento quintuplicata rispetto al valore base 1.0)

### C. Smart Entry Point:
- File modificato: `ssl/game/truck/heavy_dump/smart_entry_point_truck_sand_storage.sso`
- Rimosso vincolo di auto-esclusione `UsableCheckerIgnoreSelf = { }` che poteva interferire con il trigger remoto.

---

## 5. File di Backup e Ripristino

Prima di ogni operazione sono stati creati copie integrali di backup nei percorsi originali:
- **Backup PAK**: `E:\Giochi\RoadCraft (2025)\RoadCraft\root\paks\client\default\default_other.pak.bak` (230.443.915 byte)
- **Backup Cache**: `E:\Giochi\RoadCraft (2025)\RoadCraft\root\paks\client\default\default_other.pak.cache.bak` (944.623 byte)

### Procedura di Ripristino (Rollback):
Per ripristinare il gioco allo stato originale al 100%:
1. Chiudere il gioco.
2. Andare in `E:\Giochi\RoadCraft (2025)\RoadCraft\root\paks\client\default\`.
3. Eliminare o rinominare `default_other.pak` e `default_other.pak.cache`.
4. Rimuovere l'estensione `.bak` dai file `.bak` per ripristinare gli originali.

---

## 6. Strumenti Creati per Manutenzione Futura

- **Script Generatore**: memorizzato negli script persistenti di Antigravity in `scratch/patch_roadcraft.py`.
- Permette di modificare al volo parametri come `refillSpeed`, capienza, o integrare mod future con ricreazione automatica della tabella binaria `.pak.cache`.
