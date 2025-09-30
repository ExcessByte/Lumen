# Lumen

**Lumen** is a simple Spotify "Now Playing" widget built using [spotipy](https://spotipy.readthedocs.io/), [PySide6](https://doc.qt.io/qtforpython/), [keyring](https://pypi.org/project/keyring/), and [requests](https://requests.readthedocs.io/). It displays the currently playing music from any device connected to the same Spotify account.

---

## Features
- Displays current music playback from any device on your Spotify account
- Uses spotipy for data fetching
- GUI powered by PySide6
- Credentials securely stored using keyring
- Album art retrieved via requests

---

## Installation
1. Download the ZIP file or clone repo with `git clone https://github.com/ExcessByte/Lumen.git`
2. Extract the contents
3. Run the following command:
   ```bash
   uv run app.py
   ```
   The app will prompt for Spotify credentials (client id, client secret) the first time it runs or if there is an authorization error.

---

## Prerequisites
- Python (recommended version: 3.8+)
- Dependencies:
  - spotipy
  - pyside6
  - keyring
  - requests

---

## Usage Example (Keyring)
```python
import keyring

SERVICE_ID = "Spotify-Now-Playing-Widget"

def store_credentials(client_id, client_secret, redirect_uri):
    keyring.set_password(SERVICE_ID, "client_id", client_id)
    keyring.set_password(SERVICE_ID, "client_secret", client_secret)
    keyring.set_password(SERVICE_ID, "redirect_uri", redirect_uri)

def get_credentials():
    client_id = keyring.get_password(SERVICE_ID, "client_id")
    client_secret = keyring.get_password(SERVICE_ID, "client_secret")
    redirect_uri = keyring.get_password(SERVICE_ID, "redirect_uri")
    return client_id, client_secret, redirect_uri

USERNAME = "client_secret"

try:
    keyring.delete_password(SERVICE_ID, USERNAME)
    print(f"Successfully deleted the value for '{USERNAME}' from service '{SERVICE_ID}'.")
except keyring.errors.NoPasswordFound:
    print(f"No stored credential found for '{USERNAME}' under service '{SERVICE_ID}'.")
except Exception as e:
    print(f"An error occurred during deletion: {e}")

print(get_credentials())
```
---

## Configuration
- Obtain your Spotify Client ID and Client Secret from the [Spotify Developer Dashboard](https://developer.spotify.com/dashboard)
- The app will prompt for these values on first run

---

## Contributing
- Contributions are welcome! Please test your changes beforehand and avoid breaking the code.

---

## License
- This project is open for use. If possible, please attribute to ExcessByte for publicity.
- [Help wanted: Choose a license.]

---

## Contact & Support
- For support or questions, use the links in [my GitHub profile](https://github.com/ExcessByte)

---

## Screenshots
*(To be added)*

---

## Roadmap
*(Leave space for future plans)*

---

## Acknowledgements
*(Leave space for credits or thanks)*
