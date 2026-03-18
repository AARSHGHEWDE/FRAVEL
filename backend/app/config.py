from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # LLM (Ollama)
    ollama_model: str = ""  # e.g. "llama3", "mistral", "gemma2"
    ollama_base_url: str = "http://localhost:11434"

    # External APIs
    amadeus_api_key: str = ""
    amadeus_api_secret: str = ""
    openweather_api_key: str = ""
    yelp_api_key: str = ""
    ticketmaster_api_key: str = ""

    # Supabase
    supabase_url: str = ""
    supabase_key: str = ""
    supabase_service_key: str = ""

    # App
    frontend_url: str = "http://localhost:5173"

    model_config = {"env_file": ".env", "env_file_encoding": "utf-8"}


settings = Settings()
