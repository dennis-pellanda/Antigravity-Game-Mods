# SimCity 4 Deluxe Edition - Enhancements & Ordinances Mod Suite

Suite di mod, ottimizzazioni di sistema e strumenti di gioco per **SimCity 4 Deluxe Edition** (v1.1.641.0).

---

## 🌟 Mod Incluse

### 1. Antigravity Ordinances (`Antigravity_Ordinances.dat`)
Un vero e proprio **pannello di controllo integrato** direttamente nei menu di gioco (nella schermata del **Bilancio / Ordinanze**):
- **20 Decreti personalizzati** con etichetta `[MOD]`, testi descrittivi in italiano e **casella di spunta (checkbox)** toggleabile in qualsiasi momento della partita senza riavviare.
- **Funzionalità principali**:
  - `[MOD] Sovvenzione Regionale Illimitata`: accredito mensile netto di **+§500.000**, costo di attivazione zero e criminalità azzerata.
  - `[MOD] Super Rete Elettrica`: consumo energetico ridotto del **99,9%** (energia virtualmente infinita).
  - `[MOD] Super Rete Idrica`: consumo idrico ridotto del **99,9%** (acqua infinita e zero pompe a secco).
  - `[MOD] Purificazione Ambientale`: inquinamento dell'aria abbattuto del **99,9%**.
  - `[MOD] Città Pulita & Rifiuti Zero`: produzione di spazzatura abbattuta del **99,9%**.
  - `[MOD] Iper-Boom Economico RCI`: moltiplicatore massimo per la domanda di residenti ricchi (§§§) e uffici commerciali.
  - `[MOD] Sicurezza & Polizia Totale`: criminalità azzerata al 99,9%.
  - `[MOD] Protezione Antincendio Totale`: edifici ignifughi, zero incendi.
  - `[MOD] Sanità & Istruzione al 100%`: quozienti sanitari ed educativi portati al tetto massimo.
  - `[MOD] Viabilità Fluida & Traffico Zero`: eliminazione della congestione stradale.

### 2. Extra Cheats Plugin (`SimCity 4 Extra Cheats Plugin.dll`)
La DLL ufficiale Maxis/Buggi che sblocca il **menu a tendina contestuale segreto**:
- In partita premi **`Ctrl + X`** sulla tastiera.
- Fai **clic destro** all'interno della casella in alto a sinistra per aprire la lista completa con oltre 50 strumenti di debug (`moolah`, `You don't deserve it`, `FloraBlast`, `BuildingPlop`, ecc.).

---

## 🖥️ Ottimizzazione 2K / 4K & Stabilità Grafica

Nel 2003 SimCity 4 fu sviluppato su DirectX 7 / DirectDraw, che presenta un limite hardware invalicabile di **2048 × 2048 pixel** per le superfici a tutto schermo (causa del crash istantaneo `0x00884fe1` a 4K).

### Soluzione Applicata:
1. **dgVoodoo 2 (v2.87.5)**: Fa da ponte traducendo le chiamate DirectDraw in DirectX 11/12 moderne, consentendo qualsiasi risoluzione senza blocchi.
2. **Risoluzione 2K Nativa (2560 × 1440)**: Rappresenta lo "sweet spot" perfetto che combina una mappa amplissima con un'interfaccia utente leggibile e perfettamente dimensionata.
3. **Parametri di Lancio Protetti**:
   ```text
   -CustomResolution:enabled -r2560x1440x32 -f -d:DirectX -CPUCount:1 -intro:off
   ```
   *(Il parametro `-CPUCount:1` fissa il processo a un singolo core per prevenire freeze del motore sui processori moderni Ryzen/Intel multithread).*

---

## 📁 Struttura

```text
SimCity4/
├── README.md               # Questa documentazione
├── docs/
│   └── technical_notes.md  # Log completo, cause crash DX7, test scaling e configurazioni
├── plugins/                # File pronti per l'installazione in Documents/SimCity 4/Plugins
│   ├── Antigravity_Ordinances.dat
│   └── SimCity 4 Extra Cheats Plugin.dll
└── scripts/
    └── build_ordinances.py # Script sorgente Python per compilare il pacchetto DBPF (.dat)
```

---

## 🛠️ Installazione

Basta copiare il contenuto della cartella `plugins/` in:
`D:\Documenti\SimCity 4\Plugins\` (oppure `Documents\SimCity 4\Plugins\`).

Per disinstallare, basta cancellare i file dalla cartella `Plugins`.
