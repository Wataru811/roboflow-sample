import os
import roboflow
from dotenv import load_dotenv
from inference_sdk import InferenceHTTPClient
from PIL import Image, ImageDraw,ImageFont
import requests
from io import BytesIO




# for checking roboflow results

def draw_rectangle_on_image(url, rectangles, output_path="output_image.png"):
    """
    URLから画像をロードし、指定した矩形を描画して保存します。

    Parameters:
    - url (str): 画像のURL。
    - rectangles (list of tuples): 描画する矩形のリスト。各矩形は (x1, y1, x2, y2, color) の形式。
      例: [(50, 50, 150, 150, "red"), (200, 200, 300, 300, "blue")]
    - output_path (str): 保存する画像ファイルのパス。デフォルトは "output_image.png"。
    """
    try:
        # URLから画像をロード
        response = requests.get(url)
        response.raise_for_status()  # HTTPエラーがある場合例外を発生
        img = Image.open(BytesIO(response.content))

        # 描画用オブジェクト作成
        draw = ImageDraw.Draw(img)

        # フォントの設定 (必要に応じてデフォルトフォントを変更)
        try:
            font = ImageFont.truetype("arial.ttf", size=16)  # フォント指定（Arialフォント）
        except IOError:
            font = ImageFont.load_default()  # デフォルトフォントを使用

        # 矩形を描画
        for rect in rectangles:
            x1, y1, x2, y2, color,text = rect
            w = x2 - x1
            h = y2 - y1
            ofsX = w*-0.5   
            ofsY = h*-0.5   
            draw.rectangle([x1+ofsX, y1+ofsY, x2+ofsX, y2+ofsY], outline=color, width=3)

            # テキストを描画 (矩形の左上に配置)
            text_x = x1+ofsX + 5
            text_y = y1+ofsY - 20 if y1+ofsY - 20 > 0 else y1+ofsY + 5  # テキスト位置の調整
            draw.text((text_x, text_y), text, fill=color, font=font)

        # 画像を保存
        img.save(output_path)
        print(f"画像が保存されました: {output_path}")

    except Exception as e:
        print(f"エラーが発生しました: {e}")







"""
inference-sdk のサンプル

https://universe.roboflow.com/huawei-tz75a/gui-detection-uz7l4/model/1?fbclid=IwY2xjawH2ykJleHRuA2FlbQIxMAABHVprYt7beW8aui8Zu4uxkH28Y1AkFt4oBr44OSlHPBjTZLwFHUzVTq93kw_aem_rVSdScd9puaJUfijazLn4w
https://pypi.org/project/inference-sdk/

roboflow inference-sdk は、roboflow のAPIを使って画像の推論を行うためのライブラリです。

return:
```
{
    "inference_id": "c6c13558-b85c-43fe-9f8c-92a2d2b3b84b",
    "time": 0.049768150999625504,
    "image": {
        "width": 955,
        "height": 2048
    },
    "predictions": [
        {
            "x": 280.5,
            "y": 1634,
            "width": 435,
            "height": 68,
            "confidence": 0.953800618648529,
            "class": "Text View",
            "class_id": 6,
            "detection_id": "d9bbd75d-6a30-4dbf-bea9-8238062eda1c"
        },
	...
	]
}
```
"""
load_dotenv('.env.api.local')
API_KEY = os.getenv('ROBOFLOW_KEY')

CLIENT = InferenceHTTPClient(
    api_url="https://detect.roboflow.com",
    #api_key="oVM4qiq0AT0M3VibXoVb"
    api_key=API_KEY
)
img_url = "https://specrc.check-mate.net/view/675954787275029f36ee79b4/675954787275029f36ee79b4_G2.webp"
#img_url = "https://specrc.check-mate.net/view/675954787275029f36ee79b4/675954787275029f36ee79b4_st9.webp"
result = CLIENT.infer(img_url, model_id="gui-detection-uz7l4/3")
print(result)
#json_result = result.json()
#print(json_result)
objCounter={}
for pred in result["predictions"]:
    print(f"Label: {pred['class']}, Confidence: {pred['confidence']}")
    if pred['class'] in objCounter:
        objCounter[pred['class']]+=1
    else:
        objCounter[pred['class']]=1
print(objCounter)
draw_rectangle_on_image(img_url, [(pred["x"], pred["y"], pred["x"] + pred["width"], pred["y"] + pred["height"], "red", pred["class"]) for pred in result["predictions"]])


"""
# roboflow のサンプル

# init Roboflow
load_dotenv('.env.api.local')
API_KEY = os.getenv('ROBOFLOW_KEY')
PROJECT_NAME = "your_project_name"
MODEL_VERSION = "gui-detection-uz7l4/1"


roboflow.login()
rf = roboflow.Roboflow(api_key=API_KEY)

# APIエンドポイント
url = f"https://detect.roboflow.com/{PROJECT_NAME}/{MODEL_VERSION}?api_key={API_KEY}"

# 画像を読み込み
image_path = "./assets/G1.jpg"
with open(image_path, "rb") as image_file:
    image_data = image_file.read()

# リクエスト送信
response = requests.post(url, files={"file": image_data})

# 結果を取得
if response.status_code == 200:
    predictions = response.json()["predictions"]
    for prediction in predictions:
        print(f"Label: {prediction['class']}, Confidence: {prediction['confidence']}")
else:
    print("Error:", response.status_code, response.text)

"""

