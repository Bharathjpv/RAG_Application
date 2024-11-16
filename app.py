import random
import time

import mesop as me
import mesop.labs as mel

from model import chain


@me.page(
  security_policy=me.SecurityPolicy(
    allowed_iframe_parents=["https://google.github.io"]
  ),
  path="/chat",
  title="RAG chat",
)
def page():
  mel.chat(transform, title="RAG application chat", bot_user="Mesop Bot")


def transform(input: str, history: list[mel.ChatMessage]):
  # for line in random.sample(LINES, random.randint(3, len(LINES) - 1)):
  #   time.sleep(0.3)
    yield chain.invoke({'question': input})
