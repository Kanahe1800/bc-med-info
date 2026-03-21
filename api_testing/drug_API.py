import requests

BASE_URL = "https://health-products.canada.ca/api/drug"

def search_by_name(drug_name: str):
    """Search by brand name, return matching drugs with their DINs."""
    url = f"{BASE_URL}/drugproduct/?brandname={drug_name}&lang=en&type=json"
    response = requests.get(url)
    
    if response.status_code != 200:
        print(f"Error: API returned status {response.status_code}")
        return

    data = response.json()
    
    if not data:
        print(f"No results found for drug name: '{drug_name}'")
        return

    print(f"\nFound {len(data)} result(s) for '{drug_name}':\n")
    for drug in data:
        print(f"  Brand Name : {drug.get('brand_name', 'N/A')}")
        print(f"  DIN        : {drug.get('drug_identification_number', 'N/A')}")
        print(f"  Drug Code  : {drug.get('drug_code', 'N/A')}")
        print(f"  Company    : {drug.get('company_name', 'N/A')}")
        print(f"  Status     : (use drug_code to query /status/)")
        print(f"  Last Update: {drug.get('last_update_date', 'N/A')}")
        print("-" * 40)


def search_by_din(din: str):
    """Search by DIN, return matching drug product details."""
    url = f"{BASE_URL}/drugproduct/?din={din}&lang=en&type=json"
    response = requests.get(url)

    if response.status_code != 200:
        print(f"Error: API returned status {response.status_code}")
        return

    data = response.json()

    if not data:
        print(f"No results found for DIN: '{din}'")
        return

    print(f"\nFound {len(data)} result(s) for DIN '{din}':\n")
    for drug in data:
        drug_code = drug.get('drug_code')
        print(f"  Brand Name : {drug.get('brand_name', 'N/A')}")
        print(f"  DIN        : {drug.get('drug_identification_number', 'N/A')}")
        print(f"  Drug Code  : {drug_code}")
        print(f"  Company    : {drug.get('company_name', 'N/A')}")
        print(f"  Last Update: {drug.get('last_update_date', 'N/A')}")

        # Bonus: fetch active ingredients using drug_code
        if drug_code:
            ing_url = f"{BASE_URL}/activeingredient/?id={drug_code}&lang=en&type=json"
            ing_resp = requests.get(ing_url)
            if ing_resp.status_code == 200 and ing_resp.json():
                ingredients = ing_resp.json()
                print(f"  Ingredients:")
                for ing in ingredients:
                    print(f"    - {ing['ingredient_name']} {ing['strength']} {ing['strength_unit']}")
        print("-" * 40)


def main():
    print("=== Health Canada Drug Lookup Tool ===")
    print("1. Search by drug name")
    print("2. Search by DIN")
    choice = input("\nEnter choice (1 or 2): ").strip()

    if choice == "1":
        name = input("Enter drug/brand name (e.g. ADVIL, TYLENOL): ").strip()
        search_by_name(name)
    elif choice == "2":
        din = input("Enter DIN (e.g. 00326925): ").strip()
        search_by_din(din)
    else:
        print("Invalid choice.")

if __name__ == "__main__":
    main()