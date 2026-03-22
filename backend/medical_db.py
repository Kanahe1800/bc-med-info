from search_med import search
from summarize_monograph import summarize_monograph
from search_monograph import din_to_monograph


def final_search_din(query: str):
    try:
        trimmed_query = str(int(query))
        results = search(trimmed_query)
    except ValueError:
        results = search(query)
        
    # print(results)
    return results
    
    
def final_monograph(results: dict):
    if len(results["DIN"]) == 1:
        din = results["DIN"][0]
        din = din.zfill(8)
        print(din)
        
        monograph = din_to_monograph(din)
        summary = summarize_monograph(monograph["pdf_url"])
        # print(summary)
        print(f"PDF size: {len(monograph['pdf_b64'])} chars (base64)")
        
        return summary
        

query = "Ibuprofen"
results = final_search_din(query)
print(results)

# monograph = final_monograph(results)
# print(monograph)


