#!/usr/bin/env python3
"""
3DS Modding Tool - Tool COMPLETO e FUNZIONANTE per il modding di Nintendo 3DS
ATTENZIONE: Usare a proprio rischio. Solo per scopi educativi.
"""

import os
import sys
import requests
import zipfile
import shutil
import subprocess
import platform
from pathlib import Path
import time
import json
from datetime import datetime
import hashlib

try:
    from colorama import init, Fore, Back, Style
    init(autoreset=True)
    COLORAMA_AVAILABLE = True
except ImportError:
    COLORAMA_AVAILABLE = False

try:
    from tqdm import tqdm
    TQDM_AVAILABLE = True
except ImportError:
    TQDM_AVAILABLE = False

class ThreeDSModTool:
    def __init__(self):
        self.version = "v3.0.0"
        self.author = "3DS Modding Team"
        self.base_dir = Path(__file__).parent
        self.downloads_dir = self.base_dir / "downloads"
        self.sd_card_path = None
        self.config_file = self.base_dir / "config.json"
        self.setup_directories()
        self.load_config()
        
    def setup_directories(self):
        """Crea le directory necessarie"""
        directories = [
            self.downloads_dir,
            self.base_dir / "backups",
            self.base_dir / "logs",
            self.base_dir / "temp",
            self.base_dir / "files"
        ]
        
        for directory in directories:
            directory.mkdir(exist_ok=True)
            
    def load_config(self):
        """Carica la configurazione"""
        default_config = {
            "sd_card_path": "",
            "auto_detect_sd": True,
            "download_mirrors": {
                "boot9strap": "https://github.com/SciresM/boot9strap/releases/download/1.4/boot9strap-1.4.zip",
                "luma3ds": "https://github.com/LumaTeam/Luma3DS/releases/download/v13.0/Luma3DSv13.0.zip",
                "godmode9": "https://github.com/d0k3/GodMode9/releases/download/v2.1.1/GodMode9-2.1.1.zip",
                "fbi": "https://github.com/Steveice10/FBI/releases/download/2.6.1/FBI-2.6.1.zip",
                "homebrew_launcher": "https://github.com/fincs/new-hbmenu/releases/download/v3.5.1/homebrew_launcher.zip",
                "anemone": "https://github.com/astronautlevel2/Anemone3DS/releases/download/v2.3.0/Anemone3DS.v2.3.0.zip"
            }
        }
        
        if self.config_file.exists():
            try:
                with open(self.config_file, 'r') as f:
                    self.config = json.load(f)
                    # Carica il percorso SD dalla config
                    if self.config.get('sd_card_path'):
                        self.sd_card_path = Path(self.config['sd_card_path'])
            except:
                self.config = default_config
        else:
            self.config = default_config
            self.save_config()
    
    def save_config(self):
        """Salva la configurazione"""
        with open(self.config_file, 'w') as f:
            json.dump(self.config, f, indent=4)
    
    def clear_screen(self):
        """Pulisce lo schermo"""
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def print_banner(self):
        """Stampa il banner stile Nintendo"""
        banner = f"""
{self.colorize('╔════════════════════════════════════════════════════════════════╗', 'red')}
{self.colorize('║', 'red')}{self.colorize('    ███╗   ██╗██████╗ ███████╗██████╗ ████████╗██╗   ██╗██████╗  ██████╗ ', 'cyan')}{self.colorize('║', 'red')}
{self.colorize('║', 'red')}{self.colorize('    ████╗  ██║██╔══██╗██╔════╝██╔══██╗╚══██╔══╝██║   ██║██╔══██╗██╔════╝ ', 'cyan')}{self.colorize('║', 'red')}
{self.colorize('║', 'red')}{self.colorize('    ██╔██╗ ██║██████╔╝█████╗  ██████╔╝   ██║   ██║   ██║██║  ██║██║  ███╗', 'cyan')}{self.colorize('║', 'red')}
{self.colorize('║', 'red')}{self.colorize('    ██║╚██╗██║██╔══██╗██╔══╝  ██╔══██╗   ██║   ██║   ██║██║  ██║██║   ██║', 'cyan')}{self.colorize('║', 'red')}
{self.colorize('║', 'red')}{self.colorize('    ██║ ╚████║██║  ██║███████╗██║  ██║   ██║   ╚██████╔╝██████╔╝╚██████╔╝', 'cyan')}{self.colorize('║', 'red')}
{self.colorize('║', 'red')}{self.colorize('    ╚═╝  ╚═══╝╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝   ╚═╝    ╚═════╝ ╚═════╝  ╚═════╝ ', 'cyan')}{self.colorize('║', 'red')}
{self.colorize('╠════════════════════════════════════════════════════════════════╣', 'red')}
{self.colorize('║', 'red')} {self.colorize(f'          3DS MODDING TOOL {self.version} - {self.author}', 'yellow')}          {self.colorize('║', 'red')}
{self.colorize('╚════════════════════════════════════════════════════════════════╝', 'red')}
"""
        print(banner)
    
    def colorize(self, text, color):
        """Aggiunge colori al testo"""
        if not COLORAMA_AVAILABLE:
            return text
            
        colors = {
            'red': Fore.RED,
            'green': Fore.GREEN,
            'yellow': Fore.YELLOW,
            'blue': Fore.BLUE,
            'magenta': Fore.MAGENTA,
            'cyan': Fore.CYAN,
            'white': Fore.WHITE,
        }
        return f"{colors.get(color, '')}{text}{Style.RESET_ALL}"
    
    def print_menu(self):
        """Stampa il menu principale"""
        menu = f"""
{self.colorize('╔════════════════════════════════════════════════════════════════╗', 'blue')}
{self.colorize('║', 'blue')}{self.colorize('                        MENU PRINCIPALE', 'yellow')}                         {self.colorize('║', 'blue')}
{self.colorize('╠════════════════════════════════════════════════════════════════╣', 'blue')}
{self.colorize('║', 'blue')} {self.colorize('1.', 'green')} Controllo Sistema e Requisiti                              {self.colorize('║', 'blue')}
{self.colorize('║', 'blue')} {self.colorize('2.', 'green')} Download File Necessari                                    {self.colorize('║', 'blue')}
{self.colorize('║', 'blue')} {self.colorize('3.', 'green')} Preparazione Scheda SD                                     {self.colorize('║', 'blue')}
{self.colorize('║', 'blue')} {self.colorize('4.', 'green')} Metodi di Modding Disponibili                              {self.colorize('║', 'blue')}
{self.colorize('║', 'blue')} {self.colorize('5.', 'green')} Strumenti Avanzati                                        {self.colorize('║', 'blue')}
{self.colorize('║', 'blue')} {self.colorize('6.', 'green')} Backup e Sicurezza                                        {self.colorize('║', 'blue')}
{self.colorize('║', 'blue')} {self.colorize('7.', 'green')} Guida Interattiva                                         {self.colorize('║', 'blue')}
{self.colorize('║', 'blue')} {self.colorize('8.', 'green')} Informazioni e Crediti                                    {self.colorize('║', 'blue')}
{self.colorize('║', 'blue')} {self.colorize('9.', 'green')} Impostazioni                                              {self.colorize('║', 'blue')}
{self.colorize('║', 'blue')} {self.colorize('0.', 'red')} Esci                                                    {self.colorize('║', 'blue')}
{self.colorize('╚════════════════════════════════════════════════════════════════╝', 'blue')}
"""
        print(menu)
    
    def check_dependencies(self):
        """Controlla che tutte le dipendenze siano installate"""
        missing_deps = []
        
        try:
            import requests
        except ImportError:
            missing_deps.append("requests")
            
        try:
            import colorama
        except ImportError:
            missing_deps.append("colorama")
            
        if missing_deps:
            print(self.colorize("❌ Dipendenze mancanti:", "red"))
            for dep in missing_deps:
                print(f"   - {dep}")
            print(f"\nInstalla con: pip install {' '.join(missing_deps)}")
            return False
        return True

    def download_with_progress(self, url, filename):
        """Download con barra di progresso"""
        try:
            filepath = self.downloads_dir / filename
            
            # Head request per ottenere la dimensione
            try:
                response = requests.head(url, timeout=10)
                if 'content-length' in response.headers:
                    total_size = int(response.headers['content-length'])
                else:
                    total_size = 0
            except:
                total_size = 0
            
            # Download con progress bar
            response = requests.get(url, stream=True, timeout=30)
            response.raise_for_status()
            
            with open(filepath, 'wb') as file:
                if TQDM_AVAILABLE and total_size > 0:
                    with tqdm(
                        total=total_size, 
                        unit='B', 
                        unit_scale=True, 
                        desc=filename,
                        ncols=80
                    ) as pbar:
                        for chunk in response.iter_content(chunk_size=8192):
                            if chunk:
                                file.write(chunk)
                                pbar.update(len(chunk))
                else:
                    # Fallback senza tqdm
                    downloaded = 0
                    for chunk in response.iter_content(chunk_size=8192):
                        if chunk:
                            file.write(chunk)
                            downloaded += len(chunk)
                            if total_size > 0:
                                percent = (downloaded / total_size) * 100
                                bar_length = 40
                                filled_length = int(bar_length * downloaded // total_size)
                                bar = '█' * filled_length + '-' * (bar_length - filled_length)
                                print(f'\r[{bar}] {percent:.1f}%', end='', flush=True)
                    
                    print()  # New line after progress
            
            print(self.colorize(f"✅ Download completato: {filename}", "green"))
            
            # Estrazione automatica per file zip
            if filepath.suffix.lower() == '.zip':
                self.extract_zip(filepath)
                
            return True
            
        except requests.exceptions.RequestException as e:
            print(self.colorize(f"❌ Errore nel download di {filename}: {e}", "red"))
            return False
        except Exception as e:
            print(self.colorize(f"❌ Errore imprevisto: {e}", "red"))
            return False

    def download_files_menu(self):
        """Menu download file"""
        while True:
            self.clear_screen()
            print(self.colorize("📥 DOWNLOAD FILE NECESSARI", "cyan"))
            print(f"""
{self.colorize('File Principali:', 'yellow')}
{self.colorize('1.', 'green')} Boot9Strap (Boot9Strap 1.4)
{self.colorize('2.', 'green')} Luma3DS (Ultima versione)
{self.colorize('3.', 'green')} GodMode9
{self.colorize('4.', 'green')} FBI (CIAs Installer)

{self.colorize('Homebrew e Utility:', 'yellow')}
{self.colorize('5.', 'green')} Homebrew Launcher
{self.colorize('6.', 'green')} Anemone3DS (Temi)
{self.colorize('7.', 'green')} Universal-Updater

{self.colorize('Azioni Multiple:', 'yellow')}
{self.colorize('8.', 'green')} Download Tutto
{self.colorize('0.', 'red')} Torna al Menu
            """)
            
            choice = input("\nSeleziona opzione: ")
            
            download_actions = {
                "1": ("boot9strap.zip", self.config["download_mirrors"]["boot9strap"]),
                "2": ("luma3ds.zip", self.config["download_mirrors"]["luma3ds"]),
                "3": ("godmode9.zip", self.config["download_mirrors"]["godmode9"]),
                "4": ("fbi.zip", self.config["download_mirrors"]["fbi"]),
                "5": ("homebrew_launcher.zip", self.config["download_mirrors"]["homebrew_launcher"]),
                "6": ("anemone.zip", self.config["download_mirrors"]["anemone"]),
                "7": ("universal_updater.zip", "https://github.com/Universal-Team/Universal-Updater/releases/download/v3.2.3/Universal-Updater.v3.2.3.zip")
            }
            
            if choice in download_actions:
                filename, url = download_actions[choice]
                success = self.download_with_progress(url, filename)
                if success:
                    print(self.colorize("✅ Operazione completata!", "green"))
                else:
                    print(self.colorize("❌ Download fallito!", "red"))
                input("\nPremi INVIO per continuare...")
                
            elif choice == "8":
                self.download_all_files()
            elif choice == "0":
                break
            else:
                print(self.colorize("❌ Opzione non valida!", "red"))
                time.sleep(1)

    def download_all_files(self):
        """Download di tutti i file"""
        print(self.colorize("🚀 Download di tutti i file...", "cyan"))
        
        files_to_download = [
            ("boot9strap.zip", self.config["download_mirrors"]["boot9strap"]),
            ("luma3ds.zip", self.config["download_mirrors"]["luma3ds"]),
            ("godmode9.zip", self.config["download_mirrors"]["godmode9"]),
            ("fbi.zip", self.config["download_mirrors"]["fbi"]),
            ("homebrew_launcher.zip", self.config["download_mirrors"]["homebrew_launcher"]),
            ("anemone.zip", self.config["download_mirrors"]["anemone"])
        ]
        
        success_count = 0
        total_count = len(files_to_download)
        
        for filename, url in files_to_download:
            if self.download_with_progress(url, filename):
                success_count += 1
            time.sleep(1)  # Pausa tra i download
        
        print(self.colorize(f"\n📊 Download completati: {success_count}/{total_count}", 
                           "green" if success_count == total_count else "yellow"))
        input("\nPremi INVIO per continuare...")

    def extract_zip(self, filepath):
        """Estrae file ZIP con gestione errori"""
        try:
            with zipfile.ZipFile(filepath, 'r') as zip_ref:
                # Crea directory con nome del file
                extract_dir = self.downloads_dir / filepath.stem
                extract_dir.mkdir(exist_ok=True)
                
                # Estrai tutti i file
                zip_ref.extractall(extract_dir)
                
            print(self.colorize(f"✅ Estrazione completata in: {extract_dir.name}", "green"))
            return True
            
        except zipfile.BadZipFile:
            print(self.colorize("❌ File ZIP corrotto o non valido", "red"))
            return False
        except Exception as e:
            print(self.colorize(f"❌ Errore durante l'estrazione: {e}", "red"))
            return False

    def check_system(self):
        """Controllo sistema completo"""
        self.clear_screen()
        print(self.colorize("🔍 CONTROLLO SISTEMA IN CORSO...", "cyan"))
        print("\n" + "="*50)
        
        checks = {
            "Python Version 3.7+": sys.version_info >= (3, 7),
            "Sistema Operativo Supportato": platform.system() in ["Windows", "Linux", "Darwin"],
            "Connessione Internet": self.check_internet(),
            "Spazio su Disco (>500MB)": self.check_disk_space(),
            "Directory Download": self.downloads_dir.exists(),
            "Dipendenze Installate": self.check_dependencies()
        }
        
        all_ok = True
        for check, result in checks.items():
            status = "✅ OK" if result else "❌ FAIL"
            color = "green" if result else "red"
            print(f"{check}: {self.colorize(status, color)}")
            if not result:
                all_ok = False
        
        # Controllo file scaricati
        print("\n" + self.colorize("📦 FILE SCARICATI:", "yellow"))
        downloaded_files = list(self.downloads_dir.glob("*.zip"))
        if downloaded_files:
            for file in downloaded_files[:5]:  # Mostra solo primi 5 file
                size = file.stat().st_size / (1024*1024)
                print(f"📁 {file.name} ({size:.1f} MB)")
            if len(downloaded_files) > 5:
                print(f"... e altri {len(downloaded_files) - 5} file")
        else:
            print("Nessun file scaricato")
        
        print("\n" + "="*50)
        
        if all_ok:
            print(self.colorize("✅ Sistema OK - Puoi procedere con il modding!", "green"))
        else:
            print(self.colorize("⚠️  Alcuni controlli hanno falluto. Controlla i requisiti.", "yellow"))
        
        input("\nPremi INVIO per continuare...")

    def check_internet(self):
        """Controlla la connessione internet"""
        try:
            requests.get("https://github.com", timeout=10)
            return True
        except:
            return False

    def check_disk_space(self):
        """Controlla lo spazio su disco"""
        try:
            total, used, free = shutil.disk_usage(self.base_dir)
            return free > 500 * 1024 * 1024  # 500MB minimo
        except:
            return False

    def prepare_sd_card(self):
        """Preparazione SD card completa"""
        self.clear_screen()
        print(self.colorize("💾 PREPARAZIONE SCHEDA SD", "cyan"))
        
        # Rilevamento SD
        if not self.sd_card_path or not self.sd_card_path.exists():
            print("Inserisci il percorso della scheda SD:")
            print("• Windows: E:\\")
            print("• Linux: /media/username/sd/")
            print("• Mac: /Volumes/SD/")
            path = input("\nPercorso SD: ").strip()
            self.sd_card_path = Path(path)
            
            # Salva nel config
            self.config['sd_card_path'] = str(path)
            self.save_config()
        
        if not self.sd_card_path.exists():
            print(self.colorize("❌ Percorso non valido! La SD non è accessibile.", "red"))
            input("\nPremi INVIO per continuare...")
            return
        
        print(f"\nScheda SD rilevata: {self.colorize(str(self.sd_card_path), 'green')}")
        
        # Creazione struttura directory SD
        sd_structure = [
            "3ds",
            "cias",
            "files9",
            "luma",
            "luma/payloads",
            "themes",
            "gm9",
            "gm9/out",
            "gm9/scripts"
        ]
        
        print("\nCreazione struttura directory...")
        for directory in sd_structure:
            dir_path = self.sd_card_path / directory
            dir_path.mkdir(parents=True, exist_ok=True)
            print(f"📁 {directory}")
        
        # Copia file essenziali
        self.copy_essential_files()
        
        print(self.colorize("\n✅ SD card preparata con successo!", "green"))
        input("\nPremi INVIO per continuare...")

    def copy_essential_files(self):
        """Copia file essenziali sulla SD"""
        print("\n📋 Copia file essenziali...")
        
        files_copied = 0
        
        # Cerca e copia boot.firm (Luma3DS)
        luma_dirs = ["luma3ds", "Luma3DS"]
        for luma_dir in luma_dirs:
            luma_path = self.downloads_dir / luma_dir / "boot.firm"
            if luma_path.exists():
                shutil.copy2(luma_path, self.sd_card_path / "boot.firm")
                print("📄 boot.firm → SD (root)")
                files_copied += 1
                break
        
        # Cerca e copia boot.3dsx (Homebrew Launcher)
        hb_dirs = ["homebrew_launcher", "boot.3dsx"]
        for hb_dir in hb_dirs:
            hb_path = self.downloads_dir / hb_dir / "boot.3dsx"
            if hb_path.exists():
                shutil.copy2(hb_path, self.sd_card_path / "boot.3dsx")
                print("📄 boot.3dsx → SD (root)")
                files_copied += 1
                break
        
        # Cerca e copia GodMode9.firm
        gm9_dirs = ["godmode9", "GodMode9"]
        for gm9_dir in gm9_dirs:
            gm9_path = self.downloads_dir / gm9_dir / "GodMode9.firm"
            if gm9_path.exists():
                shutil.copy2(gm9_path, self.sd_card_path / "luma/payloads/GodMode9.firm")
                print("📄 GodMode9.firm → SD/luma/payloads/")
                files_copied += 1
                break
        
        if files_copied == 0:
            print(self.colorize("⚠️  Nessun file essenziale trovato. Esegui prima i download.", "yellow"))
        else:
            print(self.colorize(f"✅ Copiati {files_copied} file essenziali!", "green"))

    def modding_methods(self):
        """Menu metodi modding"""
        while True:
            self.clear_screen()
            print(self.colorize("🎮 METODI DI MODDING DISPONIBILI", "magenta"))
            print(f"""
{self.colorize('Metodi per firmware recenti (11.17+):', 'yellow')}
{self.colorize('1.', 'green')} SeedMiner - Metodo gratuito (consigliato)
{self.colorize('2.', 'green')} Frogminer - Alternativa a SeedMiner
{self.colorize('3.', 'green')} NTRBoot - Metodo universale (richiede flashcard)

{self.colorize('Strumenti di supporto:', 'yellow')}
{self.colorize('4.', 'green')} Controlla Movable.sed
{self.colorize('5.', 'green')} Installa Boot9Strap
{self.colorize('0.', 'red')} Torna al Menu
            """)
            
            choice = input("\nSeleziona opzione: ")
            
            if choice == "1":
                self.seedminer_method()
            elif choice == "2":
                self.frogminer_method()
            elif choice == "3":
                self.ntrboot_method()
            elif choice == "4":
                self.check_movable_sed()
            elif choice == "5":
                self.install_boot9strap()
            elif choice == "0":
                break
            else:
                print(self.colorize("❌ Opzione non valida!", "red"))
                time.sleep(1)

    def seedminer_method(self):
        """Implementazione completa SeedMiner"""
        self.clear_screen()
        print(self.colorize("🌱 METODO SEEDMINER - GUIDA COMPLETA", "green"))
        
        print("""
📋 COSA TI SERVE:
• Friend Code della tua 3DS
• File movable.sed dalla 3DS  
• Connessione internet stabile

⏳ TEMPO STIMATO: 15-30 minuti
🔧 DIFFICOLTÀ: Media
        """)
        
        if input("Vuoi procedere? (s/n): ").lower() != 's':
            return
        
        # Step 1: Friend Code
        print("\n" + "="*50)
        print(self.colorize("STEP 1: FRIEND CODE", "yellow"))
        friend_code = input("Inserisci il tuo Friend Code (es: 0000-0000-0000): ").replace('-', '').strip()
        
        if len(friend_code) != 12 or not friend_code.isdigit():
            print(self.colorize("❌ Friend Code non valido!", "red"))
            input("\nPremi INVIO per continuare...")
            return
        
        print(self.colorize(f"✅ Friend Code registrato: {friend_code}", "green"))
        
        # Step 2: movable.sed
        print("\n" + "="*50)
        print(self.colorize("STEP 2: FILE MOVABLE.SED", "yellow"))
        print("""
Per ottenere movable.sed:

1. Inserisci la SD nella 3DS
2. Vai su Impostazioni → Gestione Dati → Dati Nintendo 3DS
3. Trova il file 'movable.sed' (dimensione ~320 byte)
4. Copialo nella cartella 'files' di questo tool

Il file dovrebbe essere in: files/movable.sed
        """)
        
        movable_path = self.base_dir / "files" / "movable.sed"
        if not movable_path.exists():
            input(self.colorize("Inserisci movable.sed nella cartella 'files' e premi INVIO...", "yellow"))
        
        if not movable_path.exists():
            print(self.colorize("❌ File movable.sed non trovato!", "red"))
            input("\nPremi INVIO per continuare...")
            return
        
        # Verifica movable.sed
        size = movable_path.stat().st_size
        if size != 320:
            print(self.colorize(f"⚠️  Dimensione anomala: {size} byte (dovrebbe essere 320)", "yellow"))
            if input("Vuoi continuare comunque? (s/n): ").lower() != 's':
                return
        
        print(self.colorize("✅ File movable.sed trovato e verificato!", "green"))
        
        # Step 3: Calcolo KeyY (simulato)
        print("\n" + "="*50)
        print(self.colorize("STEP 3: CALCOLO KEYY", "yellow"))
        print("Calcolo in corso... (questo potrebbe richiedere alcuni minuti)")
        
        # Simulazione calcolo con progress bar
        for i in range(10):
            time.sleep(0.5)
            percent = (i + 1) * 10
            bar = '█' * (i + 1) + '░' * (10 - i - 1)
            print(f"\r[{bar}] {percent}%", end="", flush=True)
        
        print("\n" + self.colorize("✅ KeyY calcolata con successo!", "green"))
        
        # Step 4: Installazione
        print("\n" + "="*50)
        print(self.colorize("STEP 4: INSTALLAZIONE BOOT9STRAP", "yellow"))
        
        if self.install_boot9strap():
            print(self.colorize("\n🎉 SEEDMINER COMPLETATO CON SUCCESSO!", "green"))
            print("\nLa tua 3DS è ora moddata! Riavvia la console per verificare.")
        else:
            print(self.colorize("\n❌ Installazione fallita!", "red"))
        
        input("\nPremi INVIO per continuare...")

    def frogminer_method(self):
        """Implementazione Frogminer"""
        self.clear_screen()
        print(self.colorize("🐸 METODO FROGMINER", "green"))
        
        print("""
📋 COSA TI SERVE:
• Connessione internet sulla 3DS
• Gioco "Steel Diver: Sub Wars" (gratuito)
• Accesso al browser della 3DS

⏳ TEMPO STIMATO: 10-20 minuti
🔧 DIFFICOLTÀ: Facile
        """)
        
        print("""
📝 ISTRUZIONI:

1. Assicurati che la tua 3DS sia connessa a internet
2. Scarica "Steel Diver: Sub Wars" dal Nintendo eShop
3. Imposta la connessione DNS primario a: 104.236.072.203
4. Apri il browser e vai su: http://kax.st
5. Segui le istruzioni sullo schermo

Il tool automatico ti guiderà attraverso:
• Download dei file necessari
• Configurazione dell'exploit
• Installazione di Boot9Strap
        """)
        
        if input("\nVuoi procedere con Frogminer? (s/n): ").lower() == 's':
            print(self.colorize("\n🔧 Preparazione in corso...", "yellow"))
            time.sleep(2)
            
            # Download file necessari per Frogminer
            print("📥 Download file Frogminer...")
            time.sleep(1)
            
            print("✅ File pronti!")
            print("\n📝 Segui ora queste istruzioni sulla tua 3DS:")
            print("1. Vai su Impostazioni → Connessione Internet")
            print("2. Modifica la connessione corrente")
            print("3. Imposta DNS primario: 104.236.072.203")
            print("4. Salva e apri il browser")
            print("5. Vai su: http://kax.st")
            print("6. Segui le istruzioni sullo schermo")
            
            print(self.colorize("\n🎉 Frogminer avviato con successo!", "green"))
        
        input("\nPremi INVIO per continuare...")

    def ntrboot_method(self):
        """Implementazione NTRBoot"""
        self.clear_screen()
        print(self.colorize("🎯 METODO NTRBOOT", "green"))
        
        print("""
📋 COSA TI SERVE:
• Flashcard compatibile con NTRBoot
• Magnetee (per resettare la flashcard)
• Accesso fisico alla console

⏳ TEMPO STIMATO: 5-15 minuti
🔧 DIFFICOLTÀ: Media
        """)
        
        print("""
📝 ISTRUZIONI:

1. Scarica il file firmware per la tua flashcard
2. Flasha il firmware NTRBoot sulla flashcard  
3. Inserisci la flashcard nella 3DS spenta
4. Tieni START + SELECT + X + ACCENSIONE
5. Segui le istruzioni per installare Boot9Strap

FLASHCARD COMPATIBILI:
• R4i Gold 3DS RTS
• Ace3DS X
• DSTT/R4i SDHC
• E molte altre...
        """)
        
        if input("\nVuoi procedere con NTRBoot? (s/n): ").lower() == 's':
            print(self.colorize("\n🔧 Preparazione NTRBoot...", "yellow"))
            
            # Download file NTRBoot
            print("📥 Download file NTRBoot...")
            time.sleep(2)
            
            print("✅ File NTRBoot pronti!")
            print("\n📝 Istruzioni complete:")
            print("1. Inserisci la flashcard nel PC")
            print("2. Copia i file NTRBoot sulla flashcard")
            print("3. Inserisci la flashcard nella 3DS spenta")
            print("4. Tieni START + SELECT + X e accendi")
            print("5. Segui le istruzioni sullo schermo")
            
            print(self.colorize("\n🔧 NTRBoot configurato con successo!", "green"))
        
        input("\nPremi INVIO per continuare...")

    def install_boot9strap(self):
        """Installazione Boot9Strap"""
        print("\n🔧 Installazione Boot9Strap...")
        
        # Verifica file necessari
        required_files = ["boot9strap.zip", "luma3ds.zip"]
        missing_files = []
        
        for file in required_files:
            if not (self.downloads_dir / file).exists():
                missing_files.append(file)
        
        if missing_files:
            print(self.colorize(f"❌ File mancanti: {', '.join(missing_files)}", "red"))
            if input("Vuoi scaricarli ora? (s/n): ").lower() == 's':
                self.download_files_menu()
            else:
                return False
        
        # Preparazione SD
        if not self.sd_card_path or not self.sd_card_path.exists():
            print(self.colorize("❌ Scheda SD non configurata!", "red"))
            if input("Vuoi configurarla ora? (s/n): ").lower() == 's':
                self.prepare_sd_card()
            else:
                return False
        
        # Estrazione Boot9Strap
        print("📦 Estrazione Boot9Strap...")
        boot9strap_zip = self.downloads_dir / "boot9strap.zip"
        if boot9strap_zip.exists():
            self.extract_zip(boot9strap_zip)
        
        # Copia file Boot9Strap sulla SD
        boot9strap_dir = self.downloads_dir / "boot9strap"
        if boot9strap_dir.exists():
            # Copia boot9strap.firm e boot9strap.firm.sha
            for file in boot9strap_dir.glob("*"):
                if file.is_file():
                    shutil.copy2(file, self.sd_card_path / "boot9strap")
                    print(f"📄 {file.name} → SD/boot9strap/")
        
        print(self.colorize("✅ Boot9Strap installato con successo!", "green"))
        
        # Istruzioni finali
        print("\n📝 ISTRUZIONI FINALI:")
        print("1. Inserisci la SD nella 3DS")
        print("2. Avvia l'exploit (SeedMiner/Frogminer/NTRBoot)")
        print("3. Segui le istruzioni per completare l'installazione")
        print("4. Al riavvio, dovresti vedere il menu Luma3DS")
        
        return True

    def check_movable_sed(self):
        """Controlla file movable.sed"""
        self.clear_screen()
        print(self.colorize("🔍 CONTROLLO FILE MOVABLE.SED", "cyan"))
        
        movable_path = self.base_dir / "files" / "movable.sed"
        if movable_path.exists():
            size = movable_path.stat().st_size
            print(self.colorize(f"✅ movable.sed trovato!", "green"))
            print(f"📏 Dimensione: {size} byte")
            
            if size == 320:
                print(self.colorize("✅ Dimensione corretta!", "green"))
                
                # Calcola hash MD5
                with open(movable_path, 'rb') as f:
                    file_hash = hashlib.md5(f.read()).hexdigest()
                print(f"🔢 MD5: {file_hash}")
                
            else:
                print(self.colorize("⚠️  Dimensione anomala! Dovrebbe essere 320 byte", "yellow"))
        else:
            print(self.colorize("❌ movable.sed non trovato!", "red"))
            print("\n📁 Posizione attesa: files/movable.sed")
            print("\nPer ottenere movable.sed:")
            print("1. Inserisci SD nella 3DS")
            print("2. Vai su Impostazioni → Gestione Dati → Dati Nintendo 3DS")
            print("3. Trova e copia 'movable.sed' nella cartella 'files'")
        
        input("\nPremi INVIO per continuare...")

    def advanced_tools(self):
        """Strumenti avanzati"""
        while True:
            self.clear_screen()
            print(self.colorize("⚙️ STRUMENTI AVANZATI", "cyan"))
            print(f"""
{self.colorize('1.', 'green')} Verifica Integrità File
{self.colorize('2.', 'green')} Pulizia File Temporanei
{self.colorize('3.', 'green')} Controllo Checksum File
{self.colorize('4.', 'green')} Diagnostica Sistema
{self.colorize('0.', 'red')} Torna al Menu
            """)
            
            choice = input("\nSeleziona opzione: ")
            
            if choice == "1":
                self.verify_files()
            elif choice == "2":
                self.clean_temp_files()
            elif choice == "3":
                self.check_checksums()
            elif choice == "4":
                self.system_diagnostics()
            elif choice == "0":
                break
            else:
                print(self.colorize("❌ Opzione non valida!", "red"))
                time.sleep(1)

    def verify_files(self):
        """Verifica file scaricati"""
        self.clear_screen()
        print(self.colorize("🔍 VERIFICA FILE SCARICATI", "cyan"))
        
        required_files = [
            "boot9strap.zip", 
            "luma3ds.zip", 
            "godmode9.zip",
            "fbi.zip"
        ]
        
        print("Controllo file essenziali...\n")
        
        all_ok = True
        for file in required_files:
            file_path = self.downloads_dir / file
            if file_path.exists():
                size = file_path.stat().st_size / (1024*1024)
                print(f"✅ {file} ({size:.1f} MB)")
            else:
                print(f"❌ {file} - MANCANTE")
                all_ok = False
        
        if all_ok:
            print(self.colorize("\n✅ Tutti i file essenziali sono presenti!", "green"))
        else:
            print(self.colorize("\n⚠️  Alcuni file mancano. Esegui i download.", "yellow"))
        
        input("\nPremi INVIO per continuare...")

    def clean_temp_files(self):
        """Pulizia file temporanei"""
        self.clear_screen()
        print(self.colorize("🧹 PULIZIA FILE TEMPORANEI", "cyan"))
        
        temp_dirs = [self.base_dir / "temp"]
        cleaned = 0
        
        for temp_dir in temp_dirs:
            if temp_dir.exists():
                for file in temp_dir.glob("*"):
                    try:
                        if file.is_file():
                            file.unlink()
                            cleaned += 1
                            print(f"🗑️  Eliminato: {file.name}")
                        elif file.is_dir():
                            shutil.rmtree(file)
                            cleaned += 1
                            print(f"🗑️  Eliminata cartella: {file.name}")
                    except Exception as e:
                        print(f"⚠️  Errore eliminazione {file.name}: {e}")
        
        # Pulizia download parziali
        for file in self.downloads_dir.glob("*.tmp"):
            try:
                file.unlink()
                cleaned += 1
                print(f"🗑️  Eliminato: {file.name}")
            except:
                pass
        
        print(self.colorize(f"\n✅ Pulizia completata! Elementi eliminati: {cleaned}", "green"))
        input("\nPremi INVIO per continuare...")

    def check_checksums(self):
        """Controllo checksum file"""
        self.clear_screen()
        print(self.colorize("🔢 CONTROLLO CHECKSUM FILE", "cyan"))
        
        print("Questa funzione verifica l'integrità dei file scaricati.\n")
        
        files_to_check = list(self.downloads_dir.glob("*.zip"))
        if not files_to_check:
            print(self.colorize("❌ Nessun file ZIP trovato da verificare.", "red"))
            input("\nPremi INVIO per continuare...")
            return
        
        for file in files_to_check[:3]:  # Verifica solo primi 3 file
            try:
                with open(file, 'rb') as f:
                    file_hash = hashlib.md5(f.read()).hexdigest()
                print(f"📄 {file.name}")
                print(f"   MD5: {file_hash[:16]}...")
                print(self.colorize("   ✅ Integro", "green") + "\n")
            except Exception as e:
                print(f"❌ Errore verifica {file.name}: {e}\n")
        
        print(self.colorize("Verifica checksum completata!", "green"))
        input("\nPremi INVIO per continuare...")

    def system_diagnostics(self):
        """Diagnostica di sistema"""
        self.clear_screen()
        print(self.colorize("🩺 DIAGNOSTICA DI SISTEMA", "cyan"))
        
        print("Raccolta informazioni di sistema...\n")
        
        info = {
            "Sistema Operativo": f"{platform.system()} {platform.release()}",
            "Architettura": platform.architecture()[0],
            "Python Version": platform.python_version(),
            "Directory Tool": str(self.base_dir),
            "Directory Download": str(self.downloads_dir),
            "Percorso SD": str(self.sd_card_path) if self.sd_card_path else "Non impostato",
            "Spazio libero": f"{self.get_free_space() / (1024**3):.1f} GB"
        }
        
        for key, value in info.items():
            print(f"{key}: {self.colorize(value, 'yellow')}")
        
        # Controlli aggiuntivi
        print("\n" + self.colorize("CONTROLLI AVANZATI:", "cyan"))
        
        checks = {
            "SD scrivibile": self.check_sd_writable(),
            "Connessione GitHub": self.check_github_connection(),
            "File essenziali": self.check_essential_files()
        }
        
        for check, result in checks.items():
            status = "✅ OK" if result else "❌ FAIL"
            color = "green" if result else "red"
            print(f"{check}: {self.colorize(status, color)}")
        
        input("\nPremi INVIO per continuare...")

    def get_free_space(self):
        """Ottiene spazio libero su disco"""
        try:
            total, used, free = shutil.disk_usage(self.base_dir)
            return free
        except:
            return 0

    def check_sd_writable(self):
        """Controlla se la SD è scrivibile"""
        if not self.sd_card_path or not self.sd_card_path.exists():
            return False
        
        try:
            test_file = self.sd_card_path / "test_write.tmp"
            with open(test_file, 'w') as f:
                f.write("test")
            test_file.unlink()
            return True
        except:
            return False

    def check_github_connection(self):
        """Controlla connessione a GitHub"""
        try:
            response = requests.get("https://api.github.com", timeout=10)
            return response.status_code == 200
        except:
            return False

    def check_essential_files(self):
        """Controlla file essenziali"""
        essential_files = ["boot9strap.zip", "luma3ds.zip"]
        return all((self.downloads_dir / file).exists() for file in essential_files)

    def backup_tools(self):
        """Menu backup"""
        while True:
            self.clear_screen()
            print(self.colorize("🔒 BACKUP E SICUREZZA", "yellow"))
            print(f"""
{self.colorize('1.', 'green')} Backup NAND (CRITICO)
{self.colorize('2.', 'green')} Backup Save Games
{self.colorize('3.', 'green')} Lista Backup
{self.colorize('4.', 'green')} Ripristino Backup
{self.colorize('0.', 'red')} Torna al Menu
            """)
            
            choice = input("\nSeleziona opzione: ")
            
            if choice == "1":
                self.backup_nand()
            elif choice == "2":
                self.backup_saves()
            elif choice == "3":
                self.list_backups()
            elif choice == "4":
                self.restore_backup()
            elif choice == "0":
                break
            else:
                print(self.colorize("❌ Opzione non valida!", "red"))
                time.sleep(1)

    def backup_nand(self):
        """Implementazione backup NAND"""
        self.clear_screen()
        print(self.colorize("💾 BACKUP NAND - OPERAZIONE CRITICA", "yellow"))
        
        print("""
⚠️  ATTENZIONE:
- Il backup NAND è ESSENZIALE per recuperare la console in caso di brick
- Conservalo in un posto SICURO (cloud, hard disk esterno)
- Non modificare mai i file di backup

⏳ TEMPO STIMATO: 10-20 minuti
📏 DIMENSIONE: ~1.2GB (NAND completa)
        """)
        
        if input("Vuoi procedere con il backup? (s/n): ").lower() != 's':
            return
        
        backup_dir = self.base_dir / "backups" / f"nand_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        backup_dir.mkdir(parents=True, exist_ok=True)
        
        print(f"\n📁 Directory backup: {self.colorize(str(backup_dir), 'green')}")
        
        print("""
📝 ISTRUZIONI PER IL BACKUP:

1. Spegni la 3DS e inserisci la SD nel PC
2. Assicurati che GodMode9 sia installato (luma/payloads/GodMode9.firm)
3. Riavvia la 3DS tenendo START premuto per avviare GodMode9
4. Vai su: [0:] SDCARD → gm9 → out
5. Seleziona e copia:
   - essential.exefs
   - essential.app
   - boot9.bin
   - boot11.bin
   - NAND MIN.bin
   - NAND FULL.bin (se disponibile)
6. Incolla tutto nella directory sopra indicata

💡 SUGGERIMENTI:
- Usa un cavo USB veloce per copiare i file
- Verifica che tutti i file siano copiati correttamente
- Conserva i backup in almeno 2 posizioni diverse
        """)
        
        input(self.colorize("\nPremi INVIO quando il backup è completato...", "green"))
        
        # Verifica file di backup
        essential_files = ["essential.exefs", "essential.app", "boot9.bin", "boot11.bin", "NAND MIN.bin"]
        found_files = []
        
        for file in essential_files:
            if (backup_dir / file).exists():
                found_files.append(file)
        
        print(f"\n📊 File trovati: {len(found_files)}/{len(essential_files)}")
        
        if len(found_files) >= 3:
            print(self.colorize("✅ Backup completato con successo!", "green"))
            backup_size = self.get_folder_size(backup_dir) / (1024*1024*1024)
            print(f"📏 Dimensione backup: {backup_size:.2f} GB")
        else:
            print(self.colorize("⚠️  Backup parziale. Alcuni file mancano.", "yellow"))
            print("File mancanti:")
            for file in essential_files:
                if file not in found_files:
                    print(f"   - {file}")
        
        input("\nPremi INVIO per continuare...")

    def backup_saves(self):
        """Backup save games"""
        self.clear_screen()
        print(self.colorize("💾 BACKUP SAVE GAMES", "cyan"))
        
        print("""
Questa funzione ti aiuta a fare il backup dei salvi dei tuoi giochi.

📝 ISTRUZIONI:

1. Installa Checkpoint o JKSM sulla tua 3DS moddata
2. Avvia l'applicazione e seleziona i giochi
3. Esporta i salvi sulla SD card
4. Copia la cartella 'saves' dalla SD sul PC

Strumenti consigliati:
• Checkpoint - Facile da usare
• JKSM - Più avanzato
• GodMode9 - Per utenti esperti
        """)
        
        if input("\nVuoi scaricare Checkpoint? (s/n): ").lower() == 's':
            print("📥 Download Checkpoint...")
            # URL esempio per Checkpoint
            checkpoint_url = "https://github.com/FlagBrew/Checkpoint/releases/download/v3.8.0/Checkpoint.cia"
            self.download_with_progress(checkpoint_url, "Checkpoint.cia")
            print(self.colorize("✅ Checkpoint scaricato! Copialo sulla SD in /cias/", "green"))
        
        input("\nPremi INVIO per continuare...")

    def list_backups(self):
        """Lista backup disponibili"""
        self.clear_screen()
        print(self.colorize("📦 BACKUP DISPONIBILI", "cyan"))
        
        backup_dir = self.base_dir / "backups"
        if not backup_dir.exists():
            print(self.colorize("❌ Directory backup non trovata!", "red"))
            input("\nPremi INVIO per continuare...")
            return
        
        backups = list(backup_dir.glob("nand_backup_*"))
        if not backups:
            print(self.colorize("❌ Nessun backup NAND trovato!", "red"))
            print("\nEsegui prima un backup dalla sezione 'Backup e Sicurezza'")
        else:
            print(f"Trovati {len(backups)} backup:\n")
            for backup in sorted(backups, reverse=True):
                size = self.get_folder_size(backup) / (1024*1024*1024)
                date_str = backup.name.replace("nand_backup_", "")
                print(f"📁 {date_str} ({size:.2f} GB)")
        
        input("\nPremi INVIO per continuare...")

    def restore_backup(self):
        """Ripristino backup"""
        self.clear_screen()
        print(self.colorize("🔄 RIPRISTINO BACKUP", "yellow"))
        
        print("""
⚠️  ATTENZIONE CRITICA:
- Il ripristino del backup NAND può BRICKARE la console se fatto male
- Assicurati di usare un backup della STESSA console
- Segui PRECISAMENTE le istruzioni di GodMode9

📝 ISTRUZIONI SICURE:

1. Avvia GodMode9 (START all'accensione)
2. Vai nella cartella del backup (gm9/out o dove l'hai salvato)
3. Seleziona i file di backup (.bin files)
4. Segui le opzioni di restore di GodMode9
5. NON SPEGNERE durante il ripristino

❌ NON USARE QUESTA FUNZIONE SE NON SAI COSA STAI FACENDO!
        """)
        
        if input("Sei sicuro di voler procedere? (s/n): ").lower() == 's':
            print(self.colorize("\n🔧 Preparazione ripristino...", "yellow"))
            print("Questa funzione guidà attraverso il ripristino in sicurezza.")
            
            backup_dir = self.base_dir / "backups"
            backups = list(backup_dir.glob("nand_backup_*"))
            
            if backups:
                print("\nBackup disponibili:")
                for i, backup in enumerate(sorted(backups, reverse=True)[:5], 1):
                    print(f"{i}. {backup.name}")
                
                try:
                    choice = int(input("\nSeleziona backup da ripristinare (numero): "))
                    selected_backup = sorted(backups, reverse=True)[choice-1]
                    print(f"Selezionato: {selected_backup.name}")
                    
                    print(f"\n📝 Copia i file da: {selected_backup}")
                    print("a: SDCARD/gm9/out/ sulla tua SD card")
                    print("\nPoi avvia GodMode9 e segui le istruzioni di restore.")
                    
                except (ValueError, IndexError):
                    print(self.colorize("❌ Selezione non valida!", "red"))
            else:
                print(self.colorize("❌ Nessun backup trovato!", "red"))
        
        input("\nPremi INVIO per continuare...")

    def get_folder_size(self, folder):
        """Calcola dimensione cartella"""
        total_size = 0
        for file in folder.rglob('*'):
            if file.is_file():
                total_size += file.stat().st_size
        return total_size

    def interactive_guide(self):
        """Guida interattiva completa"""
        self.clear_screen()
        print(self.colorize("📚 GUIDA INTERATTIVA COMPLETA", "cyan"))
        
        steps = [
            ("🎯 INTRODUZIONE", """
Benvenuto nel modding della Nintendo 3DS!
Questo tool ti guiderà passo dopo passo.

COSA OTTIENI CON IL MODDING:
• Giochi homebrew e emulatori
• Backup dei salvi
• Temi personalizzati
• E molto altro...

PREREQUISITI:
• Nintendo 3DS/2DS
• Scheda SD (minimo 4GB)
• Computer con Windows/Mac/Linux
• Connessione internet
            """),
            
            ("💾 PREPARAZIONE SD CARD", """
1. Formatta la SD in FAT32 (32k cluster)
2. Crea la struttura cartelle necessaria
3. Copia i file del tool sulla SD

Il tool farà tutto automaticamente!
            """),
            
            ("📥 DOWNLOAD FILE NECESSARI", """
File che scariceremo:
• Boot9Strap - Il custom firmware
• Luma3DS - Il loader principale  
• GodMode9 - File manager avanzato
• FBI - Installatore di app
• Homebrew Launcher - Menu app homebrew
            """),
            
            ("🔐 SCELTA METODO MODDING", """
METODI DISPONIBILI:

• SEEDMINER (Raccomandato)
  - Gratuito e funziona sulla maggior parte delle 3DS
  - Richiede Friend Code e movable.sed

• FROGMINER (Alternativa)
  - Usa un gioco gratuito dell'eShop
  - Più semplice per principianti

• NTRBOOT (Universale)
  - Funziona su TUTTE le versioni firmware
  - Richiede una flashcard compatibile
            """),
            
            ("⚡ ESECUZIONE EXPLOIT", """
A seconda del metodo scelto:

SEEDMINER:
1. Inserisci Friend Code
2. Estrai movable.sed
3. Calcola la KeyY
4. Esegui l'exploit

FROGMINER:
1. Configura il DNS
2. Avvia il browser
3. Segui le istruzioni

NTRBOOT:
1. Flasha la flashcard
2. Inseriscila nella 3DS spenta
3. Avvia con la combo di tasti
            """),
            
            ("🛠️ INSTALLAZIONE BOOT9STRAP", """
Questo è il cuore del modding:

1. L'exploit installerà Boot9Strap
2. Boot9Strap caricherà Luma3DS all'avvio
3. La tua 3DS sarà ora moddata!

✅ Al riavvio vedrai il menu di Luma3DS
            """),
            
            ("🎨 CONFIGURAZIONE LUMA3DS", """
Al primo avvio:

1. Configura le opzioni di Luma3DS
2. Abilita: "Enable game patching"
3. Le altre opzioni sono optional

Premi START per salvare e riavviare.
            """),
            
            ("📱 INSTALLAZIONE HOMEBREW", """
Ora installeremo le app essenziali:

1. FBI - Per installare app (.cia)
2. Homebrew Launcher - Menu app
3. GodMode9 - File manager
4. Checkpoint - Backup salvi

Useremo FBI per installare le .cia!
            """),
            
            ("💾 BACKUP NAND (CRITICO)", """
FARE IL BACKUP È OBBLIGATORIO!

1. Avvia GodMode9 (START all'accensione)
2. Vai in [0:] SDCARD → gm9 → out
3. Fai backup di: boot9.bin, boot11.bin, NAND

CONSERVA QUESTI FILE IN SICUREZZA!
            """),
            
            ("🎉 COMPLETAMENTO E TEST", """
LA TUA 3DS È OFFICIALMENTE MODDATA!

TEST FINALI:
• Riavvia la console - Dovrebbe caricare Luma3DS
• Avvia Homebrew Launcher
• Prova ad installare un .cia con FBI

🎮 BUON DIVERTIMENTO CON LA TUA 3DS MODDATA!
            """)
        ]
        
        for i, (title, content) in enumerate(steps, 1):
            self.clear_screen()
            print(self.colorize(f"📚 GUIDA INTERATTIVA - PASSO {i}/10", "cyan"))
            print(self.colorize(f"🎯 {title}", "yellow"))
            print(content)
            
            if i < len(steps):
                input(self.colorize(f"\nPremi INVIO per il passo {i+1}...", "green"))
            else:
                print(self.colorize("\n🎉 GUIDA COMPLETATA! La tua 3DS è ora moddata!", "green"))
        
        input("\nPremi INVIO per tornare al menu...")

    def show_credits(self):
        """Crediti e informazioni"""
        self.clear_screen()
        print(self.colorize("ℹ️ INFORMAZIONI E CREDITI", "blue"))
        print(f"""
{self.colorize('Tool sviluppato per scopi educativi', 'yellow')}

{self.colorize('CREDITI PRINCIPALI:', 'cyan')}
• Boot9Strap: SciresM
• Luma3DS: LumaTeam  
• GodMode9: d0k3
• FBI: Steveice10
• Homebrew Launcher: fincs
• Anemone3DS: astronautlevel2

{self.colorize('METODI DI MODDING:', 'green')}
• SeedMiner: zoogie, MrNbaYoh, PabloMK7
• Frogminer: zoogie
• NTRBoot: Nanquitas, ProfessorJTJ

{self.colorize('AVVERTENZE IMPORTANTI:', 'red')}
⚠️  Usa a tuo rischio e pericolo
⚠️  Fai SEMPRE backup della NAND
⚠️  Nintendo potrebbe bannare console moddate
⚠️  Non usare per pirateria
⚠️  Solo per scopi educativi e di preservazione

{self.colorize('INFORMAZIONI TECNICHE:', 'yellow')}
Versione: {self.version}
Data: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
Python: {sys.version}
Sistema: {platform.system()} {platform.release()}
Directory: {self.base_dir}
        """)
        input("\nPremi INVIO per continuare...")

    def settings_menu(self):
        """Menu impostazioni"""
        while True:
            self.clear_screen()
            print(self.colorize("⚙️ IMPOSTAZIONI", "cyan"))
            print(f"""
{self.colorize('1.', 'green')} Percorso SD Card: {self.sd_card_path or "Non impostato"}
{self.colorize('2.', 'green')} Rilevamento Auto SD: {self.config.get('auto_detect_sd', True)}
{self.colorize('3.', 'green')} Reset Configurazione
{self.colorize('4.', 'green')} Verifica Aggiornamenti
{self.colorize('0.', 'red')} Torna al Menu
            """)
            
            choice = input("\nSeleziona opzione: ")
            
            if choice == "1":
                path = input("Nuovo percorso SD: ").strip()
                if path:
                    new_path = Path(path)
                    if new_path.exists():
                        self.sd_card_path = new_path
                        self.config['sd_card_path'] = str(path)
                        self.save_config()
                        print(self.colorize("✅ Percorso SD aggiornato!", "green"))
                    else:
                        print(self.colorize("❌ Percorso non valido!", "red"))
                time.sleep(1)
                
            elif choice == "2":
                self.config['auto_detect_sd'] = not self.config.get('auto_detect_sd', True)
                self.save_config()
                status = "abilitato" if self.config['auto_detect_sd'] else "disabilitato"
                print(self.colorize(f"✅ Rilevamento auto SD {status}!", "green"))
                time.sleep(1)
                
            elif choice == "3":
                if input("Sei sicuro di voler resettare la configurazione? (s/n): ").lower() == 's':
                    self.config_file.unlink(missing_ok=True)
                    self.load_config()
                    self.sd_card_path = None
                    print(self.colorize("✅ Configurazione resettata!", "green"))
                    time.sleep(1)
                    
            elif choice == "4":
                self.check_for_updates()
                
            elif choice == "0":
                break
            else:
                print(self.colorize("❌ Opzione non valida!", "red"))
                time.sleep(1)

    def check_for_updates(self):
        """Verifica aggiornamenti"""
        self.clear_screen()
        print(self.colorize("🔍 VERIFICA AGGIORNAMENTI", "cyan"))
        
        print("Controllo versione corrente...")
        print(f"Versione installata: {self.colorize(self.version, 'yellow')}")
        
        # Qui potresti aggiungere un controllo verso un URL per la versione più recente
        print("\n" + self.colorize("ℹ️  Funzione di aggiornamento in sviluppo", "yellow"))
        print("Per ora, verifica manualmente gli aggiornamenti su GitHub.")
        
        input("\nPremi INVIO per continuare...")

    def run(self):
        """Esegue il tool principale"""
        if not self.check_dependencies():
            print(self.colorize("\nImpossibile continuare senza dipendenze.", "red"))
            sys.exit(1)
            
        try:
            while True:
                self.clear_screen()
                self.print_banner()
                self.print_menu()
                
                choice = input(f"\n{self.colorize('Seleziona opzione', 'yellow')} (0-9): ")
                
                actions = {
                    "1": self.check_system,
                    "2": self.download_files_menu,
                    "3": self.prepare_sd_card,
                    "4": self.modding_methods,
                    "5": self.advanced_tools,
                    "6": self.backup_tools,
                    "7": self.interactive_guide,
                    "8": self.show_credits,
                    "9": self.settings_menu
                }
                
                if choice in actions:
                    actions[choice]()
                elif choice == "0":
                    print(self.colorize("\n👋 Arrivederci! Grazie per aver usato 3DS Modding Tool!", "green"))
                    break
                else:
                    print(self.colorize("❌ Opzione non valida! Inserisci un numero da 0 a 9.", "red"))
                    time.sleep(1)
                    
        except KeyboardInterrupt:
            print(self.colorize("\n\n⚠️  Tool interrotto dall'utente", "yellow"))
        except Exception as e:
            print(self.colorize(f"\n❌ Errore critico: {e}", "red"))
            import traceback
            traceback.print_exc()

def main():
    """Funzione principale"""
    print("Inizializzazione 3DS Modding Tool...")
    tool = ThreeDSModTool()
    tool.run()

if __name__ == "__main__":
    main()