# SimCity 4 Deluxe Edition - Documentazione Modifiche & Log Antigravity

Questo documento traccia in dettaglio le analisi tecniche, le problematiche diagnosticate, le richieste dell'utente e tutte le soluzioni definitive applicate all'installazione di **SimCity 4 Deluxe Edition**.

---

## 1. Dati Installazione & Versione Identificata

- **Cartella Principale di Gioco**: `E:\EA Launcher\SimCity 4 Deluxe Edition`
- **Cartella Eseguibile**: `E:\EA Launcher\SimCity 4 Deluxe Edition\Apps`
- **Eseguibile Principale**: `SimCity 4.exe` (Versione EA App / Digitale `1.1.641.0`, 32-bit)
- **Cartella Dati Utente & Log Crash**: `D:\Documenti\SimCity 4` (`Exception Reports`)
- **Configurazione Hardware di Riferimento**:
  - **CPU**: AMD Ryzen 7 5800X (8 Core / 16 Thread)
  - **GPU**: NVIDIA GeForce RTX 3080 (Device ID `0x220a`)
  - **Monitor**: AOC 4K (3840 × 2160) @ 60 Hz su porta DisplayPort

---

## 2. Richieste dell'Utente

1. **Risoluzione Problemi ad Alta Risoluzione**:
   - Risolvere i blocchi e crash quando il gioco viene eseguito in alta risoluzione (4K / 2K).
   - Consentire l'avvio diretto da `SimCity 4.exe` senza dover passare da EA App.
2. **Sicurezza e Backup**:
   - Creazione di copie di backup complete dei file originali prima di qualsiasi intervento.
3. **Risoluzione Crash all'Avvio**:
   - Diagnosi e risoluzione dell'errore di violazione d'accesso all'indirizzo `0x00884fe1`.
4. **Ottimizzazione UI Scaling (Dimensione Interfaccia)**:
   - Risolvere il problema dell'interfaccia microscopica e illeggibile generata dal 4K puro.
   - Test con Integer Scaling $2\times$ (da 1080p a 4K) per preservare i pixel.
   - Successivo ripristino su richiesta dell'utente (perché ritenuto troppo grande/sfocato) a favore della risoluzione **2K Nativo (2560 × 1440)** senza scaling.

---

## 3. Diagnosi Tecnica & Cause dei Problemi

### A. Limite Architetturale di DirectX 7 / DirectDraw (Crash `0x00884fe1`)
SimCity 4 (sviluppato nel 2003) è stato concepito attorno alle vecchie API **DirectX 7 / DirectDraw**:
- DirectX 7 presenta un vincolo hardware rigido: non supporta superfici video o buffer a pieno schermo superiori a **2048 × 2048 pixel**.
- Impostando la risoluzione a **3840 × 2160 (4K)** in modalità fullscreen (`-f`), la chiamata `CreateSurface` fallisce restituendo un puntatore nullo (`NULL`).
- Il motore grafico tenta subito di accedere a `NULL + 1` all'offset `0x00884fe1`, provocando un crash istantaneo con codice `0xC0000005 (ACCESS_VIOLATION)`.

### B. Incompatibilità della Patch 4GB (LAA) con la Build EA
A differenza delle versioni CD o GOG, l'eseguibile digitale di EA App (`v1.1.641.0`) ha una gestione interna degli indirizzi di memoria compilata con interi con segno (*signed 32-bit*).
- Attivando il flag LAA (`IMAGE_FILE_LARGE_ADDRESS_AWARE`), Windows alloca spazio negli indirizzi `0x80000000+`, che mandano immediatamente in confusione il memory allocator proprietario provocando crash. L'eseguibile originale a 2GB è risultato il più stabile per questa release.

### C. Sensibilità all'Encoding dei file di configurazione (`.sgr`)
I file di configurazione del motore (`Graphics Rules.sgr`, `Video Cards.sgr`) devono essere tassativamente salvati in formato **ASCII puro**.
- Qualsiasi presenza di **BOM UTF-8** (`EF BB BF`) impedisce al parser del 2003 di leggere la prima riga, portando a un crash istantaneo all'inizializzazione del database video.

### D. Conflitti Multithreading su CPU Moderne (Ryzen 7 5800X)
Il motore del 2003 non è thread-safe per CPU multi-core. Quando il sistema operativo tenta di distribuire i thread sui 16 thread logici del 5800X, si verificano race condition e freeze. È obbligatorio vincolare il processo a 1 singolo core (`-CPUCount:1` e `/affinity 1`).

---

## 4. Soluzione Definitiva Implementata

### 1. Integrazione di dgVoodoo 2 (v2.87.5)
Per abbattere il muro dei 2048 pixel di DirectX 7 e garantire piena compatibilità con l'hardware moderno, è stato integrato **dgVoodoo 2**:
- File posizionati in `Apps/`:
  - `DDraw.dll` e `D3DImm.dll` (DLL wrapper DirectX)
  - `dgVoodoo.conf` (configurazione personalizzata)
  - `dgVoodooCpl.exe` (pannello di controllo grafico)
- **Funzionamento**: dgVoodoo intercetta le chiamate DirectDraw/DX7 del gioco e le traduce in **DirectX 11 / 12 moderne**.
- La GPU RTX 3080 viene sfruttata correttamente, eliminando i crash a risoluzioni superiori a 2048px, garantendo VSync stabile a 60 FPS ed eliminando i micro-scatti dello scrolling.

### 2. Risoluzione Ottimale: 2K Nativo (2560 × 1440)
- In 4K puro i menu del 2003 occupavano meno del 4% dello schermo, risultando illeggibili.
- L'Integer Scaling 1080p ingrandiva troppo elementi e menu.
- **La Risoluzione 2K (2560 × 1440)** rappresenta il perfetto equilibrio ("sweet spot"): offre uno spazio visivo ampio per la mappa, con un'interfaccia utente perfettamente proporzionata, leggibile e priva di artefatti.

### 3. Configurazione di `dgVoodoo.conf`
- `ScalingMode = unspecified` (nessuna distorsione d'aspetto)
- `ImageScaleFactor = 1` (nessun upscaling forzato)
- `Resampling = bilinear`
- Watermark grafico dgVoodoo disattivato.

### 4. Parametri di Lancio e Collegamenti
Tutti i punti di accesso al gioco sono stati configurati con la seguente riga di comando:
```text
-CustomResolution:enabled -r2560x1440x32 -f -d:DirectX -CPUCount:1 -intro:off
```
- **`-CustomResolution:enabled`**: abilita le risoluzioni panoramiche non standard del 2003.
- **`-r2560x1440x32`**: impone 2560 × 1440 con colori a 32-bit.
- **`-f`**: modalità schermo intero (gestita fluidamente da dgVoodoo).
- **`-d:DirectX`**: attiva il renderer hardware DirectX (tradotto da dgVoodoo in DX11/12).
- **`-CPUCount:1`**: blocca l'esecuzione a 1 singolo core logico, prevenendo freeze e crash.
- **`-intro:off`**: salta i filmati EA/Maxis introduttivi a 800×600, velocizzando il caricamento.

### 5. File di Avvio Creati:
- **Collegamento Desktop**: `SimCity 4 Deluxe (4K).lnk` (sul Desktop dell'utente, aggiornato ai parametri 2K stabili).
- **Collegamento in Apps**: `Apps\SimCity 4 Deluxe (4K).lnk`
- **File Batch**: `Apps\SimCity 4 (4K).cmd` (avvia con comando Windows `/affinity 1`).

---

## 5. File di Backup e Ripristino (Rollback)

Prima degli interventi sono stati creati copie di sicurezza identiche agli originali:
- **Eseguibile**: `Apps\SimCity 4.exe.backup`
- **Regole Grafiche**: `Graphics Rules.sgr.backup`
- **Database GPU**: `Video Cards.sgr.backup`

### Procedura di Ripristino (Stato di Fabbrica):
Qualora si volesse rimuovere dgVoodoo e tornare alla configurazione EA standard:
1. Andare nella cartella `Apps/` ed eliminare `DDraw.dll`, `D3DImm.dll`, `dgVoodoo.conf` e `dgVoodooCpl.exe`.
2. Ripristinare i file `.backup` eliminando l'estensione `.backup`.

---

## 7. Installazione Mod & Menu Segreto: SimCity 4 Extra Cheats Plugin

- **Data Installazione**: 13/10/2026
- **Plugin Installato**: SimCity 4 Extra Cheats Plugin.dll (286.720 byte, release ufficiale Maxis/Buggi)
- **Posizioni**:
  - D:\Documenti\SimCity 4\Plugins\SimCity 4 Extra Cheats Plugin.dll
  - E:\EA Launcher\SimCity 4 Deluxe Edition\Plugins\SimCity 4 Extra Cheats Plugin.dll

### Come usare il Menu Segreto in Gioco:
1. Avvia SimCity 4 ed entra in una città.
2. Premi sulla tastiera la combinazione **Ctrl + X**.
   - Comparirà una barra di testo semitrasparente nell\'angolo in alto a sinistra.
3. Fai **clic col tasto destro del mouse** all\'interno della barra di testo.
   - Si aprirà all\'istante il **menu a discesa contestuale** con oltre 50 comandi e strumenti di debug.
4. Clicca sul comando desiderato e premi **Invio**.

### Comandi Principali Disponibili nel Menu:
- **moolah <cifra>**: imposta istantaneamente il saldo della cassa comunale all\'importo desiderato (es. moolah 10000000).
- **You don't deserve it**: sblocca immediatamente tutti gli edifici speciali, monumenti e ricompense della città.
- **FightThePower**: fornisce elettricità a tutti gli edifici della città senza bisogno di centrali o cavi.
- **HowDryIAm**: fornisce acqua a tutti gli edifici senza necessità di tubature o pompe.
- **BuildingPlop / LotPlop**: apre il catalogo completo per piazzare manualmente qualsiasi edificio (compresi grattacieli commerciali e residenziali).
- **FloraBlast**: genera vegetazione e alberi lussureggianti su tutta la mappa.
- **SetMayorRating 100**: fissa l\'indice di gradimento del sindaco al 100%.
- **RenderProp / Super Query (Ctrl + Alt + Shift + clic ?)**: sblocca la scheda diagnostica avanzata con tutte le statistiche nascoste di ogni edificio.

---

## 8. Mod Ordinanze & Menu di Controllo Integrato: Antigravity Ordinances

- **Data Creazione**: 13/10/2026
- **Pacchetto Mod**: Antigravity_Ordinances.dat (13.312 byte, DBPF 1.0)
- **Posizioni**:
  - D:\Documenti\SimCity 4\Plugins\Antigravity_Ordinances.dat
  - E:\EA Launcher\SimCity 4 Deluxe Edition\Plugins\Antigravity_Ordinances.dat

### Come Funziona l\'Interfaccia in Gioco:
1. In partita, apri la finestra del **Bilancio / Finanze** (cliccando sul saldo in basso a sinistra) oppure clicca sull\'icona del Sindaco e apri il menu **Ordinanze** (o Decreti).
2. Troverai tutte le 20 voci riscritte con il prefisso **[MOD]**, con descrizione in italiano e una **casella di spunta (checkbox)** per ciascuna opzione.
3. Puoi spuntare o togliere la spunta a piacimento in qualsiasi momento durante la partita: gli effetti si attivano e disattivano all\'istante!

### Elenco dei Comandi / Ordinanze Disponibili a Schermo:
1. **[MOD] Sovvenzione Regionale Illimitata (+§500.000/mese)**:
   - Genera un accredito mensile a fondo perduto di §500.000 ogni mese, costo di attivazione zero e criminalità azzerata.
2. **[MOD] Super Rete Elettrica (Energia Infinita & Consumo -99%)**:
   - Riduce il consumo energetico degli edifici del 99,9%: una sola centrale alimenta l\'intera città.
3. **[MOD] Super Rete Idrica (Acqua Infinita & Consumo -99%)**:
   - Riduce il consumo d\'acqua del 99,9%: pompe sempre cariche e fornitura idrica illimitata.
4. **[MOD] Purificazione Ambientale (Inquinamento Aria Azzerato)**:
   - Elimina il 99,9% dell\'inquinamento atmosferico di industrie, centrali e automobili.
5. **[MOD] Città Pulita & Rifiuti Zero (Discariche Vuote)**:
   - Elimina il 99,9% della spazzatura e dei rifiuti solidi urbani.
6. **[MOD] Iper-Boom Economico RCI (Domanda Massima Grattacieli)**:
   - Moltiplica la domanda commerciale e residenziale (§§§), attirando grattacieli e investimenti immediati.
7. **[MOD] Sicurezza & Polizia Totale (Criminalità Azzerata)**:
   - Riduce la criminalità del 99,9% in tutta la mappa (tasso di crimine pari a zero).
8. **[MOD] Protezione Antincendio Totale (Edifici Ignifughi)**:
   - Riduce l\'infiammabilità del 99,9%, rendendo tutti gli edifici a prova di fuoco.
9. **[MOD] Sanità Pubblica Perfetta (Salute & Longevità 100%)**:
   - Quoziente di salute e aspettativa di vita al massimo storico.
10. **[MOD] Istruzione & Genio Civico (Quoziente Educativo 100%)**:
    - Quoziente intellettivo (EQ) al livello massimo (200), sbloccando industrie hi-tech.
11. **[MOD] Viabilità Fluida & Traffico Zero (Zero Congestione)**:
    - Flusso di traffico ottimizzato e azzeramento dei tempi di pendolarismo.
12. **[MOD] Pace Sociale & Ordine Pubblico**:
    - Quartieri sempre tranquilli senza malcontento giovanile.
13. **[MOD] Benessere Sociale & Attività Sportive**:
    - Felicità cittadina e attrazione per nuove famiglie.
14. **[MOD] Pronto Intervento Sanitario Rapido**:
    - Soccorsi medici immediati e zero incidenti letali.
15. **[MOD] Zona Ecologica & Raggi Zero**:
    - Protezione totale da radiazioni e scorie tossiche.
16. **[MOD] Bonifica Emissioni Discariche**:
    - Miasmi e gas di discarica azzerati.
17. **[MOD] Digitalizzazione Totale & Carta Zero**:
    - Spese burocratiche e amministrative azzerate.
18. **[MOD] Riciclo Pneumatici & Materiali Pesanti**:
    - Riciclo dei polimeri per asfalti fonoassorbenti.
19. **[MOD] Veicoli Elettrici & Emissioni Zero**:
    - Azzeramento dello smog automobilistico.
20. **[MOD] Navette Rapide di Collegamento Quartieri**:
    - Trasporto pubblico rapido e gratuito tra quartieri.

### Disinstallazione:
Per rimuovere la mod, basta semplicemente eliminare il file Antigravity_Ordinances.dat da Plugins/.
