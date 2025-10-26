"""
Generac Dealer Locator Scraper

Scrapes Generac's dealer network for generator installations.
Generac dealers are typically electrical contractors who also do HVAC and sometimes solar.

Target URL: https://www.generac.com/dealer-locator/

Capabilities detected from Generac certification:
- Generator installation (core product)
- Electrical work (required for generator install)
- Often HVAC (many dealers are dual-trade electrical/HVAC contractors)
"""

import os
import json
import requests
from typing import Dict, List
from scrapers.base_scraper import (
    BaseDealerScraper,
    DealerCapabilities,
    StandardizedDealer,
    ScraperMode
)
from scrapers.scraper_factory import ScraperFactory


class GeneracScraper(BaseDealerScraper):
    """
    Scraper for Generac dealer network.
    
    Generac's dealer tiers indicate service commitment level:
    - Premier: Highest commitment, full-service (sales, install, service, maintenance)
    - Elite Plus: Elevated service level
    - Elite: Installation and basic service support  
    - Standard: Basic dealer with no special designation
    
    PowerPro Premier designation indicates premium residential dealer.
    """
    
    OEM_NAME = "Generac"
    DEALER_LOCATOR_URL = "https://www.generac.com/dealer-locator/"
    PRODUCT_LINES = ["Generator", "Home Standby", "Portable", "Commercial", "Industrial"]
    
    # CSS Selectors
    SELECTORS = {
        "cookie_accept": "button:has-text('Accept Cookies')",
        "zip_input": "input[placeholder*='ZIP' i]",  # Updated: Generac removed name attribute
        "search_button": "button:has-text('Search')",
    }
    
    def __init__(self, mode: ScraperMode = ScraperMode.PLAYWRIGHT):
        super().__init__(mode)

        # Load RunPod config if in RUNPOD mode
        if mode == ScraperMode.RUNPOD:
            self.runpod_api_key = os.getenv("RUNPOD_API_KEY")
            self.runpod_endpoint_id = os.getenv("RUNPOD_ENDPOINT_ID")
            self.runpod_api_url = os.getenv(
                "RUNPOD_API_URL",
                f"https://api.runpod.ai/v2/{self.runpod_endpoint_id}/runsync"
            )

        # Load Browserbase config if in BROWSERBASE mode
        if mode == ScraperMode.BROWSERBASE:
            self.browserbase_api_key = os.getenv("BROWSERBASE_API_KEY")
            self.browserbase_project_id = os.getenv("BROWSERBASE_PROJECT_ID")
    
    def get_extraction_script(self) -> str:
        """
        JavaScript extraction script for Generac dealer data.
        
        This is the tested and validated extraction logic that:
        1. Uses phone links as anchors to find dealer cards
        2. Traverses DOM upward to find container with distance element
        3. Extracts 15 fields through DOM parsing and regex
        4. Returns filtered array of dealer objects
        """
        from config import EXTRACTION_SCRIPT
        return EXTRACTION_SCRIPT
    
    def detect_capabilities(self, raw_dealer_data: Dict) -> DealerCapabilities:
        """
        Detect capabilities from Generac dealer data.
        
        Generac certifications indicate:
        - All dealers: has_generator + has_electrical (minimum for generator install)
        - Premier tier: Full-service (sales, install, service) = higher commercial capability
        - PowerPro Premier: Premium residential focus
        - Many Generac dealers are dual-trade electrical/HVAC contractors
        
        Additional capabilities will be enriched via Apollo (employee count, revenue).
        """
        caps = DealerCapabilities()
        
        # All Generac dealers have generator and electrical capabilities
        caps.has_generator = True
        caps.has_electrical = True
        
        # Extract tier and designation
        tier = raw_dealer_data.get("tier", "Standard")
        is_power_pro_premier = raw_dealer_data.get("is_power_pro_premier", False)
        
        # Premier tier indicates full-service capability
        if tier == "Premier":
            caps.is_residential = True
            caps.is_commercial = True  # May be updated via Apollo enrichment
        
        # PowerPro Premier = premium residential focus
        if is_power_pro_premier:
            caps.is_residential = True
        
        # Elite Plus and Elite tiers indicate residential service
        if tier in ["Elite Plus", "Elite"]:
            caps.is_residential = True
        
        # Many Generac dealers are electrical/HVAC contractors
        # (will be validated via domain/name analysis in multi-OEM detector)
        # For now, we conservatively only mark confirmed capabilities
        
        # Add Generac OEM certification
        caps.oem_certifications.add("Generac")

        # Detect high-value contractor types (O&M and MEP+R)
        dealer_name = raw_dealer_data.get("name", "")
        certifications_list = []
        if tier == "Premier":
            certifications_list.append("Premier Dealer")
        caps.detect_high_value_contractor_types(dealer_name, certifications_list, tier)

        return caps
    
    def parse_dealer_data(self, raw_dealer_data: Dict, zip_code: str) -> StandardizedDealer:
        """
        Convert raw Generac dealer data to StandardizedDealer format.
        
        Args:
            raw_dealer_data: Dict from extraction script
            zip_code: ZIP code that was searched
        
        Returns:
            StandardizedDealer object
        """
        # Raw data already has most fields in correct format (tested extraction script)
        # Just need to wrap in StandardizedDealer and detect capabilities
        
        capabilities = self.detect_capabilities(raw_dealer_data)
        
        # Extract certifications from tier
        tier = raw_dealer_data.get("tier", "Standard")
        certifications = []
        if tier == "Premier":
            certifications.append("Premier Dealer")
        elif tier == "Elite Plus":
            certifications.append("Elite Plus Dealer")
        elif tier == "Elite":
            certifications.append("Elite Dealer")
        
        if raw_dealer_data.get("is_power_pro_premier"):
            certifications.append("PowerPro Premier")
        
        # Create StandardizedDealer
        dealer = StandardizedDealer(
            name=raw_dealer_data.get("name", ""),
            phone=raw_dealer_data.get("phone", ""),
            domain=raw_dealer_data.get("domain", ""),
            website=raw_dealer_data.get("website", ""),
            street=raw_dealer_data.get("street", ""),
            city=raw_dealer_data.get("city", ""),
            state=raw_dealer_data.get("state", ""),
            zip=raw_dealer_data.get("zip", ""),
            address_full=raw_dealer_data.get("address_full", ""),
            rating=raw_dealer_data.get("rating", 0.0),
            review_count=raw_dealer_data.get("review_count", 0),
            tier=tier,
            certifications=certifications,
            distance=raw_dealer_data.get("distance", ""),
            distance_miles=raw_dealer_data.get("distance_miles", 0.0),
            capabilities=capabilities,
            oem_source="Generac",
            scraped_from_zip=zip_code,
        )
        
        return dealer
    
    def _scrape_with_playwright(self, zip_code: str) -> List[StandardizedDealer]:
        """
        PLAYWRIGHT mode: Print manual MCP Playwright instructions.
        
        Returns empty list and prints workflow instructions for manual execution.
        """
        print(f"\n{'='*60}")
        print(f"Generac Dealer Scraper - PLAYWRIGHT Mode")
        print(f"ZIP Code: {zip_code}")
        print(f"{'='*60}\n")
        
        print("⚠️  MANUAL WORKFLOW - Execute these MCP Playwright tools in order:\n")
        
        print("1. Navigate to Generac dealer locator:")
        print(f'   mcp__playwright__browser_navigate({{"url": "{self.DEALER_LOCATOR_URL}"}})\n')
        
        print("2. Take snapshot to get current element refs:")
        print('   mcp__playwright__browser_snapshot({})\n')
        
        print("3. Click Accept Cookies button (MUST do first or interactions fail):")
        print('   mcp__playwright__browser_click({"element": "Accept Cookies", "ref": "[from snapshot]"})\n')
        
        print("4. Fill ZIP code input:")
        print(f'   mcp__playwright__browser_type({{')
        print(f'       "element": "ZIP code input",')
        print(f'       "ref": "[from snapshot]",')
        print(f'       "text": "{zip_code}",')
        print(f'       "submit": False')
        print(f'   }})\n')
        
        print("5. Click search button:")
        print('   mcp__playwright__browser_click({"element": "Search button", "ref": "[from snapshot]"})\n')
        
        print("6. Wait for AJAX results to load (3 seconds minimum):")
        print('   mcp__playwright__browser_wait_for({"time": 3})\n')
        
        print("7. Extract dealer data using tested extraction script:")
        extraction_script = self.get_extraction_script()
        print(f'   mcp__playwright__browser_evaluate({{"function": """{extraction_script}"""}})\n')
        
        print("8. Copy the results JSON and pass to parse_results():")
        print(f'   generac_scraper.parse_results(results_json, "{zip_code}")\n')
        
        print(f"{'='*60}\n")
        print("✅ Extraction script is tested and validated")
        print("⚠️  Element refs change between page loads - always take fresh snapshot")
        print(f"{'='*60}\n")
        
        return []
    
    def _scrape_with_runpod(self, zip_code: str) -> List[StandardizedDealer]:
        """
        RUNPOD mode: Execute automated scraping via serverless API.
        
        Sends 6-step workflow to RunPod Playwright API.
        This is the fully automated production mode.
        """
        if not self.runpod_api_key or not self.runpod_endpoint_id:
            raise ValueError(
                "Missing RunPod credentials. Set RUNPOD_API_KEY and RUNPOD_ENDPOINT_ID in .env"
            )
        
        # Build 6-step workflow for Generac
        workflow = [
            {"action": "navigate", "url": self.DEALER_LOCATOR_URL},
            {"action": "click", "selector": self.SELECTORS["cookie_accept"]},
            {"action": "fill", "selector": self.SELECTORS["zip_input"], "text": zip_code},
            {"action": "click", "selector": self.SELECTORS["search_button"]},
            {"action": "wait", "timeout": 3000},  # 3 seconds for AJAX
            {"action": "evaluate", "script": self.get_extraction_script()},
        ]
        
        # Make HTTP request to RunPod API
        payload = {"input": {"workflow": workflow}}
        headers = {
            "Authorization": f"Bearer {self.runpod_api_key}",
            "Content-Type": "application/json",
        }
        
        try:
            print(f"[RunPod] Scraping Generac dealers for ZIP {zip_code}...")
            
            response = requests.post(
                self.runpod_api_url,
                json=payload,
                headers=headers,
                timeout=60  # 60 second timeout
            )
            response.raise_for_status()
            
            result = response.json()
            
            if result.get("status") == "success":
                raw_dealers = result.get("results", [])
                print(f"[RunPod] Extracted {len(raw_dealers)} dealers")
                
                dealers = [self.parse_dealer_data(d, zip_code) for d in raw_dealers]
                return dealers
            else:
                error_msg = result.get("error", "Unknown error")
                raise Exception(f"RunPod API error: {error_msg}")
        
        except requests.exceptions.Timeout:
            raise Exception(f"RunPod API timeout after 60 seconds")
        except requests.exceptions.RequestException as e:
            raise Exception(f"RunPod API request failed: {str(e)}")
        except json.JSONDecodeError:
            raise Exception("Failed to parse RunPod API response as JSON")

    def _scrape_with_browserbase(self, zip_code: str) -> List[StandardizedDealer]:
        """
        BROWSERBASE mode: Execute automated scraping via Browserbase cloud browser.

        Browserbase provides remote browser sessions accessible via Playwright CDP.
        This method:
        1. Creates a Browserbase session
        2. Connects via Playwright CDP
        3. Executes the 6-step Generac workflow
        4. Extracts dealer data
        5. Closes the session

        Requires: playwright Python package (pip install playwright)
        """
        if not self.browserbase_api_key or not self.browserbase_project_id:
            raise ValueError(
                "Missing Browserbase credentials. Set BROWSERBASE_API_KEY and BROWSERBASE_PROJECT_ID in .env"
            )

        try:
            # Import playwright (only imported when BROWSERBASE mode is used)
            try:
                from playwright.sync_api import sync_playwright
            except ImportError:
                raise ImportError(
                    "Browserbase mode requires 'playwright' package. "
                    "Install with: pip install playwright && playwright install chromium"
                )

            print(f"[Browserbase] Creating session for ZIP {zip_code}...")

            # Step 1: Create Browserbase session
            create_session_url = f"https://www.browserbase.com/v1/sessions"
            headers = {
                "X-BB-API-Key": self.browserbase_api_key,
                "Content-Type": "application/json",
            }
            payload = {
                "projectId": self.browserbase_project_id,
            }

            response = requests.post(create_session_url, json=payload, headers=headers, timeout=10)
            response.raise_for_status()
            session_data = response.json()

            session_id = session_data["id"]
            connect_url = session_data["connectUrl"]  # WebSocket URL for CDP

            print(f"[Browserbase] Session created: {session_id}")
            print(f"[Browserbase] Connecting to remote browser...")

            # Step 2: Connect to Browserbase via Playwright CDP
            with sync_playwright() as p:
                browser = p.chromium.connect_over_cdp(connect_url)
                context = browser.contexts[0]  # Browserbase provides a default context
                page = context.pages[0] if context.pages else context.new_page()

                print(f"[Browserbase] Connected! Navigating to dealer locator...")

                # Step 3: Execute the 6-step workflow
                # 1. Navigate
                page.goto(self.DEALER_LOCATOR_URL, wait_until="networkidle", timeout=30000)

                # 2. Dismiss cookie dialog
                try:
                    page.click(self.SELECTORS["cookie_accept"], timeout=5000)
                except Exception:
                    pass  # Cookie dialog may not appear

                # 3. Fill ZIP code
                page.fill(self.SELECTORS["zip_input"], zip_code)

                # 4. Click search
                page.click(self.SELECTORS["search_button"])

                # 5. Wait for AJAX results (3 seconds)
                page.wait_for_timeout(3000)

                # 6. Extract dealer data
                print(f"[Browserbase] Extracting dealer data...")
                raw_dealers = page.evaluate(self.get_extraction_script())

                print(f"[Browserbase] Extracted {len(raw_dealers)} dealers")

                # Close browser connection
                browser.close()

            # Step 4: Close Browserbase session
            delete_session_url = f"https://www.browserbase.com/v1/sessions/{session_id}"
            requests.delete(delete_session_url, headers=headers, timeout=10)
            print(f"[Browserbase] Session closed")

            # Step 5: Parse results
            dealers = [self.parse_dealer_data(d, zip_code) for d in raw_dealers]
            return dealers

        except requests.exceptions.Timeout:
            raise Exception(f"Browserbase API timeout")
        except requests.exceptions.RequestException as e:
            raise Exception(f"Browserbase API request failed: {str(e)}")
        except json.JSONDecodeError:
            raise Exception("Failed to parse Browserbase API response as JSON")
        except Exception as e:
            raise Exception(f"Browserbase scraping failed: {str(e)}")

    def _scrape_with_patchright(self, zip_code: str) -> List[StandardizedDealer]:
        """
        PATCHRIGHT mode: Stealth browser automation with bot detection bypass.

        Uses Patchright (patched Playwright) for stealth automation:
        - Patches 20+ automation fingerprints
        - Uses real Chrome browser (not Chromium)
        - Persistent context for realistic browser profile

        Workflow:
        1. Launch persistent Chrome context
        2. Navigate and dismiss cookie dialog
        3. Fill ZIP code and search
        4. Extract dealer data

        Requires: patchright Python package (pip install patchright)
        """
        try:
            # Import patchright (only imported when PATCHRIGHT mode is used)
            try:
                from patchright.sync_api import sync_playwright
            except ImportError:
                raise ImportError(
                    "Patchright mode requires 'patchright' package. "
                    "Install with: pip install patchright && patchright install chromium"
                )

            print(f"[Patchright] Launching stealth browser for ZIP {zip_code}...")

            # Step 1: Launch Patchright with persistent context (max stealth)
            with sync_playwright() as p:
                # Patchright's patched chromium has 20+ fingerprint fixes built-in
                context = p.chromium.launch_persistent_context(
                    user_data_dir="./patchright-chrome-profile",
                    headless=False,  # Visible mode (required for stealth)
                    no_viewport=True,  # Natural viewport
                    args=[
                        "--disable-blink-features=AutomationControlled",
                        "--disable-dev-shm-usage",
                        "--no-sandbox",
                    ],
                )

                page = context.pages[0] if context.pages else context.new_page()

                print(f"[Patchright] Navigating to Generac dealer locator...")

                # Step 2: Execute the 6-step workflow
                # 1. Navigate
                page.goto(self.DEALER_LOCATOR_URL, wait_until="networkidle", timeout=30000)

                # 2. Dismiss cookie dialog
                try:
                    page.click(self.SELECTORS["cookie_accept"], timeout=5000)
                except Exception:
                    pass  # Cookie dialog may not appear

                # 3. Fill ZIP code
                page.fill(self.SELECTORS["zip_input"], zip_code)

                # 4. Click search
                page.click(self.SELECTORS["search_button"])

                # 5. Wait for AJAX results (3 seconds)
                page.wait_for_timeout(3000)

                # 6. Extract dealer data
                print(f"[Patchright] Extracting dealer data...")
                raw_dealers = page.evaluate(self.get_extraction_script())

                print(f"[Patchright] Extracted {len(raw_dealers)} dealers")

                # Close browser
                context.close()

            # Step 3: Parse results
            dealers = [self.parse_dealer_data(d, zip_code) for d in raw_dealers]
            return dealers

        except Exception as e:
            raise Exception(f"Patchright scraping failed: {str(e)}")

    def parse_results(self, results_json: List[Dict], zip_code: str) -> List[StandardizedDealer]:
        """
        Helper method to parse manual PLAYWRIGHT results.
        
        Args:
            results_json: Array of dealer objects from browser_evaluate
            zip_code: ZIP code that was searched
        
        Returns:
            List of StandardizedDealer objects
        """
        dealers = [self.parse_dealer_data(d, zip_code) for d in results_json]
        self.dealers.extend(dealers)
        return dealers


# Register Generac scraper with factory
ScraperFactory.register("Generac", GeneracScraper)
ScraperFactory.register("generac", GeneracScraper)


# Example usage
if __name__ == "__main__":
    from config import ZIP_CODES_TEST
    
    # PLAYWRIGHT mode (manual workflow)
    scraper = GeneracScraper(mode=ScraperMode.PLAYWRIGHT)
    scraper.scrape_zip_code("53202")  # Milwaukee
    
    # RUNPOD mode (automated)
    # scraper = GeneracScraper(mode=ScraperMode.RUNPOD)
    # dealers = scraper.scrape_multiple(ZIP_CODES_TEST)
    # scraper.deduplicate()
    # scraper.save_json("output/generac_dealers.json")
    # scraper.save_csv("output/generac_dealers.csv")
