import funtion

test = funtion.Database()
a = test.get_sql_data(data_list="firstfloor", field="flow")
print(a)
b, c = test.conversion_flow_data(a)
print(c)
print(b)