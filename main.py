import requests

API_KEY = '9385b0c9dc8c43e9b29415cea966a7c1'


def find_recipes_by_ingredients(ingredients, number=10, offset=0):
  url = 'https://api.spoonacular.com/recipes/findByIngredients'
  params = {
    'ingredients': ','.join(ingredients),
    'number': number,
    'offset': offset,
    'limitLicense': True,
    'ranking': 1,
    'ignorePantry': True,
    'apiKey': API_KEY
  }

  try:
    response = requests.get(url, params=params)
    response.raise_for_status()
    recipes = response.json()
    return recipes
  except requests.exceptions.RequestException as e:
    print(f"Error: {e}")
    return None


def get_recipe_instructions(recipe_id):
  url = f'https://api.spoonacular.com/recipes/{recipe_id}/analyzedInstructions'
  params = {'apiKey': API_KEY}

  try:
    response = requests.get(url, params=params)
    response.raise_for_status()
    instructions = response.json()
    return instructions
  except requests.exceptions.RequestException as e:
    print(f"Error: {e}")
    return None


def suggest_additional_ingredients(recipes):
  ingredients_set = set()
  for recipe in recipes:
    for ingredient in recipe['usedIngredients']:
      ingredients_set.add(ingredient['name'])
  return list(ingredients_set)


def display_recipe(recipe):
  print("Recipe:")
  print(f"Title: {recipe['title']}")
  print(f"Image: {recipe['image']}")
  print("Ingredients:")
  for ingredient in recipe['usedIngredients']:
    print(f"- {ingredient['original']}")
  print("Instructions:")

  instructions = get_recipe_instructions(recipe['id'])

  if instructions:
    for step in instructions[0]['steps']:
      print(f"{step['step']}")
  else:
    print("Instructions not available")

  print()


def main():
  ingredients_input = input("Enter comma-separated list of ingredients: ")
  ingredients = [
    ingredient.strip() for ingredient in ingredients_input.split(',')
  ]

  if not ingredients:
    print("Please enter at least one ingredient.")
    return

  while True:
    recipes = find_recipes_by_ingredients(ingredients)

    if recipes:
      suggested_ingredients = suggest_additional_ingredients(recipes)
      if suggested_ingredients:
        print("You might also consider these ingredients:")
        for ingredient in suggested_ingredients:
          print(f"- {ingredient}")
        print()

      recipe_count = len(recipes)
      current_offset = 0
      recipe_index = 0

      while True:
        display_recipe(recipes[recipe_index])

        if recipe_index == recipe_count - 1:
          next_input = input(
            "No more recipes found. Press Enter to exit or 'u' to update ingredients: "
          )
          if next_input == 'u':
            break
          elif next_input:
            return
          else:
            break

        next_input = input(
          "Press Enter to view the next recipe or 'u' to update ingredients, or 'q' to quit: "
        )
        if next_input == 'q':
          return
        elif next_input == 'u':
          break

        recipe_index += 1
        if recipe_index % 10 == 0:
          current_offset += 10
          recipes = find_recipes_by_ingredients(ingredients,
                                                offset=current_offset)
          if not recipes:
            print("Failed to retrieve more recipes. Please try again.")
            return
          recipe_count = len(recipes)
          recipe_index = 0

    else:
      print("No recipes found.")

    update_input = input(
      "Enter updated comma-separated list of ingredients or 'q' to quit: ")
    if update_input == 'q':
      return
    else:
      ingredients = [
        ingredient.strip() for ingredient in update_input.split(',')
      ]


if __name__ == '__main__':
  main()
