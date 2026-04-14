import flet as ft
from yt_dlp import YoutubeDL
import os
import time

def main(page: ft.Page):
    page.title = "Universal Video Downloader"
    page.theme_mode = "light"
    page.horizontal_alignment = "center"
    page.scroll = "auto"

    # Statik fayllar üçün qovluq yaradırıq
    if not os.path.exists("assets"):
        os.makedirs("assets")

    status_text = ft.Text(value="Link yapıştırın", color="blue")
    link_input = ft.TextField(label="Video URL", width=400)

    def download_video(e):
        url = link_input.value
        if not url:
            status_text.value = "Lütfen bir link girin!"
            page.update()
            return

        status_text.value = "Video hazırlanıyor... Lütfen bekleyin."
        page.update()

        try:
            # Videonu 'assets' qovluğuna endiririk ki, brauzer onu görə bilsin
            file_id = int(time.time())
            file_name = f"video_{file_id}.mp4"
            file_path = os.path.join("assets", file_name)
            
            ydl_opts = {
                'format': 'best',
                'outtmpl': file_path,
            }

            with YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])

            status_text.value = "Videonuz hazır!"
            
            # ƏN VACİB HİSSƏ: Bu linkə tıkladıqda yükləmə başlayacaq
            page.add(ft.ElevatedButton(
                "VİDEONU TELEFONA ENDİR", 
                icon=ft.icons.DOWNLOAD,
                on_click=lambda _: page.launch_url(f"/{file_name}")
            ))
            
        except Exception as ex:
            status_text.value = f"Hata: {str(ex)}"
        
        page.update()

    page.add(
        ft.Text("PRO VIDEO SAVER ONLINE", size=25, weight="bold"),
        link_input,
        ft.ElevatedButton("HAZIRLA", on_click=download_video),
        status_text
    )

if __name__ == "__main__":
    # assets_dir tətbiqə faylları ötürməyə icazə verir
    ft.app(
        target=main, 
        view=ft.AppView.WEB_BROWSER, 
        port=int(os.getenv("PORT", 8550)),
        assets_dir="assets"
    )
