from api import fetch_available_pets
from databese import init_db, save_pet_to_db
# import fetch_available_pets.py databese.py 


def main():
    print("API call started...")
    
    # get function from api.py to fetch available pets
    pets_data = fetch_available_pets()
    print("Initialize database...")
    
    init_db() # Initialize the database and create the table if it doesn't exist
    
    match_count = 1
    # Filtering
    for pet in pets_data:
        name = pet.get("name")
        
        # if the name starts with 'M' (case-insensitive), print the details
        if name and name.upper().startswith('M'):
            category_name = pet.get("category", {}).get("name", "Unknown")
            char_count = len(name)
            
            # CMD output for debugging and verification
            print("{0}".format(match_count))
            print("The {0} {1} has {2} characters".format(category_name, name, char_count))
            
            # Db CALL HERE: save_pet_to_db(pet['id'], name, pet['status'], category_name, char_count)
            # 
            save_pet_to_db(pet['id'], name, pet['status'], category_name, char_count)
            # 
            # 
            
            match_count += 1

if __name__ == "__main__":
    main()
