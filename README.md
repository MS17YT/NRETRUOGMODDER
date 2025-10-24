# 🎮 3DS Modding Tool (Ms17Mod)

> 🧩 **Tool completo, interattivo e automatizzato** per il *modding di console Nintendo 3DS / 2DS*, scritto interamente in **Python 3**.  
> Include download automatico, guida passo‑passo, backup, strumenti avanzati e gestione completa della scheda SD.

---

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.7%2B-blue?logo=python" alt="Python">
  <img src="https://img.shields.io/badge/OS-Windows%20%7C%20Linux%20%7C%20macOS-lightgrey" alt="OS">
  <img src="https://img.shields.io/badge/Status-Stable-brightgreen" alt="Status">
  <img src="https://img.shields.io/github/license/3DSModdingTeam/3ds-modding-tool" alt="License">
</p>

---

## ✨ Funzionalità principali

| Categoria | Descrizione |
|------------|-------------|
| 🧭 **Interfaccia grafica a menu** | Navigazione chiara, colorata e in stile Nintendo |
| 📦 **Download automatico** | Boot9Strap, Luma3DS, GodMode9, FBI, Homebrew Launcher, Anemone3DS |
| 💾 **Preparazione SD automatica** | Crea la struttura corretta e copia i file essenziali |
| 🎯 **Metodi di modding supportati** | SeedMiner · Frogminer · NTRBoot |
| ⚙️ **Strumenti avanzati** | Diagnostica, verifica file, checksum, pulizia, backup NAND |
| 📚 **Guida interattiva passo‑passo** | Ti accompagna in ogni fase del modding |
| 🧱 **Backup e sicurezza** | Gestione completa dei backup NAND e dei salvataggi |

---

## 🧰 Requisiti

- 🐍 **Python 3.7 o superiore**
- 🌐 Connessione Internet attiva
- 💽 Scheda SD formattata in **FAT32**
- 💻 Sistema operativo: **Windows**, **Linux** o **macOS**

---

## ⚙️ Installazione

1️⃣ Clona il repository o scaricalo come `.zip`:

```bash
git clone https://github.com/<tuo-utente>/3ds-modding-tool.git
cd 3ds-modding-tool
```

2️⃣ Installa automaticamente le dipendenze:

```bash
python installa_dipendenze.py
```

---

## 🚀 Avvio del Tool

Avvia il programma principale:

```bash
python Ms17Mod.py
```

🖥️ Ti apparirà un banner in stile Nintendo e un **menu principale** con queste sezioni:

| Opzione | Descrizione |
|----------|-------------|
| 1️⃣ | Controllo Sistema e Requisiti |
| 2️⃣ | Download File Necessari |
| 3️⃣ | Preparazione Scheda SD |
| 4️⃣ | Metodi di Modding |
| 5️⃣ | Strumenti Avanzati |
| 6️⃣ | Backup e Sicurezza |
| 7️⃣ | Guida Interattiva |
| 8️⃣ | Informazioni e Crediti |
| 9️⃣ | Impostazioni |
| 0️⃣ | Esci |

---

## 🗂️ Struttura del progetto

```
📦 3ds-modding-tool/
├── Ms17Mod.py                # Script principale
├── installa_dipendenze.py    # Installa automaticamente le dipendenze
├── downloads/                # File scaricati automaticamente
├── files/                    # File utente (es. movable.sed)
├── backups/                  # Backup NAND e salvataggi
├── logs/                     # Log di sistema
├── temp/                     # File temporanei
└── config.json               # Configurazione automatica
```

---

## ⚠️ Avvertenze Importanti

> ⚠️ **Usa il tool a tuo rischio e pericolo.**
> 
> - Fai **sempre un backup NAND completo** prima di procedere  
> - Non utilizzare il tool per scopi di pirateria  
> - Nintendo può bannare console modificate  
> - L’autore non è responsabile di eventuali danni o malfunzionamenti  

---

## 👨‍💻 Crediti

| Modulo / Progetto | Autore |
|--------------------|--------|
| Boot9Strap | SciresM |
| Luma3DS | LumaTeam |
| GodMode9 | d0k3 |
| FBI | Steveice10 |
| Homebrew Launcher | fincs |
| Anemone3DS | astronautlevel2 |
| Tool Python | 3DS Modding Team 🧑‍💻 |

---

## 📜 Licenza

Distribuito sotto licenza **MIT**.  
Utilizzabile **solo per scopi educativi** e di preservazione.

---

<p align="center">
  <img src="https://user-images.githubusercontent.com/placeholder/3ds_banner.png" alt="3DS Modding Tool Banner" width="700">
</p>

<p align="center">
  <b>💫 3DS Modding Tool – Il tuo assistente per il modding Nintendo 3DS 💫</b>
</p>
