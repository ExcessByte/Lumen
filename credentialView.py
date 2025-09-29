from PySide6.QtWidgets import QWidget, QLineEdit, QVBoxLayout, QPushButton, QLabel, QMessageBox, QFrame, QSizePolicy
from PySide6.QtCore import Qt, Signal
import keyring
from keyring import errors as keyring_errors

SERVICE_ID = "Spotify-Now-Playing-Widget"
DEFAULT_REDIRECT_URI = "http://127.0.0.1:8888/callback"

class CredentialPopout(QWidget):
    credentials_saved = Signal()
    
    def __init__(self):
        super().__init__()
        
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setFixedSize(400, 500)
        
        self.setup_ui()
        
        self.save_button.clicked.connect(self.save_credentials)

    def setup_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        self.full_frame = QFrame(self)
        self.full_frame.setStyleSheet("""
            background: #101010;
            border-radius: 20px;
            border: 1px solid #323232;
        """)
        main_layout.addWidget(self.full_frame)
        self.setLayout(main_layout)

        self.full_frame.setSizePolicy(
            QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding
        )

        frame_layout = QVBoxLayout(self.full_frame)
        frame_layout.setContentsMargins(20, 20, 20, 20)
        frame_layout.setSpacing(0)

        title_label = QLabel("Please enter your spotify credentials", self.full_frame)
        title_label.setWordWrap(True)
        title_label.setStyleSheet("color: white; font-family: Space Grotesk; font-size: 25px; border: none;")
        frame_layout.addWidget(title_label)
        frame_layout.addSpacing(20)

        client_id_label = QLabel("Client ID:", self.full_frame)
        client_id_label.setStyleSheet("color: white; font-family: Space Grotesk; font-size: 18px; border: none;")
        self.client_id_input = QLineEdit(self.full_frame)
        self.client_id_input.setStyleSheet("background: #151515; color: #CCCCCC; padding: 5px; border: none; border-bottom: 2px solid #323232; border-radius: 0;")
        
        frame_layout.addWidget(client_id_label)
        frame_layout.addSpacing(5)
        frame_layout.addWidget(self.client_id_input)
        
        frame_layout.addStretch(1)

        client_secret_label = QLabel("Client Secret:", self.full_frame)
        client_secret_label.setStyleSheet("color: white; font-family: Space Grotesk; font-size: 18px; border: none;")
        self.client_secret_input = QLineEdit(self.full_frame)
        self.client_secret_input.setStyleSheet("background: #151515; color: #CCCCCC; padding: 5px; border: none; border-bottom: 2px solid #323232; border-radius: 0;")
        
        self.client_secret_input.setEchoMode(QLineEdit.Password) 

        frame_layout.addWidget(client_secret_label)
        frame_layout.addSpacing(5)
        frame_layout.addWidget(self.client_secret_input)
        
        frame_layout.addStretch(1)

        redirect_uri_label = QLabel("Redirect URI:", self.full_frame)
        redirect_uri_label.setStyleSheet("color: white; font-family: Space Grotesk; font-size: 18px; border: none;")
        self.redirect_uri_input = QLineEdit(self.full_frame)
        self.redirect_uri_input.setStyleSheet("background: #151515; color: #CCCCCC; padding: 5px; border: none; border-bottom: 2px solid #323232; border-radius: 0;")
        
        self.redirect_uri_input.setText(DEFAULT_REDIRECT_URI)
        
        frame_layout.addWidget(redirect_uri_label)
        frame_layout.addSpacing(5)
        frame_layout.addWidget(self.redirect_uri_input)
        
        frame_layout.addStretch(1)

        self.save_button = QPushButton("Save Credentials", self.full_frame)
        self.save_button.setStyleSheet("background: #1DB954; color: white; padding: 10px; border-radius: 5px;")
        
        frame_layout.addWidget(self.save_button)

    def save_credentials(self):
        client_id = self.client_id_input.text().strip()
        client_secret = self.client_secret_input.text().strip()
        redirect_uri = self.redirect_uri_input.text().strip()

        if not all([client_id, client_secret, redirect_uri]):
            QMessageBox.warning(self, "Missing Credentials", "Please fill in all three fields.")
            return

        try:
            keyring.set_password(SERVICE_ID, "client_id", client_id)
            keyring.set_password(SERVICE_ID, "client_secret", client_secret)
            keyring.set_password(SERVICE_ID, "redirect_uri", redirect_uri)
            
            QMessageBox.information(self, "Success", "Credentials saved successfully! The application will now attempt to start.")
            
            self.credentials_saved.emit()
            self.close()
            
        except keyring_errors.NoKeyringError:
            QMessageBox.critical(self, "Error", "Keyring service not available. Please install a keyring backend (e.g., `keyrings.cryptfile`).")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"An unexpected error occurred during saving: {e}")
