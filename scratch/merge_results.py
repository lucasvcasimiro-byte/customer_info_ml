import json
import os
import sys

sys.stdout.reconfigure(encoding='utf-8')

# Paths
V1_PATH = "scratch/scraping_results_v1.json"
SPECIALTY_PATH = "scratch/specialty_results.json"
TODO_PATH = "scratch/specialty_todo.json"
OUTPUT_PATH = "scratch/final_products.json"

def main():
    if not os.path.exists(V1_PATH):
        print(f"Error: {V1_PATH} not found!")
        return
        
    # Load raw direct scraping results
    with open(V1_PATH, "r", encoding="utf-8") as f:
        v1_data = json.load(f)
        
    found_grocery = v1_data.get("found", [])
    
    # Load the 36 items we wanted to replace
    if not os.path.exists(TODO_PATH):
        print(f"Error: {TODO_PATH} not found!")
        return
    with open(TODO_PATH, "r", encoding="utf-8") as f:
        todo_list = json.load(f)
    specialty_keys = {item["en"] for item in todo_list}
    
    # Filter out any of these 36 items from found_grocery
    cleaned_grocery = [item for item in found_grocery if item["product_name"] not in specialty_keys]
    
    print(f"Initial grocery matches: {len(found_grocery)}")
    print(f"Cleaned grocery matches: {len(cleaned_grocery)}")
    
    # Load specialty search results
    specialty_results = []
    if os.path.exists(SPECIALTY_PATH):
        try:
            with open(SPECIALTY_PATH, "r", encoding="utf-8") as f:
                specialty_results = json.load(f)
            print(f"Loaded {len(specialty_results)} specialty search results.")
        except Exception as e:
            print(f"Error loading {SPECIALTY_PATH}: {e}")
    else:
        print(f"Warning: {SPECIALTY_PATH} not found yet. Merging with empty list.")
        
    # Create a lookup for specialty results
    specialty_map = {}
    for item in specialty_results:
        specialty_map[item["product_name"]] = item
        
    # Combine results
    final_results = []
    
    # List of all target product names from the user request
    all_targets = [
        "airpods", "almonds", "antioxydant juice", "asparagus", "avocado", "babies food", "bacon", 
        "barbecue sauce", "beer", "black beer", "black tea", "blueberries", "bluetooth headphones", 
        "body spray", "bramble", "brownies", "burger sauce", "burgers", "butter", "cake", "candy bars", 
        "canned_tuna", "carrots", "cat food", "catfish", "cauliflower", "cotton buds", "cream", 
        "deodorant", "dessert wine", "dog food", "eggplant", "eggs", "energy bar", "energy drink", 
        "escalope", "extra dark chocolate", "final fantasy xix", "final fantasy xx", "final fantasy xxii", 
        "flax seed", "french fries", "fresh bread", "fresh tuna", "fromage blanc", "frozen smoothie", 
        "frozen vegetables", "gadget for tiktok streaming", "gluten free bar", "grated cheese", 
        "green beans", "green grapes", "green tea", "ground beef", "gums", "half-life 2", "half-life: alyx", 
        "ham", "hand protein bar", "herb & pepper", "honey", "hot dogs", "imac", "ipad", "iphone 10", 
        "ketchup", "laptop", "light cream", "light mayo", "low fat yogurt", "mashed potato", "mayonnaise", 
        "meatballs", "megaman zero", "megaman zero 2", "megaman zero 3", "megaman zero 4", "melons", 
        "metroid fusion", "metroid prime", "milk", "minecraft", "mineral water", "mint", "mint green tea", 
        "muffins", "mushroom cream sauce", "napkins", "nonfat milk", "oatmeal", "oil", "olive oil", 
        "pancakes", "parmesan cheese", "pasta", "pepper", "pet food", "phone car charger", "phone charger", 
        "pickles", "pokemon scarlet", "pokemon shield", "pokemon sword", "pokemon violet", "portal", 
        "portal 2", "protein bar", "ratchet & clank", "ratchet & clank 2", "ratchet & clank 3", "razor", 
        "red wine", "rice", "ring light", "salad", "salmon", "salt", "samsung galaxy 10", "sandwich", 
        "seabass", "shallot", "shampoo", "shower gel", "shrimp", "soda", "soup", "spaghetti", 
        "sparkling water", "spinach", "strawberries", "strong cheese", "tea", "toilet paper", 
        "tomato juice", "tomato sauce", "tomatoes", "tooth brush", "toothpaste", "trout", "turkey", 
        "vacuum cleaner", "vegetables mix", "water spray", "white wine", "whole weat flour", 
        "whole wheat pasta", "whole wheat rice", "yams", "yogurt cake", "zucchini"
    ]
    
    # Index grocery results
    grocery_map = {item["product_name"]: item for item in cleaned_grocery}
    
    missing_count = 0
    for name in all_targets:
        if name in specialty_map:
            spec = specialty_map[name]
            final_results.append({
                "product_name": name,
                "search_source": spec["search_source"],
                "product_page": spec["product_page"],
                "image_url": spec["image_url"]
            })
        elif name in grocery_map:
            groc = grocery_map[name]
            final_results.append({
                "product_name": name,
                "search_source": groc["search_source"],
                "product_page": groc["product_page"],
                "image_url": groc["image_url"]
            })
        else:
            print(f"Warning: {name} has no match in either grocery or specialty!")
            missing_count += 1
            # Put placeholder or check if we can query it
            final_results.append({
                "product_name": name,
                "search_source": "missing",
                "product_page": "",
                "image_url": ""
            })
            
    print(f"\nTotal merged products: {len(final_results)}")
    print(f"Missing products: {missing_count}")
    
    # Save final JSON
    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        json.dump(final_results, f, ensure_ascii=False, indent=2)
    print(f"Successfully saved merged results to {OUTPUT_PATH}")

if __name__ == "__main__":
    main()
