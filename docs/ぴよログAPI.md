# ぴよログAPIについて

## 設定内容の取得

アプリ設定を取得する。

`https://api2.piyolog.com/preference_fetch`

### リクエスト 

#### ヘッダー

|項目|ペイロード|
|--|--|
|メソッド|POST|
|Content-Type|application/json|
|Accept|application/json|
|User-Agent|PiyoLog/505 CFNetwork/1568.200.51 Darwin/24.1.0|
|Accept-Language|ja|
|Accept-Encoding|gzip, deflate, br|

#### ボディ

``` json
{
	"api_version": 2.1000000000000001,
	"user_id": "30C******",
	"client_id": 2,
	"client_token": "e54*********************"
}
```

#### レスポンス

``` json
{
	"status": 200,
	"preference": {
		"date": 1739607042912,
		"temperature_unit": 0,
		"babies": [{
			"color": 0,
			"baby_id": "30C******-1"
		}],
		"capacity_unit": 0,
		"milk_timer_record_mode": 0,
		"weight_unit": 0,
		"id": "30C******-2",
		"icon_theme": 0,
		"length_unit": 0
	},
	"server_version": 28
}
```

## イベントの取得

入力内容を取得する。

`https://api2.piyolog.com/sync`



### リクエスト

#### ヘッダー

|項目|ペイロード|
|--|--|
|メソッド|POST|
|Content-Type|application/json|
|Accept|application/json|
|User-Agent|PiyoLog/505 CFNetwork/1568.200.51 Darwin/24.1.0|
|Accept-Language|ja|
|Accept-Encoding|gzip, deflate, br|

#### ボディ

``` json
{
	"client_token": "e54*********************",
	"app": "PiyoLog for iPhone",
	"api_version": 2.1000000000000001,
	"minor_version": 6808,
	"user_id": "30C******",
	"main_version": 1,
	"client_id": 2
}
```

#### レスポンス

``` json
{"status": 200,
 "user_id": "30C******", 
 "main_version": 1, 
 "minor_version": 6812, 
 "data": {"baby": [], "baby_event": [
            {"user_id": "30C******", "baby_id": "30C******-1", "event_id": "3c3d623b4c462db92975eee12f327ca0", "date": 20250223, "time": "08: 15", "datetime": "20250223 08: 15", "memo": "テスト", "left_time": 0, "right_time": 0, "amount": 2, "value": 0, "image_url": "", "type": 38, "created_at": 1740266246780, "modified_at": 1740267315110, "deleted": True, "main_version": 1, "minor_version": 6810, "datetime2": 1740266100000, "meta": None
            },
            {"user_id": "30C******", "baby_id": "30C******-1", "event_id": "44fa4aef97ace806462d1b826e7f102a", "date": 20250223, "time": "08: 35", "datetime": "20250223 08: 35", "memo": "", "left_time": 0, "right_time": 0, "amount": 0, "value": 0, "image_url": "", "type": 5, "created_at": 1740267322117, "modified_at": 1740267322117, "deleted": False, "main_version": 1, "minor_version": 6811, "datetime2": 1740267300000, "meta": None
            }
        ], "day_log": [
            {"user_id": "30C******", "baby_id": "30C******-1", "date": 20250223, "diary": "this is dialy", "image_url": "", "created_at": 1740267479360, "modified_at": 1740267491134, "deleted": False, "main_version": 1, "minor_version": 6812
            }
        ], 
 "food_record": []
    }, 
 "server_version": 28
}

```

## 全イベントの取得

すべての入力内容を取得する。

`https://api2.piyolog.com/force_sync_to_app`




### リクエスト

#### ヘッダー

``` json
{
	"client_id": 2,
	"client_token": "e54*********************",
	"user_id": "30C******",
	"api_version": 2.1000000000000001
}
```

#### レスポンス

別ファイルに記載
