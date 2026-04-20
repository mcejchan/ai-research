import io, os, json
from pathlib import Path
from typing import List, Dict, Optional
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseUpload, MediaIoBaseDownload

SCOPES = ["https://www.googleapis.com/auth/drive"]

class DriveClient:
    def __init__(self):
        # Zkusíme se připojit k Google Drive, pokud selže, použijeme lokální mock
        try:
            if not os.path.exists("client_secret.json"):
                print("⚠️ client_secret.json nenalezen - používám lokální mock místo Google Drive")
                self.service = None
                self.mock_mode = True
                return
            
            creds = None
            if os.path.exists("token.json"):
                creds = Credentials.from_authorized_user_file("token.json", SCOPES)
            if not creds or not creds.valid:
                if creds and creds.expired and creds.refresh_token:
                    creds.refresh(Request())
                else:
                    flow = InstalledAppFlow.from_client_secrets_file("client_secret.json", SCOPES)
                    creds = flow.run_local_server(port=0)
                with open("token.json", "w") as token:
                    token.write(creds.to_json())
            self.service = build("drive", "v3", credentials=creds)
            self.mock_mode = False
        except Exception as e:
            print(f"⚠️ Google Drive nedostupný ({e}) - používám lokální mock")
            self.service = None
            self.mock_mode = True

    def _find_child(self, parent_id: str, name: str) -> Optional[str]:
        if self.mock_mode:
            return None  # V mock módu vždy nevím o existujících souborech
        q = f"'{parent_id}' in parents and name = '{name}' and trashed = false"
        res = self.service.files().list(q=q, fields="files(id,name)").execute()
        files = res.get("files", [])
        return files[0]["id"] if files else None

    def _create_folder(self, name: str, parent_id: str) -> str:
        if self.mock_mode:
            return f"mock_folder_{name}_{parent_id}"
        file_metadata = {"name": name, "mimeType": "application/vnd.google-apps.folder", "parents": [parent_id]}
        f = self.service.files().create(body=file_metadata, fields="id").execute()
        return f["id"]

    def ensure_path(self, parts: List[str], root_id: str) -> str:
        if self.mock_mode:
            # Prefer konfigurovatelný lokální kořen; fallback na repo/local-knowledge-base
            base_root = os.environ.get("LOCAL_KB_ROOT")
            if not base_root:
                # Pokud root_id vypadá jako cesta, použijeme ji, jinak default
                base_root = root_id if any(sep in str(root_id) for sep in (os.sep, "/")) else "local-knowledge-base"
            base_path = Path(base_root)
            if not base_path.is_absolute():
                repo_root = Path(__file__).resolve().parents[2]
                base_path = (repo_root / base_path).resolve()

            path = base_path.joinpath(*parts)
            path.mkdir(parents=True, exist_ok=True)
            print(f"📁 Vytvořena lokální složka: {path}")
            return str(path)
        
        current = root_id
        for p in parts:
            child = self._find_child(current, p)
            if not child:
                child = self._create_folder(p, current)
            current = child
        return current

    def upload_string(self, data: str, name: str, parent_id: str):
        if self.mock_mode:
            # Uložíme lokálně
            if os.path.isdir(parent_id):  # lokální cesta
                filepath = os.path.join(parent_id, name)
            else:
                # parent_id může být cesta, kterou ještě potřebujeme vytvořit
                os.makedirs(parent_id, exist_ok=True)
                filepath = os.path.join(parent_id, name)
            os.makedirs(os.path.dirname(filepath), exist_ok=True)
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(data)
            print(f"💾 Uloženo lokálně: {filepath}")
            return
            
        media = MediaIoBaseUpload(io.BytesIO(data.encode("utf-8")), mimetype="text/plain")
        file_metadata = {"name": name, "parents": [parent_id]}
        self.service.files().create(body=file_metadata, media_body=media, fields="id").execute()

    def delete_file(self, filename: str, parent_id: str):
        if self.mock_mode:
            # Smazat lokální soubor
            if os.path.isdir(parent_id):  # lokální cesta
                filepath = os.path.join(parent_id, filename)
            else:
                filepath = os.path.join(parent_id, filename)
            
            if os.path.exists(filepath):
                os.remove(filepath)
                print(f"🗑️ Smazán lokální soubor: {filepath}")
            return
            
        # Google Drive implementace
        file_id = self._find_child(parent_id, filename)
        if file_id:
            self.service.files().delete(fileId=file_id).execute()
            print(f"🗑️ Smazán soubor z Google Drive: {filename}")
