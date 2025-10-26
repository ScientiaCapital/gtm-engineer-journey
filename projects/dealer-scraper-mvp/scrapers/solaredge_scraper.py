"""
SolarEdge Certified Installer Scraper

Scrapes SolarEdge's certified installer network for inverter and optimizer installations.
SolarEdge installers typically handle string inverters with power optimizers and increasingly batteries.

Target URL: https://www.solaredge.com/us/find-installer

Capabilities detected from SolarEdge certification:
- Solar installation (string inverters + optimizers are their core)
- Battery installation (SolarEdge Home Battery)
- Electrical work (required for inverter installation)
- Commercial and residential installations

Strategic importance for Coperniq:
- SolarEdge dominates commercial solar (string inverters scale better than microinverters)
- Many installers do BOTH Enphase (residential) AND SolarEdge (commercial)
- These dual-certified contractors are prime Coperniq targets
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


class SolarEdgeScraper(BaseDealerScraper):
    """
    Scraper for SolarEdge certified installer network.

    SolarEdge focuses on string inverters with DC power optimizers,
    contrasting with Enphase's microinverter approach.

    Many commercial installers prefer SolarEdge for:
    - Better scalability for large rooftop arrays
    - Lower cost per watt at scale
    - Centralized inverter management

    Installers often carry BOTH Enphase (residential) and SolarEdge (commercial).
    """

    OEM_NAME = "SolarEdge"
    DEALER_LOCATOR_URL = "https://www.solaredge.com/us/find-installer"
    PRODUCT_LINES = ["String Inverters", "Power Optimizers", "Home Battery", "EV Chargers", "Commercial"]

    # CSS Selectors (to be verified after site inspection)
    SELECTORS = {
        "search_input": "input[placeholder*='zip']",     # Likely ZIP code input
        "search_button": "button[type='submit']",        # Search button
        "installer_cards": ".installer-card",            # Installer result cards
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

    def get_extraction_script(self) -> str:
        """
        JavaScript extraction script for SolarEdge installer data.

        Focus on commercial installers and those offering O&M services.
        String inverter expertise often indicates commercial capability.
        """

        # JavaScript extraction - prioritizes commercial installers
        extraction_script = """
        () => {
            const dealers = [];

            // Find all installer elements (adjust selector based on actual DOM)
            const installerElements = document.querySelectorAll('.installer-card, .dealer-item, [data-installer]');

            installerElements.forEach(element => {
                try {
                    // Extract dealer name
                    const nameElement = element.querySelector('.installer-name, .dealer-name, h3, h4');
                    const name = nameElement?.textContent?.trim() || '';

                    if (!name) return;

                    // Extract phone
                    const phoneElement = element.querySelector('[href^="tel:"], .phone, .contact-phone');
                    let phone = phoneElement?.textContent?.trim() || phoneElement?.href?.replace('tel:', '') || '';
                    phone = phone.replace(/[^\\d]/g, ''); // Normalize to digits only

                    // Extract website
                    const websiteElement = element.querySelector('a[href*="http"], .website, .dealer-website');
                    const website = websiteElement?.href || '';

                    // Extract address
                    const addressElement = element.querySelector('.address, .location, .dealer-address');
                    const address_full = addressElement?.textContent?.trim() || '';

                    // Parse address components
                    let street = '', city = '', state = '', zip = '';
                    if (address_full) {
                        const parts = address_full.split(',').map(p => p.trim());
                        if (parts.length >= 2) {
                            street = parts[0];
                            const lastPart = parts[parts.length - 1];
                            const stateZipMatch = lastPart.match(/([A-Z]{2})\\s+(\\d{5})/);
                            if (stateZipMatch) {
                                state = stateZipMatch[1];
                                zip = stateZipMatch[2];
                                city = parts[parts.length - 2] || '';
                            }
                        }
                    }

                    // Extract certifications and capabilities
                    const certifications = ['SolarEdge Certified'];
                    const capabilities = [];

                    // Look for certification badges
                    const badges = element.querySelectorAll('.badge, .certification, .capability, [class*="cert"]');
                    badges.forEach(badge => {
                        const text = badge.textContent?.trim();
                        if (text) {
                            if (text.toLowerCase().includes('commercial')) {
                                capabilities.push('Commercial');
                                certifications.push('Commercial Certified');
                            }
                            if (text.toLowerCase().includes('battery') || text.toLowerCase().includes('storage')) {
                                capabilities.push('Battery Storage');
                                certifications.push('Battery Certified');
                            }
                            if (text.toLowerCase().includes('service') || text.toLowerCase().includes('maintenance')) {
                                capabilities.push('O&M Services');
                                certifications.push('Service Provider');
                            }
                            if (text.toLowerCase().includes('ev') || text.toLowerCase().includes('charger')) {
                                capabilities.push('EV Chargers');
                            }
                        }
                    });

                    // Default capabilities for all SolarEdge installers
                    capabilities.push('Solar');
                    capabilities.push('String Inverters');

                    // Extract rating if available
                    const ratingElement = element.querySelector('.rating, .stars, [class*="rating"]');
                    let rating = 0;
                    if (ratingElement) {
                        const ratingText = ratingElement.textContent || ratingElement.getAttribute('data-rating') || '';
                        rating = parseFloat(ratingText) || 0;
                    }

                    // Extract review count
                    const reviewElement = element.querySelector('.reviews, .review-count');
                    let review_count = 0;
                    if (reviewElement) {
                        const reviewText = reviewElement.textContent || '';
                        const reviewMatch = reviewText.match(/(\\d+)/);
                        review_count = reviewMatch ? parseInt(reviewMatch[1]) : 0;
                    }

                    // Check for commercial focus (important for Coperniq)
                    const has_commercial = capabilities.includes('Commercial') ||
                                          name.toLowerCase().includes('commercial') ||
                                          name.toLowerCase().includes('solar systems') ||
                                          name.toLowerCase().includes('energy solutions');

                    // Check for O&M services (premium target)
                    const has_ops_maintenance = capabilities.includes('O&M Services') ||
                                               name.toLowerCase().includes('service') ||
                                               name.toLowerCase().includes('maintenance');

                    const dealer = {
                        name: name,
                        phone: phone,
                        website: website,
                        street: street,
                        city: city,
                        state: state,
                        zip: zip,
                        address_full: address_full,
                        certifications: certifications,
                        capabilities: capabilities,
                        rating: rating,
                        review_count: review_count,
                        tier: has_commercial ? 'Commercial' : 'Residential',
                        distance: '',
                        distance_miles: 0,
                        has_commercial: has_commercial,
                        has_ops_maintenance: has_ops_maintenance,
                        is_resimercial: capabilities.includes('Commercial') // If commercial, likely does both
                    };

                    // Prioritize commercial and O&M providers
                    if (has_ops_maintenance && has_commercial) {
                        dealers.unshift(dealer); // Highest priority
                    } else if (has_commercial) {
                        dealers.push(dealer);     // Second priority
                    } else {
                        dealers.push(dealer);     // Lower priority
                    }

                } catch (error) {
                    console.error('Error parsing SolarEdge dealer:', error);
                }
            });

            console.log(`Found ${dealers.length} SolarEdge installers`);
            console.log(`Commercial: ${dealers.filter(d => d.has_commercial).length}`);
            console.log(`O&M Providers: ${dealers.filter(d => d.has_ops_maintenance).length}`);

            return dealers;
        }
        """

        return extraction_script

    def detect_capabilities(self, raw_dealer_data: Dict) -> DealerCapabilities:
        """
        Detect capabilities from SolarEdge installer data.

        SolarEdge certifications indicate:
        - All installers: has_solar + has_inverters + has_electrical
        - String inverter expertise often = commercial capability
        - Battery certified = SolarEdge Home Battery installation
        - Most do roofing work (solar installations)
        """
        caps = DealerCapabilities()

        # All SolarEdge installers have these
        caps.has_solar = True
        caps.has_inverters = True  # String inverters (not micro)
        caps.has_electrical = True
        caps.has_roofing = True  # Solar requires roof work

        # Check capabilities list
        capabilities = raw_dealer_data.get("capabilities", [])

        # Battery storage
        if "Battery Storage" in capabilities or "Storage" in capabilities:
            caps.has_battery = True

        # Commercial capability (important!)
        if "Commercial" in capabilities or raw_dealer_data.get("has_commercial"):
            caps.is_commercial = True

        # Check for resimercial (both markets)
        if raw_dealer_data.get("is_resimercial"):
            caps.is_residential = True
            caps.is_commercial = True
        else:
            # Default to residential if not explicitly commercial
            caps.is_residential = True

        # Add SolarEdge OEM certification
        caps.oem_certifications.add("SolarEdge")
        caps.inverter_oems.add("SolarEdge")

        # If battery certified, add to battery OEMs
        if caps.has_battery:
            caps.battery_oems.add("SolarEdge")

        return caps

    def parse_dealer_data(self, raw_dealer_data: Dict, zip_code: str) -> StandardizedDealer:
        """
        Convert raw SolarEdge installer data to StandardizedDealer format.
        """
        # Extract domain from website
        website = raw_dealer_data.get("website", "")
        domain = ""
        if website:
            try:
                from urllib.parse import urlparse
                parsed = urlparse(website)
                domain = parsed.netloc.replace("www.", "")
            except:
                domain = ""

        # Parse distance
        distance_str = raw_dealer_data.get("distance", "")
        distance_miles = 0.0
        if distance_str:
            try:
                distance_miles = float(distance_str.replace(" mi", "").replace(",", ""))
            except:
                distance_miles = 0.0

        # Build full address if not provided
        street = raw_dealer_data.get("street", "")
        city = raw_dealer_data.get("city", "")
        state = raw_dealer_data.get("state", "")
        zip_val = raw_dealer_data.get("zip", "")

        address_full = raw_dealer_data.get("address_full", "")
        if not address_full and all([street, city, state, zip_val]):
            address_full = f"{street}, {city}, {state} {zip_val}"

        # Detect capabilities
        capabilities = self.detect_capabilities(raw_dealer_data)

        # Set O&M and resimercial flags (for GTM targeting)
        has_ops_maintenance = raw_dealer_data.get("has_ops_maintenance", False)
        is_resimercial = raw_dealer_data.get("is_resimercial", False)

        # Create StandardizedDealer
        dealer = StandardizedDealer(
            name=raw_dealer_data.get("name", ""),
            phone=raw_dealer_data.get("phone", ""),
            domain=domain,
            website=website,
            street=street,
            city=city,
            state=state,
            zip=zip_val,
            address_full=address_full,
            rating=raw_dealer_data.get("rating", 0.0),
            review_count=raw_dealer_data.get("review_count", 0),
            tier=raw_dealer_data.get("tier", "Standard"),
            certifications=raw_dealer_data.get("certifications", []),
            distance=distance_str,
            distance_miles=distance_miles,
            capabilities=capabilities,
            oem_source="SolarEdge",
            scraped_from_zip=zip_code,
            has_ops_maintenance=has_ops_maintenance,
            is_resimercial=is_resimercial
        )

        return dealer

    def _scrape_with_playwright(self, zip_code: str) -> List[StandardizedDealer]:
        """
        PLAYWRIGHT mode: Print manual MCP Playwright instructions.
        """
        print(f"\n{'='*60}")
        print(f"SolarEdge Installer Network Scraper - PLAYWRIGHT Mode")
        print(f"ZIP Code: {zip_code}")
        print(f"{'='*60}\n")

        print("⚠️  MANUAL WORKFLOW - Execute these MCP Playwright tools in order:\n")

        print("1. Navigate to SolarEdge installer locator:")
        print(f'   mcp__playwright__browser_navigate({{"url": "{self.DEALER_LOCATOR_URL}"}})\n')

        print("2. Take snapshot to get current element refs:")
        print('   mcp__playwright__browser_snapshot({})\n')

        print("3. Handle cookie consent (if present):")
        print('   mcp__playwright__browser_click({"element": "Accept", "ref": "[from snapshot]"})\n')

        print("4. Enter ZIP code:")
        print(f'   mcp__playwright__browser_type({{')
        print(f'       "element": "ZIP code input",')
        print(f'       "ref": "[from snapshot]",')
        print(f'       "text": "{zip_code}",')
        print(f'       "submit": False')
        print(f'   }})\n')

        print("5. Click search button:")
        print('   mcp__playwright__browser_click({"element": "Search", "ref": "[from snapshot]"})\n')

        print("6. Wait for results:")
        print('   mcp__playwright__browser_wait_for({"time": 3})\n')

        print("7. Extract installer data:")
        extraction_script = self.get_extraction_script()
        print(f'   mcp__playwright__browser_evaluate({{"function": """{extraction_script}"""}})\n')

        print("8. Process results with:")
        print(f'   solaredge_scraper.parse_results(results_json, "{zip_code}")\n')

        print(f"{'='*60}\n")

        return []

    def _scrape_with_runpod(self, zip_code: str) -> List[StandardizedDealer]:
        """
        RUNPOD mode: Execute automated scraping via serverless API.
        """
        if not self.runpod_api_key or not self.runpod_endpoint_id:
            raise ValueError(
                "Missing RunPod credentials. Set RUNPOD_API_KEY and RUNPOD_ENDPOINT_ID in .env"
            )

        # Build workflow for SolarEdge
        workflow = [
            {"action": "navigate", "url": self.DEALER_LOCATOR_URL},
            {"action": "wait", "timeout": 2000},
            {"action": "fill", "selector": self.SELECTORS["search_input"], "text": zip_code},
            {"action": "click", "selector": self.SELECTORS["search_button"]},
            {"action": "wait", "timeout": 3000},
            {"action": "evaluate", "script": self.get_extraction_script()},
        ]

        # Make HTTP request to RunPod API
        payload = {"input": {"workflow": workflow}}
        headers = {
            "Authorization": f"Bearer {self.runpod_api_key}",
            "Content-Type": "application/json",
        }

        try:
            response = requests.post(
                self.runpod_api_url,
                json=payload,
                headers=headers,
                timeout=60
            )
            response.raise_for_status()

            result = response.json()

            if result.get("status") == "success":
                raw_dealers = result.get("results", [])
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

    def _scrape_with_patchright(self, zip_code: str) -> List[StandardizedDealer]:
        """
        PATCHRIGHT mode: Not implemented yet.
        """
        raise NotImplementedError("Patchright mode not yet implemented for SolarEdge")

    def parse_results(self, results_json: List[Dict], zip_code: str) -> List[StandardizedDealer]:
        """
        Helper method to parse manual PLAYWRIGHT results.
        """
        dealers = [self.parse_dealer_data(d, zip_code) for d in results_json]
        self.dealers.extend(dealers)
        return dealers


# Register SolarEdge scraper with factory
ScraperFactory.register("SolarEdge", SolarEdgeScraper)
ScraperFactory.register("solaredge", SolarEdgeScraper)


# Example usage
if __name__ == "__main__":
    # PLAYWRIGHT mode (manual workflow)
    scraper = SolarEdgeScraper(mode=ScraperMode.PLAYWRIGHT)
    scraper.scrape_zip_code("94102")  # San Francisco

    # RUNPOD mode (automated)
    # scraper = SolarEdgeScraper(mode=ScraperMode.RUNPOD)
    # dealers = scraper.scrape_zip_code("94102")
    # scraper.save_json("output/solaredge_installers_sf.json")