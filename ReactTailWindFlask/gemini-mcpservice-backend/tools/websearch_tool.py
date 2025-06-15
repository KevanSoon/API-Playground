from duckduckgo_search import DDGS

def perform_web_search(query: str, max_results: int = 5):
    results = []
    
    # Use DuckDuckGo Search
    with DDGS() as ddgs:
        search_results = ddgs.text(query, max_results=max_results)
        
        for result in search_results:
            results.append({
                "title": result.get("title", "No Title"),
                "summary": result.get("body", "No Summary"),
                "href": result.get("href", "No URL")
            })
    
    return {"results": results}
