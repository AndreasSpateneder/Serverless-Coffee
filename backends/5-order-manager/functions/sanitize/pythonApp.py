import boto3

def handler(event, context):

  order = event['body']


  valid = True
  drinks = event['menu']['Item']['menu']['L']


  order_drink = order['drink']
  print("order drink: " + str(order_drink))

  result = []


  for item in drinks:
    drink = item['M'].get('drink')
    print(str(drink))
    if drink['S'] == order_drink:
      result.append(drink)

  if len(result) == 0:
    return False

  print(result)

  for modifier in order['modifiers']:
    print(json.dumps(modifier, indent=0))

    allowed_modifiers = result[0]['modifiers']['L']
    present = [allowed_modifiers for allowed_modifiers in allowed_modifiers if modifier in allowed_modifiers['Options']]

    if len(present) == 0:
      valid = False

  print('sanitizeOrder: ', valid)
  # Order and modifiers both exist in the menu
  return valid
