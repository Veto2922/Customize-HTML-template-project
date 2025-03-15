from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.output_parsers import StrOutputParser
import os

os.environ["GOOGLE_API_KEY"] = "AIzaSyAToPaEHdI98hF0zwDXJX9U2PV0xhgrLNM"


llm = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash",
    temperature=0
)

system_prompt = """
your job is to extract the edits from the conversation 
that user wants and ignore any thing else .

dont generate html code , just generate a list of points of the edits
like this

1. edit 1
2. edit 2

conversation :

"""

filter_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", system_prompt),
        MessagesPlaceholder("conversation")
    ]
)


filter_chain = filter_prompt | llm | StrOutputParser()


if __name__ == "__main__":

    with open(r'data\test_html.html', 'r') as f:
        html = f.read()

    res = filter_chain.invoke({
        "conversation": [
            ("user", html),
            ("ai", "You can use CSS for that. I suggest adding `text-align: center;` to your `<h1>` style. Do you want me to generate the full CSS rule for you?"),
            ("user", "Yes, do that."),
            ("user", "Yes, apply this edit."),
            ("user", "I need to add padding around my <div> elements."),
            ("ai", "I suggest adding `padding: 20px;` to your `<div>` elements. Would you like a different value?"),
            ("user", "Make it `15px` instead."),
            ("user", "Yes, apply this edit.")
        ]
    })

    print(res)