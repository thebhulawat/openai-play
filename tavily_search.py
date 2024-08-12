from tavily import TavilyClient

# Step 1. Instantiating your TavilyClient
tavily_c = TavilyClient(api_key="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")

# Step 2. Executing a Q&A search query
answer = tavily_c.qna_search(query="Who is Leo Messi?")

# Step 3. That's it! Your question has been answered!
print(answer)