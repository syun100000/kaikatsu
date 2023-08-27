このPythonクラス`Fee`は、快活クラブでの利用料金を計算するために設計されています。クラスは多数のメソッドと属性を持っており、以下のように詳細に説明します。
このモジュールを使用したWEBアプリを
https://tools.syun1.com/kaikatsu/
で公開しています。
### 初期化 (`__init__`)
このメソッドで、カスタム料金（`custom_fee`、整数型）と料金の詳細を格納する辞書（`detail`、辞書型）が初期化されます。

### メソッド

#### `set_user_info(age: int, student_discount: bool, duration: int, checkin_time: str)`
- `age` (整数型): 利用者の年齢を設定。
- `student_discount` (ブール型): 学割の有無。Trueであれば学割が適用されます。
- `duration` (整数型): 利用時間を分単位で設定。例えば、2時間30分の場合は`150`と設定。
- `checkin_time` (文字列型): チェックイン時間。"HH:MM"の形式で設定。

#### `set_custom_fee(custom_fee: int)`
- `custom_fee` (整数型): カスタム料金（例：食事代）を設定。

#### `set_store_info(...)`
店舗の料金体系を設定する。各パラメータは以下の通り。
- `first_30min_fee` (整数型): 最初の30分の料金。
- `every_10min_fee` (整数型): 10分ごとの追加料金。
- `pack_fees` (リスト型): パック料金。各時間パックの料金をリストで設定。
- `night_8hr_fee` (整数型 or None): 8時間夜間パックの料金。設定しない場合は`None`。
- `night_12hr_fee` (整数型 or None): 12時間夜間パックの料金。設定しない場合は`None`。
- `holiday_fee_amount` (整数型): 休日料金の加算額。

#### `calculate(tenp_duration=None) -> int`
- `tenp_duration` (整数型 or None): 一時的に設定する利用時間（分）。通常は`None`。
- 戻り値: 計算された料金（整数型）。

#### `calculate_fee_by_time(time_show=True) -> dict`
- `time_show` (ブール型): 時間を表示するかどうか。
- 戻り値: 各時間帯での料金（辞書型）。

#### `calculate_now() -> int`
- 戻り値: 現在の時間に基づいた料金（整数型）。

このクラスを使う際は、まずインスタンスを生成し、`set_user_info`と`set_store_info`で必要な情報を設定します。その後、`calculate`や`calculate_now`を呼び出して料金を計算できます。料金の詳細は`detail`辞書に格納され、後で参照可能です。

以下は、`Fee`クラスを使用して料金を計算する一例です。

```python
# Feeクラスのインスタンスを生成
fee_calculator = Fee()

# 利用者情報を設定（年齢: 25歳, 学割: なし, 利用時間: 2時間30分, チェックイン時間: 14:00）
fee_calculator.set_user_info(25, False, 150, "14:00")

# カスタム料金を設定（食事代など: 500円）
fee_calculator.set_custom_fee(500)

# 店舗情報を設定
# - 最初の30分: 300円
# - 10分ごと: 100円
# - パック料金: [900円（3時間）, 1700円（6時間）]
# - 8時間夜間パック: 2000円（20時から4時）
# - 休日料金加算: 0円
fee_calculator.set_store_info(300, 100, [900, 1700], night_8hr_fee=2000, night_8hr_fee_starrt=20, night_8hr_fee_end=4, holiday_fee_amount=0)

# 料金を計算
total_fee = fee_calculator.calculate()

# 料金と詳細を表示
print("Total Fee:", total_fee, "円")
print("Fee Details:", fee_calculator.detail)

# 現在の料金を計算（時間が進んだと仮定して）
# この機能は実際の時刻に依存するため、この例では実行しない
# current_fee = fee_calculator.calculate_now()
# print("Current Fee:", current_fee, "円")
```

この例では、25歳で学割がなく、2時間30分利用すると仮定しています。また、食事代などのカスタム料金として500円を設定しています。店舗の料金体系も設定しています。

`calculate`メソッドを呼び出すことで、総料金が計算され、`total_fee`に格納されます。また、計算の詳細は`detail`辞書に格納され、後で参照できます。

注: `calculate_now`メソッドは現実の時間に依存するため、この例では使用していません。実際には、このメソッドを呼び出すと現在の料金が計算されます。
