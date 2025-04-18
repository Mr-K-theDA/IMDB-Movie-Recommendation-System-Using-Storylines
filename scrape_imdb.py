import time
import random
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

# Configuration
IMDB_URL = "https://www.imdb.com/search/title/?title_type=feature&release_date=2024-01-01,2024-12-31"
MAX_MOVIES = 500
DELAY = 5
HEADLESS = False

def setup_driver():
    chrome_options = webdriver.ChromeOptions()
    if HEADLESS:
        chrome_options.add_argument("--headless=new")
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
    
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    return driver

def expand_plot_section(driver):
    try:
        read_more = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, 'button.ipc-see-more__button')))
        driver.execute_script("arguments[0].click();", read_more)
        time.sleep(1)
    except:
        pass

def get_plot(driver):
    plot_selectors = [
        ('[data-testid="plot"] span', "standard plot"),
        ('[data-testid="storyline-plot-summary"]', "storyline section"),
        ('[data-testid="plot-xs_to_m"]', "compact plot"),
        ('.ipc-html-content-inner-div', "general content"),
        ('[data-testid="sub-section-summary"]', "summary section"),
        ('.sc-5f699a2-0.kKUuxe', "fallback class")
    ]
    
    for selector, description in plot_selectors:
        try:
            element = WebDriverWait(driver, 5).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, selector)))
            plot = element.text.strip()
            if plot and len(plot) > 50:  # Filter out short texts
                return plot
        except:
            continue
    return "Plot summary not available on IMDb yet"

def get_movie_details(driver, url):
    try:
        driver.get(url)
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '[data-testid="hero__pageTitle"]')))
        
        # Expand plot section if available
        expand_plot_section(driver)
        
        title = driver.find_element(By.CSS_SELECTOR, 'h1[data-testid="hero__pageTitle"]').text
        plot = get_plot(driver)
        
        return {
            "Movie Name": title.strip(),
            "Storyline": plot
        }
    except Exception as e:
        print(f"⚠️ Error scraping {url}: {str(e)}")
        return None

def handle_pagination(driver):
    try:
        next_btn = WebDriverWait(driver, 15).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, 'button.ipc-see-more__button:not([disabled])')))
        
        # Scroll and click using JavaScript
        driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", next_btn)
        time.sleep(1)
        driver.execute_script("arguments[0].click();", next_btn)
        
        # Wait for new content
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'div.ipc-metadata-list-summary-item__c')))
        return True
    except Exception as e:
        print(f"🚫 Pagination ended: {str(e)}")
        return False

def scrape_imdb():
    driver = setup_driver()
    movies = []
    
    try:
        driver.get(IMDB_URL)
        time.sleep(DELAY)
        
        while len(movies) < MAX_MOVIES:
            # Get current page movies
            movie_links = []
            try:
                movie_cards = WebDriverWait(driver, 20).until(
                    EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'a.ipc-title-link-wrapper[href*="/title/tt"]')))
                movie_links = list({card.get_attribute("href") for card in movie_cards})
            except:
                break

            # Scrape movie details
            for link in movie_links:
                if len(movies) >= MAX_MOVIES:
                    break
                
                time.sleep(DELAY + random.uniform(0, 3))
                movie_data = get_movie_details(driver, link)
                if movie_data:
                    movies.append(movie_data)
                    print(f"✅ ({len(movies)}) {movie_data['Movie Name']}")
                else:
                    print(f"❌ Failed: {link}")

            # Pagination
            if not handle_pagination(driver):
                break
            time.sleep(DELAY * 2)

    finally:
        driver.quit()
        if movies:
            df = pd.DataFrame(movies)
            df.to_csv("imdb_2024_full.csv", index=False)
            print(f"\n🎉 Successfully saved {len(movies)} movies!")
            print(df.head())
        else:
            print("\n❌ Scraping failed completely")

if __name__ == "__main__":
    scrape_imdb()