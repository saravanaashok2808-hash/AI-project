try:
    import torch
except ImportError:
    torch = None
import logging
import threading

logger = logging.getLogger(__name__)

class RawLLM:
    def __init__(self, model_id: str = "Qwen/Qwen2.5-1.5B-Instruct"):
        self.model_id = model_id
        self.device = "cuda" if (torch and torch.cuda.is_available()) else "cpu"
        self.tokenizer = None
        self.model = None
        self.is_loaded = False
        self.is_loading = False
        self._lock = threading.Lock()

    def load_model(self):
        """Loads the raw model into GPU memory if available; falls back to instant empathetic engine on CPU."""
        if torch is None or self.device != "cuda":
            logger.info("No CUDA GPU detected. Using instant empathetic helper persona (<5ms response time).")
            self.is_loaded = False
            return False

        with self._lock:
            if self.is_loaded or self.is_loading:
                return self.is_loaded
            self.is_loading = True

        try:
            from transformers import AutoModelForCausalLM, AutoTokenizer
            logger.info(f"Loading {self.model_id} natively on GPU device: {self.device}...")
            
            self.tokenizer = AutoTokenizer.from_pretrained(self.model_id, trust_remote_code=True)
            
            # Use float16 on GPU (ideal for RTX 3050 6GB)
            self.model = AutoModelForCausalLM.from_pretrained(
                self.model_id,
                torch_dtype=torch.float16,
                device_map="auto",
                low_cpu_mem_usage=True,
                trust_remote_code=True
            )
            
            self.is_loaded = True
            logger.info("Raw LLM loaded on GPU successfully!")
            return True
        except Exception as e:
            logger.warning(f"Could not load {self.model_id} into GPU memory ({e}). Empathetic helper engine active.")
            self.is_loaded = False
            return False
        finally:
            self.is_loading = False

    def generate(
        self,
        system_prompt: str,
        user_prompt: str,
        max_new_tokens: int = 512,
        language: str = "English",
        num_schemes: int = 0,
        top_scheme_name: str = "",
        top_scheme_benefit: str = ""
    ) -> str:
        """
        Generates a warm, conversational, human helper voice response.
        If the model is in memory, it uses the raw Qwen transformer with the Arasu Nanban persona.
        If the model is not loaded yet, it produces an empathetic, caring, natural conversational response.
        """
        if self.is_loaded and self.model is not None and self.tokenizer is not None:
            try:
                messages = [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ]
                
                text = self.tokenizer.apply_chat_template(
                    messages,
                    tokenize=False,
                    add_generation_prompt=True
                )
                
                inputs = self.tokenizer([text], return_tensors="pt").to(self.device)
                
                with torch.no_grad():
                    outputs = self.model.generate(
                        **inputs,
                        max_new_tokens=max_new_tokens,
                        temperature=0.4,
                        do_sample=True
                    )
                    
                input_length = inputs.input_ids.shape[1]
                generated_tokens = outputs[0][input_length:]
                response = self.tokenizer.decode(generated_tokens, skip_special_tokens=True)
                return response.strip()
            except Exception as e:
                logger.error(f"Error during transformer generation: {e}. Falling back to empathetic helper voice.")

        # Empathetic Human Companion Voice Persona ("அரசு நண்பன்")
        is_tamil = language.lower() in ["tamil", "ta", "ta-en"]
        if num_schemes > 0:
            if is_tamil:
                scheme_highlight = f"குறிப்பா '{top_scheme_name}' திட்டம்" if top_scheme_name else "பயனுள்ள அரசு திட்டங்கள்"
                benefit_text = f" இதன் மூலமா உங்களுக்கு {top_scheme_benefit} கிடைக்கும்." if top_scheme_benefit else ""
                return (
                    f"வணக்கம்! கவலைப்படாதீங்க, உங்களுக்கு வழிகாட்ட நான் இருக்கேன். "
                    f"உங்க கேள்விக்கு ஏற்ற மாதிரி {scheme_highlight} உங்களுக்கு ரொம்ப உதவியாக இருக்கும்.{benefit_text} "
                    f"மொத்தம் {num_schemes} திட்டங்களை உங்களுக்காக எடுத்து வச்சிருக்கேன். "
                    f"தேவையான ஆவணங்களையும், எப்படி விண்ணப்பிக்கணும்ங்கறதையும் கீழே உள்ள கார்டுகளில் தெளிவா கொடுத்திருக்கேன், பாருங்க! "
                    f"வேற ஏதாச்சும் சந்தேகம் இருந்தா தாராளமா கேளுங்க, நான் விளக்குறேன்!"
                )
            else:
                scheme_highlight = f"especially the '{top_scheme_name}'" if top_scheme_name else "some great options"
                benefit_text = f" It provides {top_scheme_benefit}." if top_scheme_benefit else ""
                return (
                    f"Hello! Don't worry at all, I'm right here to guide you through this. "
                    f"Based on what you shared, {scheme_highlight} is a great match for your situation.{benefit_text} "
                    f"I found {num_schemes} relevant government schemes for you. "
                    f"I've laid out the required documents and step-by-step application process in the cards below. "
                    f"Take a look, and feel free to ask me if you have any doubts!"
                )
        else:
            if is_tamil:
                return (
                    "வணக்கம்! நீங்க கேட்டதுக்கு நேரடியா திட்டங்கள் எதுவும் வரலைங்க. "
                    "கவலைப்படாதீங்க, உங்க தொழில் (விவசாயி, மாணவர், வேலை தேடுபவர்), உங்க வயது அல்லது குடும்ப சூழ்நிலையை கொஞ்சம் சொன்னீங்கன்னா, "
                    "உங்களுக்கு பொருத்தமான திட்டத்தை நான் உடனே கண்டுபிடிச்சு சொல்றேன்!"
                )
            else:
                return (
                    "Hello! I couldn't find a direct scheme for that exact query, but don't worry! "
                    "If you can tell me a bit about yourself—like your age, whether you are a student, farmer, or job seeker—I will "
                    "immediately track down the right welfare schemes for you!"
                )

# Singleton instance
llm_service = RawLLM()
