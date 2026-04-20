"""Mock classes for OpenAI API"""

class MockOpenAIMessage:
    def __init__(self, content):
        self.content = content

class MockOpenAIChoice:
    def __init__(self, content):
        self.message = MockOpenAIMessage(content)

class MockOpenAIResponse:
    def __init__(self, content):
        self.choices = [MockOpenAIChoice(content)]

class MockEmbeddingData:
    def __init__(self, embedding):
        self.embedding = embedding

class MockEmbeddingResponse:
    def __init__(self, embedding):
        self.data = [MockEmbeddingData(embedding)]

class MockOpenAI:
    def __init__(self, api_key=None, response_content="Mock LLM response", embedding_data=None):
        self.api_key = api_key
        self.response_content = response_content
        self.embedding_data = embedding_data or [0.1, 0.2, 0.3]
    
    @property
    def chat(self):
        return MockOpenAIChatCompletions(self.response_content)
    
    @property
    def embeddings(self):
        return MockOpenAIEmbeddings(self.embedding_data)

class MockOpenAIChatCompletions:
    def __init__(self, response_content):
        self.response_content = response_content
    
    @property  
    def completions(self):
        return self
        
    def create(self, **kwargs):
        return MockOpenAIResponse(self.response_content)

class MockOpenAIEmbeddings:
    def __init__(self, embedding_data):
        self.embedding_data = embedding_data
        
    def create(self, **kwargs):
        return MockEmbeddingResponse(self.embedding_data)