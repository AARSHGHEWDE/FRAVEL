from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # LLM (Ollama)
    ollama_model: str = ""  # e.g. "llama3", "mistral", "gemma2"
    ollama_base_url: str = "http://localhost:11434"

    # External APIs
    aviationstack_api_key: str = ""
    openweather_api_key: str = ""
    foursquare_api_key: str = ""
    ticketmaster_api_key: str = ""

    # Supabase
    supabase_url: str = ""
    supabase_key: str = ""
    supabase_service_key: str = ""

    # App
    frontend_url: str = "http://localhost:5173"

    model_config = {"env_file": ".env", "env_file_encoding": "utf-8"}


settings = Settings()
