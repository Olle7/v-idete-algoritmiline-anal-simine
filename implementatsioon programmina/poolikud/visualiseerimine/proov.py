def flatten_list(my_list):
   if my_list == []:
      return my_list
   if isinstance(my_list[0], list):
      return flatten_list(my_list[0]) + flatten_list(my_list[1:])
   return my_list[:1] + flatten_list(my_list[1:])
my_list = [[1,2],[3,4], [90, 11,[23,54,7,[1,2,3]]], [56, 78], [[34,56]]]
print("The list is :")
print(my_list)
print("The list after flattening is : ")
print(flatten_list(my_list))