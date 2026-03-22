from backend.search_med import search
from backend.summarize_monograph import summarize_monograph
from backend.search_monograph import din_to_monograph


def final_search_din(query: str):
    try:
        trimmed_query = str(int(query))
        results = search(trimmed_query)
    except ValueError:
        results = search(query)
        
    # print(results)
    return results
    
    
def final_monograph(results: dict):
    if len(results["DIN"]) >= 1:
        din = results["DIN"][0]
        # din = din.zfill(8)
        print(din)
        
        try:
            monograph = din_to_monograph(din)
        except ValueError:
            return "No monograph PDF found for DIN '00000019'"
            
        summary = summarize_monograph(monograph["pdf_url"])
        print(f"PDF size: {len(monograph['pdf_b64'])} chars (base64)")
        
        return summary
        

# query = "02549883"
# results = final_search_din(query)
# print(results)

# monograph = final_monograph(results)
# print(monograph)


