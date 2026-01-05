import asyncio
from pydoll.browser import Chrome

async def resolver_cloudflare():
    async with Chrome() as browser:
        print("🚀 Iniciando navegador con PyDoll...")
        page = await browser.start()

        await page.enable_auto_solve_cloudflare_captcha()
        print("🕵️  Modo Auto-Solve de Cloudflare activado.")

        url = "https://2captcha.com/demo/cloudflare-turnstile"
        print(f"🔗 Navegando a: {url}")
        await page.go_to(url)

        print("⏳ Esperando resolución del desafío...")

        token = None
        for i in range(30):
            try:
                element = await page.find(name="cf-turnstile-response", timeout=1)
                
                if element:
                    token_val = element.get_attribute("value")
                    
                    if asyncio.iscoroutine(token_val):
                        token_val = await token_val
                    
                    if token_val and len(token_val) > 0:
                        token = token_val
                        print(f"🔍 Token detectado en intento {i+1}")
                        break
                        
            except Exception as e:
                pass
            
            await asyncio.sleep(1)

        if token:
            print("\n✅ ¡CAPTCHA RESUELTO CON ÉXITO!")
            print(f"🎟️ Token obtenido: {token[:50]}...")
        else:
            print("\n❌ No se detectó el token después de 30 segundos.")

        await asyncio.sleep(3)
        print("👋 Cerrando navegador.")

if __name__ == '__main__':
    asyncio.run(resolver_cloudflare())