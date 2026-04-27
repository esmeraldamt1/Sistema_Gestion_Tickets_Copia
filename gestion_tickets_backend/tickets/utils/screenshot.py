from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time

def capture_screenshot(url, output_path="screenshot.png"):
    """Captura una pantalla del sitio web y la guarda como imagen."""

    # Configurar opciones de Chrome
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Ejecutar sin abrir navegador
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1280x1024")

    # Configurar WebDriverManager para gestionar ChromeDriver automáticamente
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)

    try:
        driver.get(url)  # Abrir la URL
        time.sleep(3)  # Esperar a que cargue la página
        driver.save_screenshot(output_path)  # Guardar captura de pantalla
        print(f"✅ Captura guardada en: {output_path}")
    except Exception as e:
        print(f"❌ Error capturando pantalla: {e}")
    finally:
        driver.quit()  # Cerrar el navegador

# **Prueba ejecutando este archivo**
if __name__ == "__main__":
    capture_screenshot("http://localhost:5173/tickets", "ticket_screenshot.png")
