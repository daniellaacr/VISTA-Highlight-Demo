# check_tasks.py
from SoccerNet.Downloader import SoccerNetDownloader

SN_PATH = r"C:\SoccerNetData"

def main():
    downloader = SoccerNetDownloader(LocalDirectory=SN_PATH)
    print("SoccerNetDownloader creado correctamente.")
    print(f"Descargando únicamente etiquetas v3 en {SN_PATH} ...")
    downloader.downloadGames(
        files=["Labels-v3.json"],
        split=["train"],      # o ["train","valid","test"] si quieres todo
        task="frames"         # tarea documentada para SoccerNet-v3
    )
    print("Descarga terminada.")

if __name__ == "__main__":
    main()
