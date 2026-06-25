import os
import sys
import time
import json
import urllib.request
import urllib.parse
import urllib.error
import xml.etree.ElementTree as ET
import textwrap
import webbrowser
from datetime import datetime

def clear_screen():
    """Clears the terminal screen for a clean UI experience."""
    os.system('cls' if os.name == 'nt' else 'clear')

def type_text(text, delay=0.01):
    """Simulates a typewriter effect for terminal output."""
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(delay)
    print()

def pause_execution():
    """Pauses the OS until the user is ready to proceed."""
    input("\n[Press Enter to continue...]")

class LiveCivicClient:
    """Handles all real-world data fetching from live APIs and RSS feeds."""
    def __init__(self):
        self.config_file = 'civic_config.json'
        self.config = self.load_config()

    def load_config(self):
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r') as f:
                    return json.load(f)
            except Exception:
                return {"city": "", "address": "", "api_key": ""}
        return {"city": "", "address": "", "api_key": ""}

    def save_config(self):
        with open(self.config_file, 'w') as f:
            json.dump(self.config, f)

    def fetch_news(self):
        """Fetches live news via Google News RSS for the user's city."""
        city = self.config.get('city', 'United States')
        query = urllib.parse.quote(f"{city} local government OR city council")
        url = f"https://news.google.com/rss/search?q={query}&hl=en-US&gl=US&ceid=US:en"
        
        try:
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req) as response:
                tree = ET.parse(response)
                root = tree.getroot()
                items = root.findall('.//channel/item')
                
                news_list = []
                for item in items[:5]: # Top 5 recent news articles
                    title = item.find('title').text if item.find('title') is not None else 'No Title'
                    pubDate = item.find('pubDate').text if item.find('pubDate') is not None else 'Unknown Date'
                    link = item.find('link').text if item.find('link') is not None else ''
                    news_list.append({"title": title, "date": pubDate, "link": link})
                return news_list
        except Exception as e:
            return f"Error fetching live news: {e}"

    def fetch_representatives(self):
        """Fetches real representatives using the Google Civic Information API."""
        address = self.config.get('address')
        api_key = self.config.get('api_key')
        
        if not address or not api_key:
            return "MISSING_CONFIG"
            
        query = urllib.parse.quote(address)
        url = f"https://www.googleapis.com/civicinfo/v2/representatives?address={query}&key={api_key}"
        
        try:
            req = urllib.request.Request(url)
            with urllib.request.urlopen(req) as response:
                data = json.loads(response.read().decode())
                return self._parse_civic_data(data)
        except urllib.error.HTTPError as e:
            if e.code == 403:
                return "API_KEY_INVALID"
            return f"HTTP Error: {e.code}"
        except Exception as e:
            return f"Error fetching representatives: {e}"

    def _parse_civic_data(self, data):
        """Maps Google Civic API offices to officials."""
        officials = data.get('officials', [])
        offices = data.get('offices', [])
        
        reps = []
        for office in offices:
            role = office.get('name', 'Unknown Office')
            for index in office.get('officialIndices', []):
                official = officials[index]
                name = official.get('name', 'Unknown Name')
                emails = official.get('emails', ['No email publicly listed'])
                phones = official.get('phones', ['No phone publicly listed'])
                urls = official.get('urls', ['No website'])
                
                reps.append({
                    "role": role,
                    "name": name,
                    "email": emails[0],
                    "phone": phones[0],
                    "website": urls[0]
                })
        return reps

class AppNewsReader:
    """Application module for reading real local civic news."""
    def __init__(self, client):
        self.client = client

    def run(self):
        clear_screen()
        print("="*60)
        print(f"📰  LIVE CIVIC NEWS FOR: {self.client.config.get('city', 'Unknown').upper()}")
        print("="*60)
        print("Fetching latest updates from live RSS feeds...\n")
        
        news = self.client.fetch_news()
        
        if isinstance(news, str):
            print(news) # Print error message
        elif not news:
            print("No recent civic news found for your area.")
        else:
            for item in news:
                # Clean up the date string
                date_str = item['date'].replace(" GMT", "")
                print(f"[{date_str}]")
                wrapped_title = textwrap.fill(item['title'], width=60)
                print(wrapped_title)
                print(f"Read more: {item['link']}")
                print("-" * 60)
                
        pause_execution()

class AppRepDirectory:
    """Application module for browsing real local representatives."""
    def __init__(self, client):
        self.client = client

    def run(self):
        clear_screen()
        print("="*60)
        print("🏛️  LIVE REPRESENTATIVE DIRECTORY")
        print("="*60)
        print("Querying Google Civic Information API...\n")
        
        reps = self.client.fetch_representatives()
        
        if reps == "MISSING_CONFIG":
            print("Action Required: Address or API Key is missing.")
            print("Please run the Setup Wizard from the main menu to configure.")
        elif reps == "API_KEY_INVALID":
            print("Authentication Error: The Google Civic API Key provided is invalid or unauthorized.")
        elif isinstance(reps, str):
            print(reps) # Print other errors
        elif not reps:
            print("No representatives found for that address.")
        else:
            for rep in reps:
                print(f"Office:  {rep['role']}")
                print(f"Name:    {rep['name']}")
                print(f"Phone:   {rep['phone']}")
                print(f"Email:   {rep['email']}")
                print(f"Website: {rep['website']}")
                print("-" * 60)
            
        pause_execution()

class AppActionCenter:
    """Application module for drafting real emails to fetched representatives."""
    def __init__(self, client):
        self.client = client

    def run(self):
        while True:
            clear_screen()
            print("="*60)
            print("✍️  LIVE ACTION CENTER")
            print("="*60)
            print("1. Draft & Send Real Email to Representative")
            print("2. Return to Main Menu")
            print("="*60)
            
            choice = input("Select an option (1-2): ")
            
            if choice == '1':
                self.draft_email()
            elif choice == '2':
                break
            else:
                print("Invalid selection.")
                time.sleep(1)

    def draft_email(self):
        clear_screen()
        print("Fetching your representatives...")
        reps = self.client.fetch_representatives()
        
        if isinstance(reps, str) or not reps:
            print("\nCannot load representatives. Make sure your Address and API key are configured.")
            pause_execution()
            return
            
        # Filter reps that actually have an email
        emailable_reps = [r for r in reps if '@' in r['email']]
        
        if not emailable_reps:
            print("\nUnfortunately, none of your mapped representatives have public emails listed.")
            pause_execution()
            return

        clear_screen()
        print("--- Select Representative to Contact ---")
        for idx, rep in enumerate(emailable_reps):
            print(f"{idx + 1}. {rep['name']} - {rep['role']}")
            
        try:
            rep_choice = int(input("\nEnter number: ")) - 1
            if 0 <= rep_choice < len(emailable_reps):
                target = emailable_reps[rep_choice]
                issue = input("\nWhat specific local issue are you addressing?: ")
                stance = input("Briefly state your stance/demand: ")
                
                print("\nGenerating final draft...")
                time.sleep(1)
                
                subject_text = f"Constituent Concern regarding {issue}"
                body_text = f"""Dear {target['name']},

As a resident of your district, I am writing to you today regarding {issue}. 
{stance}. 

I urge you to consider the impact of this issue on our community. I look forward to hearing your plan to address this matter.

Sincerely,
A Concerned Constituent
{self.client.config.get('address', '')}
"""
                clear_screen()
                print("="*60)
                print(f"To: {target['email']}")
                print(f"Subject: {subject_text}")
                print("="*60)
                print(body_text.strip())
                print("="*60)
                
                send_now = input("\nDo you want to attempt to open this in your device's email client now? (Y/N): ").upper()
                if send_now == 'Y':
                    try:
                        # Build the actual mailto link
                        subject_encoded = urllib.parse.quote(subject_text)
                        body_encoded = urllib.parse.quote(body_text)
                        mailto_url = f"mailto:{target['email']}?subject={subject_encoded}&body={body_encoded}"
                        print("\nLaunching email client...")
                        webbrowser.open(mailto_url)
                    except Exception as e:
                        print(f"\nCould not automatically launch email client: {e}")
                
                pause_execution()
            else:
                print("Invalid selection.")
                time.sleep(1)
        except ValueError:
            print("Invalid input.")
            time.sleep(1)

class CivicAdvocateOS:
    """The main Operating System class that manages real apps and configuration."""
    def __init__(self):
        self.client = LiveCivicClient()
        self.apps = {
            '1': AppNewsReader(self.client),
            '2': AppRepDirectory(self.client),
            '3': AppActionCenter(self.client)
        }
        self.is_running = True

    def setup_wizard(self):
        """Walks the user through providing real data for the OS."""
        clear_screen()
        print("="*60)
        print("⚙️  SYSTEM CONFIGURATION & SETUP")
        print("="*60)
        print("To fetch real, accurate data, the OS needs your location.")
        print("Leave blank and press Enter to keep current value.\n")
        
        curr_city = self.client.config.get('city', '')
        city_input = input(f"City and State (e.g., Chicago, IL) [{curr_city}]: ")
        if city_input.strip():
            self.client.config['city'] = city_input.strip()

        curr_address = self.client.config.get('address', '')
        addr_input = input(f"Full Address or Zip Code (For API mapping) [{curr_address}]: ")
        if addr_input.strip():
            self.client.config['address'] = addr_input.strip()
            
        print("\n--- API Key Setup ---")
        print("To fetch actual representatives, you need a free Google Civic Information API Key.")
        print("Get one here: https://developers.google.com/civic-information")
        curr_key = "SET" if self.client.config.get('api_key') else "NOT SET"
        key_input = input(f"Enter API Key [{curr_key}]: ")
        if key_input.strip():
            self.client.config['api_key'] = key_input.strip()
            
        self.client.save_config()
        print("\nConfiguration saved locally.")
        pause_execution()

    def boot_sequence(self):
        """Simulates an OS boot-up while doing real setup checks."""
        clear_screen()
        type_text("Booting REAL Civic Advocate OS kernel...", 0.01)
        type_text("Mounting live network drivers...", 0.01)
        type_text("Checking local configuration file...", 0.01)
        time.sleep(0.5)
        
        # If it's the first time running, force setup
        if not self.client.config.get('city'):
            type_text("\n[!] FIRST BOOT DETECTED: Initialization required.", 0.03)
            time.sleep(1)
            self.setup_wizard()
            
        self.show_banner()

    def show_banner(self):
        clear_screen()
        banner = """
   _____ _       _         ___      _                     _         ____   _____ 
  / ____(_)     (_)       / _ \\    | |                   | |       / __ \\ / ____|
 | |     ___   ___  ___  | |_| | __| |_   _____  ___ __ _| |_ ___ | |  | | (___  
 | |    | \\ \\ / / |/ __| |  _  |/ _` \\ \\ / / _ \\/ __/ _` | __/ _ \\| |  | |\\___ \\ 
 | |____| |\\ V /| | (__  | | | | (_| |\\ V / (_) | (_| (_| | ||  __/ |__| |____) |
  \\_____|_| \\_/ |_|\\___| \\_| |_/\\__,_| \\_/ \\___/ \\___\\__,_|\\__\\___|\\____/|_____/ 
                                                                                 
        >>> LIVE ENVIRONMENT ACTIVE. CONNECTED TO REAL-WORLD DATA. <<<
        """
        print(banner)
        print("\nPress Enter to access the live dashboard.")
        input()

    def run(self):
        """The main execution loop for the OS dashboard."""
        self.boot_sequence()
        
        while self.is_running:
            clear_screen()
            print("="*60)
            print("🖥️  LIVE CIVIC ADVOCATE OS - DASHBOARD")
            print("="*60)
            print("Please select an application to launch:\n")
            print("  [1] 📰 Live News Reader    - Real local RSS feeds")
            print("  [2] 🏛️  Rep Directory      - Live API query (Requires Key)")
            print("  [3] ✍️  Action Center      - Real email integration")
            print("  [4] ⚙️  System Setup       - Update location & API keys")
            print("  [5] 🚪 Exit System")
            print("="*60)
            
            try:
                choice = input("\nroot@live-civic-os:~$ ").strip()
                
                if choice in self.apps:
                    self.apps[choice].run()
                elif choice == '4':
                    self.setup_wizard()
                elif choice == '5':
                    self.shutdown()
                else:
                    print("Error: Command not recognized.")
                    time.sleep(1)
            except KeyboardInterrupt:
                self.shutdown()
            except Exception as e:
                print(f"\nAn unexpected system error occurred: {e}")
                pause_execution()

    def shutdown(self):
        clear_screen()
        type_text("Flushing live connections...", 0.02)
        type_text("Saving local state...", 0.02)
        type_text("Terminating Live OS. Stay engaged, Citizen.", 0.03)
        self.is_running = False
        sys.exit(0)

if __name__ == "__main__":
    try:
        os_system = CivicAdvocateOS()
        os_system.run()
    except Exception as fatal_error:
        print(f"FATAL ERROR: Failed to boot Live OS. Details: {fatal_error}")
        sys.exit(1)
