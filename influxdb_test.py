from influxdb import InfluxDBClient


json_body = [
    {
        "measurement": "electric_power",
        "tags": {
            "device_id": "BB12IIMSG-1059010201",
            "location": "Taipei"
        },
        "time": "2017-11-10T23:00:00Z",
        "fields": {
            "W": 50.64
        }
    },
    {
        "measurement": "electric_power",
        "tags": {
            "device_id": "RR72WWBBG-40190123456",
            "location": "U.S.A"
        },
        "time": "2017-11-11T03:00:00Z",
        "fields": {
            "W": 60.88
        }
    }
]

data = [
    {
        "measurement": "Temperature",
        "tags": {
            "topic": "Sensor/Temperature"
        },
        "fields": {
            "tem": 25,
            "aaa": 1,
        }
    }
]

# 寫入influxdb
# 初始化
# client = InfluxDBClient('localhost', 8086, 'root', 'root', 'example')
client = InfluxDBClient('localhost', 8086, 'root', '', 'testdb')

# client.create_database('testdb')
# client.write_points(json_body)

# 寫入數據-未設條件
# client.write_points(data)
# 寫入數據-有設條件
# result = client.query("select * from Temperature where tem=25;")
# if not result:
#     client.write_points(data)

# client.create_database('testdb') # 創建資料庫
client.drop_database('testdb') # 刪除資料庫
# print(client.get_list_database()) # 顯示目前有哪些資料庫

# measurements操作
# print(client.query('show measurements')) # 顯示資料庫中目前有那些 measurement

# 顯示measurement
result = client.query("select * from exchange_rate;")
# print(list(result.get_points()))
for point in result.get_points():
    print(point)
    
# result = client.query("select * from Temperature;")
# # print(list(result.get_points()))
# for point in result.get_points():
#     print(point)
