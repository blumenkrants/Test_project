price = int(56.24)
one = "Цена: "
two = " руб."
def format_price(one, price, two):
  return (str(one) + str(price) + str(two))
display_price = format_price(one, price, two)
print(display_price)