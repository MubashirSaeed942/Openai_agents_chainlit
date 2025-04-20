import os 
from dotenv import load_dotenv
from agents import Agent, AsyncOpenAI, RunConfig, Runner, OpenAIChatCompletionsModel
import chainlit as cl

# Load environment variables from .env file
load_dotenv()

gemini_api_key = os.getenv("GEMINI_API_KEY")

provider = AsyncOpenAI(
    api_key=gemini_api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"

)

model = OpenAIChatCompletionsModel(
     model="gemini-2.0-flash",
     openai_client= provider,
)

run_config = RunConfig(
    model_provider=provider,
    model=model,
    tracing_disabled=True,
)

agent1 = Agent(
    name="Poetry Agent",
    instructions="An agent that responds in poetry style.",
    
)

@cl.on_chat_start
async def start_chat():
    cl.user_session.set("history", [])
    await cl.Message(
        content="Hello! I am your Poetry Agent. How can I assist you today?",
    ).send()


@cl.on_message
async def handle_message(message: cl.Message):
     history = cl.user_session.get("history")
     history.append({"role": "user", "content": message.content})
     result = await Runner.run(
          agent1,
          input=history,
          run_config=run_config,
     )
     history.append({"role": "assistant", "content": result.final_output})
     cl.user_session.set("history", history)
     await cl.Message(content=result.final_output ).send()