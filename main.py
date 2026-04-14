import flet as ft
from yt_dlp import YoutubeDL
import os
import time

def main(page: ft.Page):
    page.title = "Universal Video Downloader"
    page.theme_mode = "light"
    page.horizontal_alignment = "center"
    page.scroll = "auto"

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
            # Server üzerinde geçici dosya adı
            file_name = f"video_{int(time.time())}.mp4"
            
            ydl_opts = {
                'format': 'best',
                'outtmpl': file_name,
            }

            with YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])

            status_text.value = "Videonuz hazır! Aşağıdaki linkten cihazınıza kaydedin."
            
            # Statik fayl kimi ötürmək üçün link yaradırıq
            download_link = ft.Text(
                "VİDEOYU CİHAZA KAYDET (TIKLA)", 
                size=20, 
                color="green", 
                weight="bold",
                selectable=True
            )
            page.add(download_link)
            
        except Exception as ex:
            status_text.value = f"Hata: {str(ex)}"
        
        page.update()

    page.add(
        ft.Text("PRO VIDEO SAVER ONLINE", size=25, weight="bold"),
        link_input,
        ft.ElevatedButton("HAZIRLA", on_click=download_video),
        status_text
    )

# RENDER ÜÇÜN PORT AYARI (ƏN VACİB HİSSƏ)
if __name__ == "__main__":
    port = int(os.getenv("PORT", 8550))
    ft.app(target=main, view=ft.AppView.WEB_BROWSER, port=port)
