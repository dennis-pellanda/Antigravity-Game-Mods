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

## 2. Richieste dell'Utente & Esito Tecnico

1. **Localizzazione e Verifica Versione**:
   - Individuare dove e quale versione del videogioco Roadcraft fosse installata sul PC.
   - Ripristinare il collegamento sul Desktop che puntava a un vecchio percorso non più valido.
2. **Tentativo Ricarica di Sabbia Globale (Non funzionante in v4.1)**:
   - Tentativo di permettere il riempimento dei cassoni da qualsiasi punto della mappa forzando parametri di distanza (`sandDistance`).
   - **Esito riscontrato**: *Non funzionante*. La ricarica remota ovunque non ha mai operato con successo nella v4.1 perché la logica dell'engine esige la presenza fisica presso la cava (funzionalità poi risolta nella v6.0 tramite la proprietà nativa `volumeChangeMult = 0.0` per sabbia infinita).
3. **Velocità di Riempimento Aumentata (Funzionante)**:
   - Accelerare sensibilmente il tempo necessario per caricare la sabbia nei cassoni presso le cave (impostato `refillSpeed = 5.0`).
4. **Costo di Attivazione Cave Azzerato (Funzionante)**:
   - Azzeramento del carburante/monete richiesto dalle cave (`fuelCoinsForActivate = 0`).

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

### Limite della verifica di distanza in v4.1:
Nel motore Saber la verifica di prossimità alle cave è vincolata internamente:
- Anche provando a incrementare `distance` o `sandDistance` a valori elevati nei file `.cls`/`.prop`, il trigger interattivo di aggancio UI e avvio erogazione richiede la prossimità fisica all'edificio cava. La ricarica remota da ovunque non è quindi ottenibile tramite semplici modifiche ai file di configurazione nella v4.1.

---

## 4. Modifiche Applicate

Tutte le modifiche sono state implementate ricompilando `default_other.pak` e ricostruendo integralmente `default_other.pak.cache` tramite script Python dedicato.

### A. Modifiche Funzionanti:
1. **Camion con Cassone Ribaltabile (14 file `.cls` + 1 file `.prop`)**:
   - `ssl/game/truck/prop_load_volume_controller.prop` e camion in `ssl/game/truck/heavy_dump/`, `medium_dump/`, `light_dump/`, ecc.
   - `refillSpeed = 5.0` (velocità di riempimento quintuplicata rispetto al valore base 1.0 presso le cave).
2. **Costo Cave Azzerato (21 file `.cls`)**:
   - File `sand_quarry_*.cls` in `ssl/game/buildings/sand/`.
   - `fuelCoinsForActivate = 0` (costo attivazione azzerato).

### B. Parametri Sperimentali di Distanza (Non Efficaci):
- I parametri `distance = 999999`, `sandDistance = 999999` e `isOBBCheck = False` applicati a cave e camion rimangono nel file come tentativo storico, ma non consentono l'erogazione remota da tutta la mappa. Per ottenere l'effetto desiderato di operare ovunque senza esaurire la sabbia, la soluzione definitiva è stata implementata nella versione **v6.0** con il parametro `volumeChangeMult = 0.0`.

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
