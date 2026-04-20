"""Mock classes for YouTube Transcript API"""

class MockTranscriptSegment:
    def __init__(self, text, start, duration):
        self.text = text
        self.start = start
        self.duration = duration

class MockTranscript:
    def __init__(self, segments):
        self.segments = segments
    
    def fetch(self):
        return [MockTranscriptSegment(**seg) for seg in self.segments]

class MockYouTubeTranscriptApi:
    def __init__(self, transcript_data=None):
        self.transcript_data = transcript_data or []
        
    def list_transcripts(self, video_id):
        return self
    
    def find_transcript(self, language_codes):
        return MockTranscript(self.transcript_data)
    
    def fetch(self):
        return [MockTranscriptSegment(**seg) for seg in self.transcript_data]