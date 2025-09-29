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

# store_credentials("757db74a554f45189b58ba8974f640ae", "1c025d1cdff44cbeb662b50a217b3a28", "http://127.0.0.1:8888/callback")

USERNAME = "client_secret"

try:
    keyring.delete_password(SERVICE_ID, USERNAME)
    print(f"Successfully deleted the value for '{USERNAME}' from service '{SERVICE_ID}'.")
except keyring.errors.NoPasswordFound:
    # This exception occurs if the value was already deleted or never stored
    print(f"No stored credential found for '{USERNAME}' under service '{SERVICE_ID}'.")
except Exception as e:
    # Handle other potential errors during deletion
    print(f"An error occurred during deletion: {e}")


print(get_credentials())