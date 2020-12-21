#!/usr/bin/env python3

lines = [l.rstrip("\n") for l in open("input.txt") if l != "" and l != "\n"]
#lines = [l.rstrip("\n") for l in open("input_test_1.txt") if l != "" and l != "\n"]
foods = []
for l in lines:
    l_ingredients, l_allergens = l[:-1].split(" (contains ")
    foods += [(l_ingredients.split(" "), l_allergens.split(", "))]

def solve():
    # Our knowledge base:
    index_allergen_to_possible_ingredient = {} # allergen -> ingredients

    # Also list all ingredients.
    all_ingredients = set()
    for (f_ingredients, _) in foods:
        for i in f_ingredients: all_ingredients.add(i)

    # Build initial index_allergen_to_possible_ingredient. We know nothing yet, therefore all_ingredients are possible.
    for (_, f_allergens) in foods:
        for a in f_allergens:
            if a not in index_allergen_to_possible_ingredient:
                index_allergen_to_possible_ingredient[a] = set(all_ingredients)

    # Now go through the list and add knowledge we get from each line to the knowledge base (indexes).
    for (f_ingredients, f_allergens) in foods:
        for a in f_allergens:
            # We know from this line only that this allergen relates to one of the ingredients:
            knowledge_a_to_possible_ingredient = {ingredient for ingredient in f_ingredients}
            # Apply new knowledge to knowledge base.
            # Fancy python set operator comes in handy!
            index_allergen_to_possible_ingredient[a] = index_allergen_to_possible_ingredient[a] & knowledge_a_to_possible_ingredient

    # Part 1
    absolutely_clean_ingredients = set(all_ingredients)
    for a, ingredients in index_allergen_to_possible_ingredient.items():
        for i in ingredients:
            if i in absolutely_clean_ingredients: absolutely_clean_ingredients.remove(i)
    #print("Absolutely clean ingredients:")
    #print(absolutely_clean_ingredients)
    count_appearances_of_any_absolutely_clean_ingredient = 0
    for ingredients, _ in foods:
        for i in ingredients:
            if i in absolutely_clean_ingredients:
                count_appearances_of_any_absolutely_clean_ingredient += 1
    print("Part 1: {}".format(count_appearances_of_any_absolutely_clean_ingredient))

    # Part 2
    # Iterate through the knowledge and use elimination process to derive more knowledge.
    ingredients_we_are_sure_about = set(next(iter(ingredients)) for ingredients in index_allergen_to_possible_ingredient.values() if len(ingredients) == 1)
    while not all(len(possible_ingredients) == 1 for possible_ingredients in index_allergen_to_possible_ingredient.values()):
        for a, ingredients in index_allergen_to_possible_ingredient.items():
            if len(ingredients) != 1:
                # Another application for the fancy python set operators!
                ingredients -= ingredients_we_are_sure_about
                if len(ingredients) == 1:
                    ingredients_we_are_sure_about.add(next(iter(ingredients)))
        #print(index_allergen_to_possible_ingredient)
    final_relations_ingredient_and_allergen = [(next(iter(i)), a) for a, i in index_allergen_to_possible_ingredient.items()]
    canonical_dangerous_ingredient_list = [i for (i, a) in sorted(final_relations_ingredient_and_allergen, key=lambda r: r[1])]
    print("Part 2: {}".format(",".join(canonical_dangerous_ingredient_list)))

solve()
