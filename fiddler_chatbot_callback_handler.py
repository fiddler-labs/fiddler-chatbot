import time
from typing import Any, Dict, List, Optional
import uuid as UUID
#import uuid as uuid_g

from langchain_core.callbacks import BaseCallbackHandler
from langchain_core.outputs import LLMResult

from langchain_community.callbacks.utils import import_pandas

# Define constants

# LLMResult keys
TOKEN_USAGE = "token_usage"
TOTAL_TOKENS = "total_tokens"
PROMPT_TOKENS = "prompt_tokens"
COMPLETION_TOKENS = "completion_tokens"
RUN_ID = "run_id"
MODEL_NAME = "model_name"
GOOD = "good"
BAD = "bad"
NEUTRAL = "neutral"
SUCCESS = "success"
FAILURE = "failure"

# Default values
DEFAULT_MAX_TOKEN = 65536
DEFAULT_MAX_DURATION = 120000

# Fiddler specific constants
PROMPT = "prompt"
RESPONSE = "response"
CONTEXT = "context"
DURATION = "duration"
FEEDBACK = "feedback"
LLM_STATUS = "llm_status"

FEEDBACK_POSSIBLE_VALUES = [GOOD, BAD, NEUTRAL]


# First, define custom callback handler implementations
class FiddlerChatbotCallbackHandler(BaseCallbackHandler):
    def __init__(
        self,
        dbconn: object,
        table: str,
    ) -> None:
        """
        Initialize Fiddler Chatbot callback handler.

        Args:
            dbconn: Fiddler URL (e.g. https://demo.fiddler.ai).
                Make sure to include the protocol (http/https).
            table: Fiddler organization id
        """
        super().__init__()
        # Initialize Fiddler client and other necessary properties
        self.dbconn = dbconn
        self.pd = import_pandas()
        self.table = table

        self.run_id_prompts: Dict[UUID, List[str]] = {}
        self.run_id_response: Dict[UUID, List[str]] = {}
        self.run_id_starttime: Dict[UUID, int] = {}

    def on_llm_start(self, serialized: Dict[str, Any], prompts: List[str], **kwargs: Any) -> Any:
        run_id = kwargs[RUN_ID]
        self.run_id_prompts[run_id] = prompts
        self.run_id_starttime[run_id] = int(time.time() * 1000)

    def on_llm_end(self, response: LLMResult, **kwargs: Any) -> None:
        flattened_llmresult = response.flatten()
        run_id = kwargs[RUN_ID]
        duration = int(time.time() * 1000) - self.run_id_starttime[run_id]
        model_name = ""
        token_usage_dict = {}
    

        if isinstance(response.llm_output, dict):
            token_usage_dict = {
                k: v
                for k, v in response.llm_output.items()
                if k in [TOTAL_TOKENS, PROMPT_TOKENS, COMPLETION_TOKENS]
            }
            model_name = response.llm_output.get(MODEL_NAME, "")

        prompt_responses = [
            llmresult.generations[0][0].text for llmresult in flattened_llmresult
        ]

        prompt_count = len(self.run_id_prompts[run_id])
        df = self.pd.DataFrame(
            {
                PROMPT: self.run_id_prompts[run_id],
                RESPONSE: prompt_responses,
                RUN_ID: [str(run_id)] * prompt_count,
                DURATION: [duration] * prompt_count,
                LLM_STATUS: [SUCCESS] * prompt_count,
                MODEL_NAME: [model_name] * prompt_count,
            }
        )

        if token_usage_dict:
            for key, value in token_usage_dict.items():
                df[key] = [value] * prompt_count if isinstance(value, int) else value

        sd = ''
        #st.session_state[UUID] = uuid_g.uuid4()
#         for document in source_docs:
#             for key in document:
#                 value = document.page_content
#                 sd = sd + "  Document:  " + value

#         sd = sd.replace("'","''")

        query = "INSERT INTO fiddlerai.fiddler_chatbot_ledger (row_id, run_id, prompt, response, duration, model_name, completion_tokens, prompt_tokens, total_tokens, ts) \
                 VALUES (?,?,?,?,?,?,?,?,?,toTimestamp(now()))"
        prepared = self.dbconn.prepare(query)
        uuid_capture = str(UUID.uuid4())
        row = df.iloc[0]
        self.dbconn.execute(prepared, (uuid_capture, row[RUN_ID], row[PROMPT], row[RESPONSE], row[DURATION], row[MODEL_NAME], 0, 0, 0 ))
