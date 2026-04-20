"""Mock classes for Google Drive API"""

class MockDriveFile:
    def __init__(self, id, name):
        self.id = id
        self.name = name

class MockDriveFiles:
    def __init__(self):
        self.created_files = []
        
    def create(self, body=None, media_body=None, fields=None):
        file_id = f"mock_file_{len(self.created_files)}"
        file_name = body.get('name', 'untitled') if body else 'untitled'
        mock_file = MockDriveFile(file_id, file_name)
        self.created_files.append(mock_file)
        
        # Return an object with execute method like the real API
        class CreateResult:
            def execute(self):
                return {'id': file_id, 'name': file_name}
        
        return CreateResult()
    
    def list(self, q=None, fields=None):
        # Return empty list for simplicity
        return {'files': []}

class MockGoogleDriveService:
    def __init__(self):
        self.files_mock = MockDriveFiles()
        
    def files(self):
        return self.files_mock