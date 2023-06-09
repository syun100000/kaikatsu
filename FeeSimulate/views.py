from django.shortcuts import render
import json
def fee(age, duration, checkin_time, first_30min_fee, every_10min_fee, pack_fees, night_8hr_fee, custom_fee, student_discount):
    fee = 0
    # 12歳以下か2分以内なら無料
    if age <= 12 or duration <= 2:
        fee = 0
    else:
        # チェックイン時間が20時以降か4時以前なら夜パックが使える
        checkin_hour = int(checkin_time.split(':')[0])
        night_pack_available = checkin_hour >= 20 or checkin_hour < 4
        # パックのインデックスを計算
        pack_index = min(int(duration / 180), 7)
        # パック料金を計算
        pack_fee = pack_fees[pack_index]

        # 65歳以上なら10%割引
        if age >= 65:
            pack_fee *= 0.9
        # 学割なら20%割引
        elif student_discount:
            pack_fee *= 0.8

        # 通常料金を計算
        regular_fee = first_30min_fee
        # 30分を引いた残りの時間を10分単位で計算
        remaining_duration = duration - 30
        # 10分単位で料金を加算
        while remaining_duration > 0:
            regular_fee += every_10min_fee
            remaining_duration -= 10

        # パック料金と通常料金の小さい方を適用
        fee = min(pack_fee, regular_fee)

        # 夜パックがある場合は8時間以内ならそちらを適用
        if night_pack_available and duration <= 480:
            fee = min(fee, night_8hr_fee)

    fee+=custom_fee
    return fee
# Create your views here.

def index(request):
    return render(request, "index.html")

def calculateFee(request):
    if request.method == 'GET':
        # Get form data
        age = int(request.GET.get('age'))
        duration = (request.GET.get('duration'))
        checkin_time = request.GET.get('checkin-time')
        first_30min_fee = int(request.GET.get('first-30min-fee'))
        every_10min_fee = int(request.GET.get('every-10min-fee'))
        pack_fees = [
            int(request.GET.get('pack-3hr-fee')),
            int(request.GET.get('pack-6hr-fee')),
            int(request.GET.get('pack-9hr-fee')),
            int(request.GET.get('pack-12hr-fee')),
            int(request.GET.get('pack-15hr-fee')),
            int(request.GET.get('pack-18hr-fee')),
            int(request.GET.get('pack-21hr-fee')),
            int(request.GET.get('pack-24hr-fee'))
        ]
        night_8hr_fee = int(request.GET.get('night-8hr-fee'))
        # カスタム料金
        custom_fee = int(request.GET.get('custom-fee'))
        student_discount = request.GET.get('student-discount')

        h, m = map(int, duration.split(":"))
        duration = h * 60 + m
        print(duration)
        fee_render=fee(age=age, duration=duration, checkin_time=checkin_time, first_30min_fee=first_30min_fee, every_10min_fee=every_10min_fee, pack_fees=pack_fees, night_8hr_fee=night_8hr_fee, custom_fee=custom_fee, student_discount=student_discount)
        print(f"会計金額: {fee_render}円")
        
        print("金額推移情報")
        fee_list = {}
        for i in range(145):
            i *= 10
            # iを時間に変換
            h_, m_ = divmod(i, 60)
            key = f"{str(h_).zfill(2)}:{str(m_).zfill(2)}"
            valule=fee(age=age, duration=i, checkin_time=checkin_time, first_30min_fee=first_30min_fee, every_10min_fee=every_10min_fee, pack_fees=pack_fees, night_8hr_fee=night_8hr_fee, custom_fee=custom_fee, student_discount=student_discount)
            fee_list[key]=valule
            print(f"{key}:{valule}円")
        
        print(fee_list)
            
        return render(request, "calculateFee.html" , {"fee_render": fee_render,"h": h ,"m":m ,"fee_list": fee_list,"fee_list_json": json.dumps(fee_list) })
        # END: be15d9bcejpp


