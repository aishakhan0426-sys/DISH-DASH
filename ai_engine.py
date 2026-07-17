import json
from data_structures import PriorityQueue

class SmartAIEngine:
    def __init__(self):
        self.recipe_database = {}
        self.hash_table = {}
        self.load_database()

    def load_database(self):
        """Loads recipes from JSON using UTF‑8 encoding."""
        db_path = "recipe_db.json"
        try:
            with open(db_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                self.recipe_database = data
                
                for cuisine, meal_types in data.items():
                    for meal_type, recipes in meal_types.items():
                        for recipe in recipes:
                            self.hash_table[recipe["name"].lower()] = recipe
        except (FileNotFoundError, json.JSONDecodeError) as e:
            print(f"Error loading database: {e}")
            # Fallback minimal database
            self.recipe_database = {
                "Desi": {"Main Course": [], "Snacks": [], "Desserts": [], "Drinks": []},
                "Continental": {"Main Course": [], "Snacks": [], "Desserts": [], "Drinks": []},
                "East Asian": {"Main Course": [], "Snacks": [], "Desserts": [], "Drinks": []},
                "South East Asian": {"Snacks": [], "Main Courses": [], "Desserts": [], "Drinks": []},
                "West/Central Asian": {"Snacks": [], "Main Courses": [], "Desserts": [], "Drinks": []},
                "Personal": {"Custom": []}
            }
            self.hash_table = {}

    def _write_database_to_file(self):
        """Write entire database to JSON with UTF‑8 encoding."""
        db_path = "recipe_db.json"
        with open(db_path, "w", encoding="utf-8") as f:
            json.dump(self.recipe_database, f, indent=4, ensure_ascii=False)

    def add_custom_recipe(self, recipe_dict, cuisine="Personal", meal_type="Custom"):
        name_lower = recipe_dict["name"].lower()
        if name_lower in self.hash_table:
            raise ValueError(f"Recipe '{recipe_dict['name']}' already exists. Use update instead.")
        
        self.hash_table[name_lower] = recipe_dict
        
        if cuisine not in self.recipe_database:
            self.recipe_database[cuisine] = {}
        if meal_type not in self.recipe_database[cuisine]:
            self.recipe_database[cuisine][meal_type] = []
        
        self.recipe_database[cuisine][meal_type].append(recipe_dict)
        self._write_database_to_file()

    def update_custom_recipe(self, old_name, new_recipe_dict, cuisine="Personal", meal_type="Custom"):
        old_name_lower = old_name.lower()
        if old_name_lower not in self.hash_table:
            raise ValueError(f"Recipe '{old_name}' not found for update.")
        
        self.delete_custom_recipe(old_name, cuisine, meal_type)
        self.add_custom_recipe(new_recipe_dict, cuisine, meal_type)

    def delete_custom_recipe(self, recipe_name, cuisine="Personal", meal_type="Custom"):
        name_lower = recipe_name.lower()
        if name_lower not in self.hash_table:
            raise ValueError(f"Recipe '{recipe_name}' not found.")
        
        del self.hash_table[name_lower]
        recipes_list = self.recipe_database.get(cuisine, {}).get(meal_type, [])
        self.recipe_database[cuisine][meal_type] = [r for r in recipes_list if r["name"].lower() != name_lower]
        self._write_database_to_file()

    def save_custom_recipe_to_disk(self, recipe_dict, cuisine="Personal", meal_type="Custom"):
        self.add_custom_recipe(recipe_dict, cuisine, meal_type)

    def recommend_pipeline(self, cuisine, meal_type, mode, max_time, input_ingredients):
        pq = PriorityQueue()
        matched_recipes = []
        target_ingredients = [i.strip().lower() for i in input_ingredients if i.strip()] if input_ingredients else []
        
        if cuisine in self.recipe_database and meal_type in self.recipe_database[cuisine]:
            recipes_pool = self.recipe_database[cuisine][meal_type]
            for recipe in recipes_pool:
                score = 10
                if mode == "Time Only" or mode == "Both":
                    if recipe["time"] > max_time:
                        continue
                    score += (max_time - recipe["time"])
                if mode == "Staples Only" or mode == "Both":
                    if target_ingredients:
                        recipe_ings = [ri.lower() for ri in recipe["ingredients"]]
                        matched_count = sum(1 for ti in target_ingredients if ti in " ".join(recipe_ings))
                        if matched_count == 0 and mode == "Staples Only":
                            continue
                        score += (matched_count * 30)
                pq.push(recipe, score)
        
        while not pq.is_empty():
            matched_recipes.append(pq.pop())
        return matched_recipes

    # =========================================================================
    # ENHANCED AI TROUBLESHOOTING - handles hundreds of cooking issues
    # =========================================================================
    def troubleshoot(self, query):
        """Advanced cooking issue solver with extensive keyword matching."""
        q = query.lower().strip()
        
        # ----- BURNT / BURNING -----
        if any(word in q for word in ["burnt", "burn", "burning", "charred", "black", "smoke", "smoky"]):
            if "rice" in q or "pulao" in q or "biryani" in q:
                return "💡 ChefAI Fix: If rice burnt at bottom, immediately remove unburnt rice to another pot. Place a slice of bread or raw potato on top to absorb burnt smell. Do not scrape the burnt crust."
            elif "meat" in q or "chicken" in q or "beef" in q or "mutton" in q:
                return "💡 ChefAI Fix: Transfer meat to a clean pot without scraping burnt bits. Add a cup of water or broth and simmer gently. Finish with fresh herbs or a splash of lemon juice to mask any residual bitterness."
            elif "curry" in q or "gravy" in q:
                return "💡 ChefAI Fix: Immediately pour the unburnt gravy into a new pan. Add a tablespoon of yogurt, cream, or coconut milk and stir. For thick curries, add a small roux (butter+flour) to rebind."
            else:
                return "💡 ChefAI Fix: Immediately transfer the unburnt portion to a fresh pot without scraping the burnt bottom! Simmer with a clean damp cloth under the lid, or stir in a splash of milk/yogurt to absorb smoky smells. For baked goods, scrape off burnt parts and serve with frosting/sauce."

        # ----- RAW SMELL / ODOR (meat, fish, eggs) -----
        if any(word in q for word in ["raw smell", "odor", "smells", "smelling", "stinks", "foul", "fishy", "eggy"]):
            if "fish" in q or "seafood" in q or "prawn" in q or "shrimp" in q:
                return "💡 ChefAI Fix: Soak fish in milk for 20 min before cooking. Add ginger-garlic paste, turmeric, and lemon juice while cooking. For already cooked fish, squeeze fresh lime and garnish with coriander to mask odor."
            elif "egg" in q or "eggy" in q:
                return "💡 ChefAI Fix: Eggy smell often comes from overcooking. Cook eggs on low-medium heat. Add a pinch of black salt (kala namak) or turmeric to mask the smell. For boiled eggs, rinse in cold water immediately."
            elif "meat" in q or "chicken" in q or "mutton" in q or "beef" in q:
                return "💡 ChefAI Fix: Marinate meat with yogurt, ginger-garlic paste, lemon juice, and spices for at least 30 min. While cooking, add a piece of charcoal (dunked in oil and wrapped in foil) to the pot and cover for 5 min to absorb odors."
            else:
                return "💡 ChefAI Fix: Neutralize odors using acidic ingredients (lemon juice, vinegar, tamarind), aromatic spices (cloves, cardamom, cinnamon), or fresh herbs (coriander, mint, parsley). For strong odors, simmer a charcoal disc in the dish."

        # ----- SALTY / EXCESS SALT -----
        if any(word in q for word in ["salty", "too much salt", "excess salt", "sodium", "salty taste"]):
            if "dough" in q or "batter" in q or "flour" in q:
                return "💡 ChefAI Fix: Add more unsalted flour and liquid proportionally. For cookie dough, add extra sugar and flour to balance."
            elif "soup" in q or "sauce" in q or "curry" in q or "gravy" in q or "stew" in q:
                return "💡 ChefAI Fix: Drop a peeled raw potato wedge into the simmering liquid for 15 min, then discard. Or add a teaspoon of sugar, a splash of lemon juice, or extra coconut milk/cream to dilute saltiness."
            elif "rice" in q or "pasta" in q or "noodles" in q:
                return "💡 ChefAI Fix: Rinse the rice/pasta with fresh water, then reheat with unsalted water or broth. Alternatively, cook extra unsalted rice and mix together."
            else:
                return "💡 ChefAI Fix: Dilute solid dishes with unsalted vegetables, boiled potatoes, or plain rice. Add a small amount of sugar, honey, or acid (lemon/vinegar) to mask saltiness. In gravies, add plain yogurt or coconut milk."

        # ----- SWEET / SUGARY -----
        if any(word in q for word in ["sweet", "sugary", "too sweet", "excess sugar", "sweetness"]):
            if "tea" in q or "coffee" in q or "beverage" in q:
                return "💡 ChefAI Fix: Add more hot water or milk to dilute. For iced tea, add ice cubes and a squeeze of lemon."
            elif "curry" in q or "gravy" in q or "sauce" in q:
                return "💡 ChefAI Fix: Balance sweetness by adding salt (a pinch), acid (lemon juice or vinegar), or spicy elements (red chili, black pepper). You can also add tomato puree or yogurt."
            elif "cake" in q or "cookie" in q or "dessert" in q:
                return "💡 ChefAI Fix: Serve with unsweetened whipped cream, fresh fruit, or a dusting of cocoa powder. For cake batter, add a tablespoon of flour and a pinch of salt."
            else:
                return "💡 ChefAI Fix: Counter excess sweetness with sour (lemon juice, vinegar, tamarind), salty, or bitter ingredients. For savoury dishes, add tomato, yogurt, or spices like cumin and coriander."

        # ----- SOUR / TOO MUCH ACID / TANGY -----
        if any(word in q for word in ["sour", "tangy", "too much lemon", "excess vinegar", "acidic", "tamarind"]):
            return "💡 ChefAI Fix: Add a pinch of baking soda (start with 1/4 tsp) to neutralize acid. Or add sugar/honey and a little butter to balance. For curries, stir in coconut milk or cream."

        # ----- BITTER -----
        if "bitter" in q:
            return "💡 ChefAI Fix: Bitter taste often comes from burnt spices or overcooked greens. Add a teaspoon of sugar or honey, plus a splash of cream or coconut milk. For vegetables, blanch before cooking."

        # ----- SPICY / TOO MUCH CHILI -----
        if any(word in q for word in ["spicy", "too much chili", "too hot", "burning sensation", "spice level"]):
            return "💡 ChefAI Fix: Add dairy (yogurt, cream, milk, coconut milk) to neutralize capsaicin. Adding sugar or honey also helps. For soups, add boiled potato chunks to absorb excess spice, then remove."

        # ----- RUNNY / THIN / WATERY -----
        if any(word in q for word in ["runny", "thin", "watery", "liquidy", "too much water"]):
            if "sauce" in q or "gravy" in q or "curry" in q:
                return "💡 ChefAI Fix: Simmer uncovered to reduce liquid. Or make a slurry (1 tbsp cornstarch + 2 tbsp cold water) and stir in. For cream-based sauces, add grated cheese or cream cheese."
            elif "soup" in q:
                return "💡 ChefAI Fix: Mix 2 tbsp cornstarch with 1/2 cup cold water, add slowly while stirring until desired thickness. Alternatively, add pureed vegetables or beaten egg."
            elif "batter" in q or "dough" in q:
                return "💡 ChefAI Fix: Add more flour, breadcrumbs, or ground nuts gradually until correct consistency."
            else:
                return "💡 ChefAI Fix: Thicken by simmering uncovered, adding a roux (butter+flour), cornstarch slurry, or mashed potatoes. For curries, add coconut milk or ground nuts."

        # ----- THICK / GUMMY / PASTY -----
        if any(word in q for word in ["thick", "gummy", "pasty", "gluey", "too thick", "viscous"]):
            return "💡 ChefAI Fix: Thin out by adding warm water, broth, or milk a little at a time until desired consistency. For sauces, add more wine or cream. For rice, add hot water and fluff."

        # ----- DRY / CRUMBLY / TOUGH -----
        if any(word in q for word in ["dry", "dryness", "crumbly", "tough", "hard", "chewy"]):
            if "cake" in q or "cookie" in q:
                return "💡 ChefAI Fix: Brush with simple syrup (sugar+water) or milk. Serve with frosting, custard, or ice cream. Next time, reduce baking time and add an extra egg."
            elif "meat" in q or "chicken" in q:
                return "💡 ChefAI Fix: Add a splash of broth or water and simmer covered on low heat. Or shred the meat and mix with a sauce/gravy. Marinating overnight helps prevent dryness."
            elif "rice" in q:
                return "💡 ChefAI Fix: Sprinkle a few tablespoons of water over rice, cover, and reheat on low. Fluff with a fork. For biryani, add a little warm milk and ghee."
            else:
                return "💡 ChefAI Fix: Add moisture: butter, oil, yogurt, cream, or broth. Cover and rest for 5-10 min. For dough, knead in extra liquid a teaspoon at a time."

        # ----- OILY / GREASY / TOO MUCH OIL -----
        if any(word in q for word in ["oily", "greasy", "too much oil", "fatty", "excess oil"]):
            return "💡 ChefAI Fix: Skim off excess oil with a ladle or absorb with a slice of bread. Add a spoonful of yogurt, tomato puree, or lemon juice to emulsify. For fried foods, drain on paper towel and serve with acidic side (pickle, salsa)."

        # ----- CURDLED / SEPARATED SAUCE -----
        if any(word in q for word in ["curdled", "separated", "split", "broken sauce", "curdle"]):
            return "💡 ChefAI Fix: Remove from heat immediately. Whisk in 1-2 tablespoons of cold cream or a few ice cubes while whisking vigorously. Strain if needed. Next time, temper dairy with hot liquid before adding."

        # ----- LUMPY / CLUMPY BATTER OR SAUCE -----
        if any(word in q for word in ["lumpy", "clumpy", "clumps", "lumps"]):
            return "💡 ChefAI Fix: For sauces, strain through a fine sieve and whisk. For batter, blend in a food processor or add more liquid and whisk vigorously. Next time, sift dry ingredients and add liquid slowly."

        # ----- STICKY DOUGH -----
        if any(word in q for word in ["sticky dough", "dough too sticky", "dough sticking"]):
            return "💡 ChefAI Fix: Add flour 1 tablespoon at a time while kneading until smooth. Lightly oil your hands and surface. Refrigerate dough for 15-30 min to make it less sticky."

        if any(word in q for word in ["cracked", "crack", "split", "cracks"]):
            if "cake" in q or "cheesecake" in q:
                return "💡 ChefAI Fix: Fill cracks with frosting, whipped cream, or fruit glaze. Prevent by not overbaking and cooling slowly in the oven with door ajar."
            elif "pie" in q or "pastry" in q:
                return "💡 ChefAI Fix: Patch cracks with extra dough and brush with egg wash. For baked pie, hide cracks with lattice strips or serve with crumble topping."

        if any(word in q for word in ["didn't rise", "dough not rising", "yeast", "flat bread"]):
            return "💡 ChefAI Fix: Check yeast freshness – use warm liquid (105-115°F) and a pinch of sugar to proof. Let dough rise in a warm, draft‑free place. Add a little baking powder as backup."

        if any(word in q for word in ["undercooked", "raw inside", "not cooked", "still raw"]):
            return "💡 ChefAI Fix: Return to heat and cook covered on low. For meat, finish in oven at 350°F. For baked goods, cover with foil and bake longer at lower temp. For rice, add 2 tbsp water and microwave covered for 2 min."

        if any(word in q for word in ["overcooked", "mushy", "soggy", "too soft"]):
            if "vegetables" in q or "veggies" in q:
                return "💡 ChefAI Fix: Shock in ice water to stop cooking. Use in soups or purees. Next time, cook al dente."
            elif "pasta" in q or "noodles" in q:
                return "💡 ChefAI Fix: Rinse with cold water and toss with olive oil to prevent sticking. Use in baked dishes or salads."
            else:
                return "💡 ChefAI Fix: Slightly mushy dishes can be rescued by adding a crunchy topping (nuts, breadcrumbs, fried onions) or serving with crispy sides."

        return "💡 ChefAI Fix: Please describe your cooking issue using keywords like 'burnt', 'salty', 'sweet', 'runny', 'dry', 'oily', 'curdled', 'lumpy', 'sticky', 'cracked', 'undercooked', 'raw smell', 'spicy', 'sour', 'bitter', 'thick', etc. I'll give you a specific solution!"