# roboflow-sample
roboflow GUI detection sample


こちらのモデルを利用してGUI認識できるかのサンプル
https://universe.roboflow.com/huawei-tz75a/gui-detection-uz7l4/model/1?fbclid=IwY2xjawH2ykJleHRuA2FlbQIxMAABHVprYt7beW8aui8Zu4uxkH28Y1AkFt4oBr44OSlHPBjTZLwFHUzVTq93kw_aem_rVSdScd9puaJUfijazLn4w

**RESULT**
![STRAVA](./STRAVA_output_image.png =720x)
![Grab](./Grab_output_image.png =720x)



#  python setup

```bash
> pyenv local 3.11.9 
> echo 3.11.9 > .python_version
> python -V 
Python 3.11.9

python -m venv .venv
source .venv/bin/activate

>pip install roboflow 
```




## About roboflow

https://pypi.org/project/roboflow/

## API_KEY

https://app.roboflow.com/

-> settings -> (menu) API Keys


## API documents

https://docs.roboflow.com/api-reference/introduction


### install

**requirements:**

- Python 3.8


```
pip install roboflow
```

```python
import roboflow

rf = roboflow.Roboflow(api_key="")
```





