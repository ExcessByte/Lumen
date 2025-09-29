import requests
from PySide6.QtWidgets import QApplication, QWidget
from PySide6.QtCore import Qt, QTimer, Slot, QSize, QRectF, QThread, Signal
from PySide6.QtGui import QPainter, QPixmap, QColor, QFont, QPainterPath
import spotipy

class CoverLoader(QThread):
    image_loaded = Signal(QPixmap)

    def __init__(self, url):
        super().__init__()
        self.url = url

    def run(self):
        try:
            response = requests.get(self.url, timeout=8)
            response.raise_for_status()
            pixmap = QPixmap()
            if pixmap.loadFromData(response.content):
                self.image_loaded.emit(pixmap)
            else:
                self.image_loaded.emit(QPixmap()) 
        except Exception as e:
            print(f"Cover load failed for {self.url}: {e}")
            self.image_loaded.emit(QPixmap()) 


class UnifiedSpotifyPill(QWidget):
    def __init__(self, sp): 
        super().__init__()
        
        self.sp = sp 
        self.track_id = None
        self.cover_url = None
        self.cover = None 
        self.title = "Loading..."
        self.artist = "Initializing Spotipy"
        self.status = "loading"
        
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setFixedSize(280, 70)
        
        self._center_bottom()
        self._start_timer()
        
    def _center_bottom(self):
        screen = QApplication.primaryScreen().availableGeometry()
        self.move((screen.width() - self.width()) // 2, screen.height() - self.height() - 20)

    def _start_timer(self):
        self.timer = QTimer(self)
        self.timer.timeout.connect(self._update)
        self.timer.start(1000) 

    @Slot()
    def _update(self):
        try:
            data = self.sp.current_user_playing_track()
            
            if not data or not data.get("is_playing"):
                self.status = "paused" if data and not data.get("is_playing") else "idle"
                self.title = "Music Paused" if self.status == "paused" else "Nothing playing"
                self.artist = "Spotify Idle"
                self.cover = None
                self.repaint()
                self.timer.start(15000) 
                return

            item = data.get("item")
            
            if not item:
                self.status = "ad"
                self.title = "Ad playing..."
                self.artist = "Waiting for music"
                self.cover = None
                self.repaint()
                self.timer.start(5000) 
                return

            if item["id"] != self.track_id:
                self.track_id = item["id"]
                self.status = "playing"
                self.title = item["name"]
                self.artist = ", ".join([a["name"] for a in item["artists"]])
                
                url = item["album"]["images"][-1]["url"]
                if url != self.cover_url:
                    self.cover_url = url
                    self._load_cover(url)
                else:
                    self.repaint()

            progress_ms = data.get("progress_ms", 0)
            duration_ms = item.get("duration_ms", 300000)
            remaining_ms = max(duration_ms - progress_ms, 5000)
            
            next_update_delay = min(remaining_ms + 500, 15000)
            self.timer.start(next_update_delay)
            self.repaint() 

        except spotipy.exceptions.SpotifyException as e:
            self.status = "error"
            self.title = "Re-auth Needed"
            self.artist = "Please restart the app"
            self.cover = None
            self.repaint()
            print(f"Spotify API Error: {e}")
            self.timer.start(30000) 
        except requests.exceptions.Timeout:
            print("Spotify API timed out, retrying in 10s...")
            self.timer.start(10000)
        except Exception as e:
            print(f"General Spotify update error: {e}")
            self.timer.start(15000)

    def _load_cover(self, url):
        self.cover_loader_thread = CoverLoader(url)
        self.cover_loader_thread.image_loaded.connect(self._set_cover_pixmap)
        self.cover_loader_thread.start()

    @Slot(QPixmap)
    def _set_cover_pixmap(self, pixmap):
        if not pixmap.isNull():
            self.cover = pixmap.scaled(QSize(60, 60), Qt.KeepAspectRatioByExpanding, Qt.SmoothTransformation)
            self.repaint()
        else:
            self.cover = None
            self.repaint()


    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        rect = self.rect()
        
        painter.setBrush(QColor("#101010"))
        painter.setPen(QColor("#484848"))
        painter.drawRoundedRect(rect, 22, 22)

        if self.cover and not self.cover.isNull():
            cover_rect = QRectF(8, 8, 54, 54)
            path = QPainterPath()
            path.addRoundedRect(cover_rect, 14, 14)
            painter.save()
            painter.setClipPath(path)
            
            source_x = (self.cover.width() - 54) // 2
            source_y = (self.cover.height() - 54) // 2
            painter.drawPixmap(
                int(cover_rect.x()),
                int(cover_rect.y()),
                int(cover_rect.width()),
                int(cover_rect.height()),
                self.cover,
                source_x,
                source_y,
                54, 54
            )
            painter.restore()
        else:
            painter.setPen(QColor("#EEEEEE"))
            painter.setFont(QFont("Segoe UI Emoji", 30)) 
            
            emoji = "🎶"
            if self.status == "ad":
                emoji = "📢" 
            elif self.status == "paused":
                emoji = "⏸️"
            elif self.status == "idle":
                emoji = "🌙"
            elif self.status == "error":
                emoji = "⚠️"
            
            painter.drawText(8, 46, emoji) 

        text_x = 70
        painter.setFont(QFont("Space Grotesk", 13, QFont.Bold))
        
        if self.status in ["error", "ad"]:
            painter.setPen(QColor("#FF4500")) 
        elif self.status == "paused":
            painter.setPen(QColor("#FFFF00")) 
        else:
            painter.setPen(QColor("#FFFFFF")) 

        metrics = painter.fontMetrics()
        title = metrics.elidedText(self.title, Qt.ElideRight, 170)
        painter.drawText(text_x, 32, title)

        painter.setFont(QFont("Inter", 10))
        painter.setPen(QColor("#B3B3B3")) 
        painter.drawText(text_x, 52, self.artist if self.artist else "")
