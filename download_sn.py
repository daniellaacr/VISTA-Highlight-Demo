from SoccerNet.Downloader import SoccerNetDownloader

SN_PATH = r"C:\SoccerNetData"

mySoccerNetDownloader = SoccerNetDownloader(LocalDirectory=SN_PATH)

mySoccerNetDownloader.downloadGames(
    files=["annotations.json"],   # ESTE es el archivo con bounding boxes
    split=["train"],
    task="tracking"
)


print("Descarga de etiquetas terminada.")
