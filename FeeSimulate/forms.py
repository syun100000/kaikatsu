from django  import forms

class FeeForm(forms.Form):
    age = forms.IntegerField(label="年齢", min_value=0, max_value=150)
    duration = forms.TimeField(label="滞在時間")
    checkin_time = forms.TimeField(label="チェックイン時間")
    first_30min_fee = forms.IntegerField(label="30分までの料金", min_value=0, max_value=10000)
    every_10min_fee = forms.IntegerField(label="10分ごとの追加料金", min_value=0, max_value=10000)
    pack_3hr_fee = forms.IntegerField(label="3時間パック料金", min_value=0, max_value=10000)
    pack_6hr_fee = forms.IntegerField(label="6時間パック料金", min_value=0, max_value=10000)
    pack_9hr_fee = forms.IntegerField(label="9時間パック料金", min_value=0, max_value=10000)
    pack_12hr_fee = forms.IntegerField(label="12時間パック料金", min_value=0, max_value=10000)
    pack_15hr_fee = forms.IntegerField(label="15時間パック料金", min_value=0, max_value=10000)
    pack_18hr_fee = forms.IntegerField(label="18時間パック料金", min_value=0, max_value=10000)
    pack_21hr_fee = forms.IntegerField(label="21時間パック料金", min_value=0, max_value=10000)
    pack_24hr_fee = forms.IntegerField(label="24時間パック料金", min_value=0, max_value=10000)
    night_8hr_fee = forms.IntegerField(label="夜パック料金", min_value=0, max_value=10000)
    # custom_fee = forms.IntegerField(label="カスタム料金", min_value=0, max_value=10000)
    student_discount = forms.BooleanField(label="学割", required=False)