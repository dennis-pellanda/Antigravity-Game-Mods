# Roadcraft (1-Year Anniversary Edition v6.0) - Documentazione Modifiche & Log Antigravity

Questo documento tiene traccia delle analisi, delle richieste dell'utente e di tutte le modifiche tecniche apportate all'installazione di **Roadcraft: 1-Year Anniversary Edition (v6.0)**.

---

## 1. Dati Installazione & Versione Identificata

- **Cartella Principale di Gioco**: `E:\Giochi\RoadCraft`
- **Eseguibile Principale**: `E:\Giochi\RoadCraft\root\bin\pc\Roadcraft - Retail.exe`
- **Versione Gioco**: Build `v6.0` (*1-Year Anniversary Edition*, Release ByXatab / FitGirl, UserName `RUNE`)
- **Architettura Motore**: Saber Interactive Engine (evoluzione proprietaria del motore SnowRunner / Expeditions)
- **Cartella Salvataggi**:
  - `C:\Users\denni\AppData\Local\Saber\RoadCraftGame\storage\steam\user\76561197960271872\Main\save\SLOT_0`
  - Backup preventivo di sicurezza salvataggio: `SLOT_0_backup_v4.1`

---

## 2. Riepilogo Richieste Utente & Interventi Eseguiti

1. **Risoluzione Blocco Caricamento Mappa (Infinite Loading Screen)**:
   - Diagnosi e risoluzione del blocco indefinito dopo la selezione della mappa.
2. **Sabbia Infinita nei Cassoni Ribaltabili (Dump Trucks)**:
   - Possibilità di posare sabbia per fondazioni e riparazione strade all'infinito senza mai esaurire il carico nel cassone.
   - Spawn dei camion con cassone sempre pieno al 100%.
3. **Potenziamento Coppia Motore (10x Wheel Torque)**:
   - Aumento di un ordine di grandezza della coppia di trazione su tutti i 298 camion/veicoli del gioco.
4. **Allargamento Raggio Operativo Macchine da Cantiere**:
   - **Rullo Compattatore**: larghezza di rullaggio/compattazione estesa a **15.3 m** e **10.0 m**.
   - **Asfaltatrice (Paver)**: larghezza stesura asfalto estesa a **10.6 m** e **10.4 m**, con spessore posa ottimizzato a **0.065**.
   - **Pala Gommata (Wheel Loader) & Dozer**: larghezza lama di spianamento sabbia/terra estesa a **12.0 m**.

---

## 3. Diagnosi Approfondita: Il Bug del Caricamento Infinito

### Sintomo:
All'avvio di una mappa (es. *Dam Break*), il gioco rimaneva fermo sulla schermata di caricamento con l'icona in basso che ruotava all'infinito, senza mai completare l'ingresso in partita.

### Causa Radice Identificata:
Nelle versioni precedenti si era tentato di ottenere sabbia illimitata modificando i file delle cave (`ssl/game/buildings/sand/prop_sand_quarry.prop` e i 21 file `.cls` associati) impostando `maxSand = 99999` e parametri di prossimità a 999999 metri.
Dall'analisi del codice nativo di Saber Interactive all'interno di `Roadcraft - Retail.exe`, è emerso che l'interfaccia grafica HUD Flash/Scaleform calcola i segmenti della barra progressiva della cava tramite la formula:
```cpp
int segmentsCount = (maxSand / 10) - 1;
```
Con `maxSand = 99999`, il valore restituito era pari a circa **9.999 segmenti**.
Durante la fase di caricamento della mappa, i controller UI `UiHudSandQuarryWidgetController` e `UiEagleModeProgressBarQuarryController` tentavano di istanziare e registrare circa 10.000 widget grafici per ciascuna cava presente nella mappa. Questa operazione saturava la coda degli eventi della UI Scaleform, bloccando il thread di sincronizzazione del caricamento e impedendo l'accesso al mondo di gioco.

### Soluzione Applicata:
Tutti i file delle cave di sabbia (`sand_quarry_*.cls` e `prop_sand_quarry.prop`) e le impostazioni hard-mode sono stati ripristinati integralmente ai valori puliti e bilanciati vanilla. Il caricamento mappa è tornato istantaneo (pochi secondi).

---

## 4. Reverse Engineering: La Vera Soluzione per la Sabbia Infinita

### Perché i Vecchi Metodi Fallivano:
1. **Cheat Engine Table v3.0 (`RoadCraft_3.0_SandHax.ct`)**:
   Utilizzava un hook assembly su byte rigidi (`F3 42 0F 11 4C A8 0C` -> `movss [rax+r13*4+0Ch], xmm1`) appartenenti al delta di calcolo delle altezze del terreno su coordinate voxel nella v3.0. Nella v6.0 la sequenza è cambiata e non trovava corrispondenze.
2. **Cheat Engine Scan Float Dinamico**:
   I float rilevati diminuendo/aumentando il carico appartenevano a buffer di velocità angolare e delta fisici temporanei, soggetti a continue fluttuazioni anche a veicolo fermo.

### La Soluzione Architetturale Nativa (`volumeChangeMult = 0.0`):
Analizzando le strutture dati del motore Saber in memoria (RVA `0x14047e684`, classe `PropLoadVolume`), è emerso che il gioco include nativamente un parametro moltiplicatore del consumo di volume:
```ini
volumeChangeMult = 0.0
```
Questo parametro è implementato direttamente dal codice C++ di simulazione dei volumi ed era già utilizzato in modo ufficiale dagli sviluppatori su veicoli specifici (es. `auto_wayfarer_oft96_ts_d.cls` con valore `0.35`).

Configurando nel file centrale `ssl/terraforming/prop_load_volume.prop` e su tutti i 16 camion ribaltabili:
- `volumeChangeMult = 0.0` (il decremento di volume per unità di tempo viene moltiplicato per zero)
- `spawnFull = True` (ogni volta che il camion spawna o viene recuperato, ha il cassone pieno al 100%)
- `fakeSandConsumption = 0.0` (in `prop_load_volume_controller.prop`, azzerato il consumo fittizio)

**Risultato in-game**:
- La fisica del terreno e le particelle continuano a generarsi normalmente sul suolo.
- Le missioni di riparazione stradale e riempimento rilevano regolarmente la sabbia posata.
- Il livello nel cassone **non scende mai**.
- Se il veicolo si ribalta con cassone aperto, continua a produrre sabbia all'infinito senza mai esaurirsi.

---

## 5. Elenco Dettagliato dei Parametri Modificati

Tutte le modifiche sono archiviate in `default_other.pak` e indicizzate nella tabella binaria `default_other.pak.cache`.

### A. Sabbia Infinita (16 file veicolo + 2 file di proprietà):
- `ssl/terraforming/prop_load_volume.prop`:
  - `volumeChangeMult = 0.0`
  - `spawnFull = True`
- `ssl/game/truck/prop_load_volume_controller.prop`:
  - `fakeSandConsumption = 0.0`
- Tutti i 16 camion con cassone ribaltabile in `ssl/game/truck/` (Aramatsu Bowhead, Tayga, Voron, Baikal, Epec, ecc.):
  - `volumeChangeMult = 0.0`
  - `spawnFull = True`

### B. Coppia Motore Decuplicata (10x Torque):
- Modificati **298 file di veicoli e rimorchi** in `ssl/game/truck/`.
- Per ogni blocco `wheelTorque = X`, il valore è stato moltiplicato per 10 (es. da 2.000 a 20.000 Nm, da 4.500 a 45.000 Nm), garantendo aderenza e potenza estreme su fango, salite e detriti.

### C. Macchine Operatrici Allargate:
- **Rulli Compattatori** (`ssl/game/truck/roller/`):
  - Larghezza passata rullaggio estesa a **15.3 m** e **10.0 m**.
- **Asfaltatrici (Paver)** (`ssl/game/truck/paver/`):
  - Larghezza stesa asfalto estesa a **10.6 m** e **10.4 m**.
  - `asphaltHeight = 0.065`.
- **Dozer & Loader** (`ssl/game/truck/dozer/`, `ssl/game/truck/loader/`):
  - Larghezza lama di spianamento sabbia/terra estesa a **12.0 m**.

---

## 6. Architettura File PAK & Cache Binaria `.pak.cache`

Saber Interactive utilizza un sistema a doppio file per gli asset:
1. **`default_other.pak`**: archivio ZIP standard (senza compressione o con compressione Deflate standard).
2. **`default_other.pak.cache`**: tabella binaria strutturata con entry fisse da 34 byte + nome file:
   - `version` (uint32 = 6)
   - `flag` (uint8 = 0x3F)
   - `name_length` (uint32)
   - `file_name` (stringa ASCII con slash diretti `/`)
   - `data_offset` (uint64)
   - `uncompressed_size` (uint64)
   - `compressed_size` (uint64)
   - `compression_method` (uint16: 0 = Store, 8 = Deflate)
   - `crc32` (uint32)

> **Regola fondamentale**: Se il PAK viene alterato senza ricalcolare esattamente gli offset a 64-bit, le dimensioni e i CRC32 di ogni singolo record nella cache binaria, il gioco crasha o non carica gli asset. Lo script `patch_v6_roadcraft.py` ricostruisce entrambi in perfetta sincronia.

---

## 7. Strumenti & Manutenzione

Nella cartella `Antigravity` è memorizzato lo script autonomo di applicazione e modifica:
- **`patch_v6_roadcraft.py`**: Eseguibile con `python patch_v6_roadcraft.py`.
  Estrae il PAK, applica tutte le modifiche sopra elencate, crea i backup automatici e rigenera al 100% la cache binaria `.pak.cache`.

---

## 8. Procedura di Ripristino (Rollback)

In caso di necessità di ripristinare il gioco vanilla al 100%:
1. Chiudere il gioco.
2. Accedere a `E:\Giochi\RoadCraft\root\paks\client\default\`.
3. Eliminare `default_other.pak` e `default_other.pak.cache`.
4. Rimuovere il suffisso `.bak` dai file di backup:
   - `default_other.pak.bak` -> `default_other.pak`
   - `default_other.pak.cache.bak` -> `default_other.pak.cache`
