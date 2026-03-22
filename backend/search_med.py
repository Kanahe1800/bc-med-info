from supabase import create_client
from dotenv import load_dotenv
import os

load_dotenv()

supabase = create_client(
    os.getenv("SUPABASE_URL"),
    os.getenv("SUPABASE_KEY")
)

TABLE = "pharmacare_formulary"
COLS  = '"DIN/PIN", "Brand Nm", "Generic Nm", "Pcare Plan Desc"'


# ── Scoring ────────────────────────────────────────────────────────────────────

def score_match(value: str, query: str) -> int:
    if not value:
        return 0
    v = value.lower()
    q = query.lower().strip()
    if v == q:
        return 3
    if v.startswith(q):
        return 2
    words = q.split()
    return sum(1 for w in words if w in v)


def top_matches(rows, query, field, n=3):
    scored = [(score_match(r.get(field, ""), query), r) for r in rows]
    scored = [(s, r) for s, r in scored if s > 0]
    scored.sort(key=lambda x: x[0], reverse=True)
    return [r for _, r in scored[:n]]


# ── Display ────────────────────────────────────────────────────────────────────

def print_results(rows, matched_on, dictionary, top=False, prnt=False):
    label = f"  Top {len(rows)} match(es)" if top else f"  {len(rows)} result(s) found"
    if prnt:
        print(f"\n  Matched on: {matched_on}")
        print(f"\n  {'DIN/PIN':<12} {'Brand Name':<35} {'Generic Name':<35} {'Coverage'}")
        print("  " + "─" * 105)
    # index = 0
    for r in rows:
        din      = r.get("DIN/PIN")         or "—"
        brand    = r.get("Brand Nm")        or "—"
        generic  = r.get("Generic Nm")      or "—"
        coverage = r.get("Pcare Plan Desc") or "—"
        brand   = brand[:33]   + ".." if len(brand)   > 35 else brand
        generic = generic[:33] + ".." if len(generic) > 35 else generic
        
        if prnt:
            print(f"  {din:<12} {brand:<35} {generic:<35} {coverage}")
        
        din = din.zfill(8)
        dictionary["DIN"].append(din)
        dictionary["Generic Name"].append(generic)
        dictionary["Brand Name"].append(brand)
        dictionary["coverage"].append(coverage)
        
        # index += 1
        
    if prnt:
        print(f"\n{label}.\n")
    
    return dictionary


# ── Waterfall search ───────────────────────────────────────────────────────────

def search(query: str, prnt=False):
    results = {"DIN": [], "Generic Name": [], "Brand Name": [], "coverage": []}
    
    q = query.strip()

    # 1. Try exact DIN match
    res = supabase.table(TABLE).select(COLS).eq('"DIN/PIN"', q).execute()
    if res.data:
        return print_results(res.data, matched_on="DIN/PIN (exact)", dictionary=results, prnt=prnt)

    # 2. Try Generic Name — all words, then broaden
    words = q.split()
    gquery = supabase.table(TABLE).select(COLS).not_.is_('"Generic Nm"', "null")
    for word in words:
        gquery = gquery.ilike('"Generic Nm"', f"%{word}%")
    gres = gquery.execute()

    if not gres.data and len(words) > 1:
        gres = (supabase.table(TABLE).select(COLS)
                .not_.is_('"Generic Nm"', "null")
                .ilike('"Generic Nm"', f"%{words[0]}%")
                .execute())

    best_generic = top_matches(gres.data, q, "Generic Nm", n=3)
    if best_generic:
        return print_results(best_generic, matched_on="Generic Name", dictionary=results, top=True, prnt=prnt)

    # 3. Try Brand Name — all words, then broaden
    bquery = supabase.table(TABLE).select(COLS)
    for word in words:
        bquery = bquery.ilike('"Brand Nm"', f"%{word}%")
    bres = bquery.execute()

    if not bres.data and len(words) > 1:
        bres = (supabase.table(TABLE).select(COLS)
                .ilike('"Brand Nm"', f"%{words[0]}%")
                .execute())

    best_brand = top_matches(bres.data, q, "Brand Nm", n=3)
    if best_brand:
        return print_results(best_brand, matched_on="Brand Name", dictionary=results, top=True, prnt=prnt)

    # 4. Nothing found
    print("\n  No results found for that DIN, Generic Name, or Brand Name.\n")
    return results


# ── Menu ───────────────────────────────────────────────────────────────────────

MENU = """
╔══════════════════════════════════════╗
║     BC PharmaCare Formulary Search   ║
╠══════════════════════════════════════╣
║  Enter a DIN, Generic Name,          ║
║  or Brand Name to search.            ║
║                                      ║
║  0 · Quit                            ║
╚══════════════════════════════════════╝
"""

def main():
    print(MENU)
    while True:
        query = input("  Search: ").strip()

        if query == "0":
            print("\n  Goodbye!\n")
            break
        elif query == "":
            print("\n  Please enter a search term.\n")
        else:
            search(query)

        input("  Press Enter to continue...")
        print(MENU)


if __name__ == "__main__":
    main()