import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

STREAMLIT_URL = "https://creditpulse-indian-aplrf7swwheadhpqhouazq.streamlit.app/" 

def main():
    options = Options()
    options.add_argument('--headless=new')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    
    # Crucial: Large window size ensures elements aren't hidden by mobile-responsive layouts
    options.add_argument('--window-size=1920,1080')
    
    # Spoof user agent to bypass basic automated bot scrapers
    options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36')
    
    print("Initializing Chrome Driver...")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    
    try:
        print(f"Navigating to {STREAMLIT_URL}...")
        driver.get(STREAMLIT_URL)
        
        # Give the cloud wrapper plenty of time to render its elements
        print("Waiting for page load (10 seconds)...")
        time.sleep(10)  
        
        print("Searching for the wake-up button inside Shadow DOM layers...")
        
        # JavaScript logic designed to pierce Streamlit's shadow root barriers
        js_script = """
        // Method 1: Check known custom tags used by Streamlit Cloud
        const host = document.querySelector('st-cloud-viewer') || document.querySelector('cloud-viewer');
        if (host && host.shadowRoot) {
            const btn = host.shadowRoot.querySelector('button');
            if (btn && btn.textContent.toLowerCase().includes('get this app back up')) {
                return btn;
            }
        }
        
        // Method 2: Fallback deep scan across all page elements to find any hidden shadow roots
        const allElements = document.querySelectorAll('*');
        for (let el of allElements) {
            if (el.shadowRoot) {
                const btn = el.shadowRoot.querySelector('button');
                if (btn && btn.textContent.toLowerCase().includes('get this app back up')) {
                    return btn;
                }
            }
        }
        return null;
        """
        
        # Attempt to capture the button element object
        wake_button = driver.execute_script(js_script)
        
        if wake_button:
            print("Wake-up button successfully intercepted! Triggering click sequence...")
            # Click directly via JS execution context to bypass physical click blockages
            driver.execute_script("arguments[0].click();", wake_button)
            print("Success! Wake-up button clicked.")
            
            # Allow the backend server container ample time to spin up and load resources
            print("Holding connection open for 25 seconds while container spins up...")
            time.sleep(25) 
            print("App should now be completely functional.")
        else:
            print("Wake up button not found. The app is likely already active and running!")
            
    except Exception as e:
        print(f"An unexpected error occurred during execution: {e}")
    finally:
        print("Closing the automation driver instance...")
        driver.quit()
        print("Driver closed safely.")

if __name__ == "__main__":
    main()
