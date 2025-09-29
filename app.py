import sys
from PySide6.QtWidgets import QApplication, QMessageBox
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import keyring
from credentialView import CredentialPopout, SERVICE_ID 
from widgetView import UnifiedSpotifyPill 

SPOTIFY_SCOPE = "user-read-currently-playing,user-read-playback-state" 

main_window = None 

def start_main_app(app, client_id, client_secret, redirect_uri):
    """Initializes Spotify client and starts the main widget."""
    global main_window
    
    auth_manager = SpotifyOAuth(
        scope=SPOTIFY_SCOPE,
        client_id=client_id,
        client_secret=client_secret,
        redirect_uri=redirect_uri,
        cache_path=f".cache" 
    )
    sp = spotipy.Spotify(auth_manager=auth_manager)
    
    if main_window is not None:
        main_window.close()
        main_window = None

    main_window = UnifiedSpotifyPill(sp)
    main_window.show()

def get_credentials():
    """Retrieves credentials from the keyring."""
    client_id = keyring.get_password(SERVICE_ID, "client_id")
    client_secret = keyring.get_password(SERVICE_ID, "client_secret")
    redirect_uri = keyring.get_password(SERVICE_ID, "redirect_uri")
    return client_id, client_secret, redirect_uri

if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    def initial_startup_attempt(credential_popout_window=None):
        """
        Attempts to start the main Spotify widget. 
        If credentials are missing or Spotify OAuth fails, 
        it displays the credential pop-up.
        """
        client_id, client_secret, redirect_uri = get_credentials()
        
        main_app_started = False
        
        if client_id and client_secret and redirect_uri:
            try:
                if credential_popout_window:
                    credential_popout_window.hide()
                
                start_main_app(app, client_id, client_secret, redirect_uri)
                main_app_started = True
                
            except spotipy.exceptions.SpotifyOauthError:
                QMessageBox.warning(None, "Authentication Required", "Please log in to Spotify via the browser window that just opened, or your saved credentials are invalid.")
                
            except Exception as e:
                QMessageBox.critical(None, "Startup Error", f"An unexpected error occurred during client initialization: {e}")
        
        if not main_app_started:
            
            if credential_popout_window is None:
                popout = CredentialPopout()
                
                popout.credentials_saved.connect(
                    lambda: initial_startup_attempt(popout)
                )
                popout.show()
            
            elif not credential_popout_window.isVisible():
                 credential_popout_window.show()
    
        return main_app_started

    initial_startup_attempt()
        
    sys.exit(app.exec())
