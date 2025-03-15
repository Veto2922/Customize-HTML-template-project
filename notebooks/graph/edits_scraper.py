from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.output_parsers import PydanticOutputParser
from pydantic import BaseModel, Field
import os
from typing import Optional

os.environ["GOOGLE_API_KEY"] = "AIzaSyAToPaEHdI98hF0zwDXJX9U2PV0xhgrLNM"


llm = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash",
    temperature=0
)


class RecoQuestionResponse(BaseModel):
    response: Optional[str] = Field(description="another question if user wants more edits or if you dont know he wants")
    is_conversation_finished: bool = Field(description="is conversation finished")


parser = PydanticOutputParser(pydantic_object=RecoQuestionResponse)

system_prompt = """
We are developing an intelligent HTML editing app that analyzes HTML code 
and provides personalized editing recommendations through an interactive, 
storytelling-like approach.


Your job is to:

Read and analyze the provided HTML code.
Generate a single-line analysis that feels like storytelling but remains 
informative and precise.
Ask the user one recommendation question based on the analysis, making it
highly relevant to their specific content 
(e.g., names, placeholders, or other dynamic elements).
Process the user’s response and refine your recommendations.
Repeat the process with a new tailored question until the user indicates they 
want to end the conversation.
The interaction should be engaging, clear, and intuitive, ensuring that 
recommendations feel natural and helpful.

{format_instructions}
"""

reco_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", system_prompt),
        MessagesPlaceholder("conversation")
    ]
).partial(
    format_instructions=parser.get_format_instructions()
)


reco_chain = reco_prompt | llm | parser


if __name__ == "__main__":

    with open(r'data\test_html.html', 'r') as f:
        html = f.read()

    res = reco_chain.invoke({
        "conversation": [
            ("user", html)
        ]
    })

    print(res)