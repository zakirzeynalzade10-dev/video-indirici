import flet as ft
from yt_dlp import YoutubeDL
import os
import time

def main(page: ft.Page):
    page.title = "Universal Video Downloader"
    page.theme_mode = "light"
    page.horizontal_alignment = "center"
    page.scroll = "auto"

    # Statik fayllar üçün qovluğu yoxlayırıq
    if not os.path.exists("assets"):
        os.makedirs("assets")

    status_text = ft.Text(value="Link yapıştırın", color="blue")
    link_input = ft.TextField(label="Video URL", width=400)
    
    # Endirmə düyməsi üçün yer
    download_link_container = ft.Column(horizontal_alignment="center")

    def download_video(e):
        url = link_input.value
        if not url:
            status_text.value = "Lütfen bir link girin!"
            page.update()
            return

        status_text.value = "Video hazırlanıyor... Lütfen bekleyin."
        download_link_container.controls.clear()
        page.update()

        try:
            # Fayl adını zaman damğası ilə unikal edirik
            file_id = int(time.time())
            file_name = f"video_{file_id}.mp4"
            file_path = os.path.join("assets", file_name)
            
            ydl_opts = {
                'format': 'best',
                'outtmpl': file_path,
                'noplaylist': True,
            }

            with YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])

            status_text.value = "Videonuz hazır!"
            # Ikon xətası olmasın deyə standart ikon adından istifadə edirik
            download_link_container.controls.append(
                ft.ElevatedButton(
                    "VİDEONU TELEFONA ENDİR", 
                    icon=ft.icons.FILE_DOWNLOAD, # DOWNLOAD əvəzinə FILE_DOWNLOAD
                    on_click=lambda _: page.launch_url(f"/{file_name}")
                )
            )
            
        except Exception as ex:
            status_text.value = f"Hata: {str(ex)}"
        
        page.update()

    page.add(
        ft.Text("PRO VIDEO SAVER ONLINE", size=25, weight="bold"),
        link_input,
        ft.ElevatedButton("VİDEONU HAZIRLA", on_click=download_video),
        status_text,
        download_link_container
    )

if __name__ == "__main__":
    ft.app(
        target=main, 
        view=ft.AppView.WEB_BROWSER, 
        port=int(os.getenv("PORT", 8550)),
        assets_dir="assets" # Faylların brauzerdən görünməsi üçün mütləqdir
    )
