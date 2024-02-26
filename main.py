import time
import serial
import asyncio
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

# 分鐘
minute = 5
watertime = 0
water = False

# 初始化 Firebase_admin
account_key = "./pocketplanet-AccountKey/serviceAccountKey.json"
cred = credentials.Certificate(account_key)
firebase_admin.initialize_app(cred)
db = firestore.client()

# serial 讀取
socket = serial.Serial("/dev/ttyUSB0", baudrate=9600, timeout=1)


def on_snapshot(doc_snapshot, changes, read_time):
    for doc in doc_snapshot:
        data = doc.to_dict()
        return data


doc_ref = db.collection("Control").document("change")
doc_watch = doc_ref.on_snapshot(on_snapshot)
# watertimer = doc_watch["WaterTimer"]


# 解析 json 格式資料
def parse_data(d):
    data_split = d.split(",")
    data = {}
    for item in data_split:
        try:
            key, value = item.strip().split(":")
            data[key] = value
        except ValueError:
            print(f"Error parsing data item: {item}")
    return data


# 讀取 serial 資料
def serial_read():
    try:
        socket.write("request_data\n".encode())
        reveiced_data = socket.readline().decode().strip()
        if reveiced_data:
            parsed_data = parse_data(reveiced_data)
            print("========= Read Data =========")
            print("Received data:", parsed_data)
            print("=============================")
            return parsed_data
    except Exception as e:
        print("Error reading from serial:", e)
        return None


# 上傳 firestore 資料
async def upload_data_to_firestore(d):
    try:
        # 獲取當前日期
        current_day = time.strftime("%Y%m%d")
        # 使用當前時間作為資料鍵名
        current_time = time.strftime("%H:%M")
        # 取得當前日期的文檔參考
        d["time"] = current_time
        ref = db.collection("data").document(current_day)
        doc = ref.get()
        # 確認文檔是否存在，如果不存在則創建新文檔
        if doc:
            ref.update({"data": firestore.ArrayUnion([d])})
        else:
            ref.set({})
        print("資料成功上傳到 Firestore！")
    except Exception as e:
        print("在 Firestore 中添加資料時出錯：", e)


async def main():
    try:
        while True:
            data = serial_read()
            if data:
                await upload_data_to_firestore(data)
                await asyncio.sleep(60 * minute)
    except KeyboardInterrupt:
        socket.close()


if __name__ == "__main__":
    asyncio.run(main())
