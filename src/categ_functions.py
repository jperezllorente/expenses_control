def categorization(value):
    for number in range(0, len(categories)):
        for element in categories[number]:
            if element.lower() in value.lower():
                return categories[number][-1]
            else:
                pass

def subcategorization(value):
    for number in range(0, len(subcategories)):
        for element in subcategories[number]:
            if element.lower() in value.lower():
                return subcategories[number][-1]
            else:
                pass

def bizum_categorization():
    date = str(input())
    name = str(input())
    qty = float(input())
    category = str(input())
    subcategory = str(input())
    return move.update_one({'description':{'$regex':name},'date':date,
                                  'quantity':qty},{'$set':{'category':category, 'subcategory': subcategory}})