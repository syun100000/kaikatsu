import datetime
import pytz

'''
このクラスは料金を計算するクラスです。
利用者情報と店舗情報を設定することで料金を計算します。
料金の計算はcalculateメソッドを呼び出すことで行います。
'''
class Fee:
    def __init__(self):
        self.custom_fee = 0
        self.detail = {}
    #利用者情報を設定
    def set_user_info(self, age:int, student_discount:bool, duration:int, checkin_time:str):
        # 年齢を設定
        self.age = int(age)
        # もし0から150以外の年齢が入力された場合、エラーを返す
        if self.age < 0 or self.age > 150:
            raise ValueError("年齢は0から150までの整数を入力してください")
        # 学割を設定 (True or False)
        self.student_discount = student_discount
        #利用時間を設定
        #形式はMM
        self.duration = int(duration)
        if self.duration < 0 or self.duration > 1440:
            raise ValueError("利用時間は0から1440までの整数を入力してください")
        #入店時間を設定
        # 形式は"HH:MM"
        self.checkin_time = checkin_time
        # print(f"入力された利用時間:{self.duration}分")
    # カスタム料金を設定
    def set_custom_fee(self, custom_fee):
        self.custom_fee = custom_fee

    # 店舗情報を設定
    def set_store_info(self, first_30min_fee, every_10min_fee, pack_fees, 
                       night_8hr_fee=None,night_8hr_fee_starrt=20,night_8hr_fee_end=4,
                       night_12hr_fee=None,night_12hr_fee_starrt=20,night_12hr_fee_end=4,
                       holiday_fee_amount=0):
        # 休日料金の加算
        for i in range(len(pack_fees)):
            pack_fees[i] += holiday_fee_amount
        if night_8hr_fee != None:
            night_8hr_fee += holiday_fee_amount
        if night_12hr_fee != None:
            night_12hr_fee += holiday_fee_amount
        self.store_info = {
            'first_30min_fee': first_30min_fee,
            'every_10min_fee': every_10min_fee,
            'pack_fees': pack_fees,
            'night_8hr_fee': night_8hr_fee,
            'night_8hr_fee_starrt':night_8hr_fee_starrt,
            'night_8hr_fee_end':night_8hr_fee_end,
            'night_12hr_fee':night_12hr_fee,
            'night_12hr_fee_starrt':night_12hr_fee_starrt,
            'night_12hr_fee_end':night_12hr_fee_end,
        }
    # 料金を計算する関数
    def calculate(self,temp_duration=None) -> int:
        # temp_durationは利用時間を指定する。Noneの場合は利用時間はself.durationを使用する
        # 前回の料金明細を削除するために初期化
        self.detail = {}
        #calculate_fee_by_time用にdurationを更新
        temp = None
        pack_time =(180,360,540,720,900,1080,1260,1440)
        pack_label =("3時間パック","6時間パック","9時間パック","12時間パック","15時間パック","18時間パック","21時間パック","24時間パック")
        if temp_duration != None:
            # あとで元に戻すために保存
            temp = self.duration
            self.duration = temp_duration
        # print(f"利用時間:{self.duration}分")
        # 料金を初期化
        fee = 0
        # 店舗情報から各パラメータを取得
        first_30min_fee = self.store_info['first_30min_fee']
        every_10min_fee = self.store_info['every_10min_fee']
        pack_fees = self.store_info['pack_fees']
        night_8hr_fee = self.store_info['night_8hr_fee']
        night_8hr_fee_starrt = self.store_info['night_8hr_fee_starrt']
        night_8hr_fee_end = self.store_info['night_8hr_fee_end']
        night_12hr_fee = self.store_info['night_12hr_fee']
        night_12hr_fee_starrt = self.store_info['night_12hr_fee_starrt']
        night_12hr_fee_end = self.store_info['night_12hr_fee_end']
        # 12歳以下または2分以下の滞在時間は無料
        if self.age <= 12:
            fee = 0
            self.detail["小学生以下は無料"] = 0
        elif self.duration <= 2:
            fee = 0
            self.detail["2分以下は無料"] = 0
        else:
            # チェックイン時間から夜間パックの可用性を確認
            checkin_hour = int(self.checkin_time.split(':')[0])
            # 夜間パックの可用性を確認
            if night_8hr_fee != None:
                night8hr_pack_available = checkin_hour >= night_8hr_fee_starrt or checkin_hour < night_8hr_fee_end
            else:
                night8hr_pack_available = False
            if night_12hr_fee != None:
                night12hr_pack_available = checkin_hour >= night_12hr_fee_starrt or checkin_hour < night_12hr_fee_end
            else:
                night12hr_pack_available = False
            # 最初の30分は30分料金
            regular_fee = first_30min_fee
            # 残りの時間を計算
            remaining_duration = self.duration - 30
            every_10min_fee_count = 0
            while remaining_duration > 0:
                # 10分ごとに10分料金を追加
                regular_fee += every_10min_fee
                remaining_duration -= 10
                every_10min_fee_count += 1
            # パック料金を計算
            for pack_index, pack_fee in enumerate(pack_fees):
                if self.duration <= pack_time[pack_index]:
                    fee = pack_fee
                    break
            #　通常料金とパック料金のうち、小さい方を選択
            # fee = min(fee, regular_fee)
            if fee > regular_fee:
                fee = regular_fee
                self.detail["基本料金30分"] = first_30min_fee
                self.detail[f"10分料金({every_10min_fee}円)×{every_10min_fee_count}"] = every_10min_fee_count * every_10min_fee
            elif fee < regular_fee:
                self.detail[pack_label[pack_index]] = pack_fees[pack_index]
            #３時間パック以上の場合の処理
            if pack_index > 0:
                #　次のパック料金を適用するのではなくて前回のパック料金に10分料金を加算した方が安い場合、前回のパック料金に10分料金を加算
                #まず残り時間を計算
                remaining_duration = self.duration - pack_time[pack_index-1]
                temp_fee = pack_fees[pack_index-1]
                every_10min_fee_count = 0
                while remaining_duration > 0:
                    # 10分ごとに10分料金を追加
                    temp_fee += every_10min_fee
                    remaining_duration -= 10
                    every_10min_fee_count += 1
                #前回のパック料金に10分料金を加算した方が安い場合、前回のパック料金に10分料金を加算
                if temp_fee < fee:
                    fee = temp_fee
                    pack_index -= 1
                    # 今ままでの料金明細を削除
                    self.detail = {}
                    #パック料金をdetailに追加
                    self.detail[pack_label[pack_index]] = pack_fees[pack_index]
                    #10分料金をdetailに追加
                    self.detail[f"10分料金×{every_10min_fee_count}"] = every_10min_fee_count * every_10min_fee
                    
                    
            # 夜間パックが利用可能で8時間以内の場合、夜間パック料金も考慮
            if night8hr_pack_available and self.duration <= 480:
                # fee = min(fee, night_8hr_fee)
                if night_8hr_fee < fee:
                    fee = night_8hr_fee
                    #　今ままでの料金明細を削除
                    self.detail = {}
                    self.detail["ナイト8時間パック"] = night_8hr_fee
            #もしかしたら、８時間パックに10分料金を加算した方が安い場合があるかもしれない
            if night8hr_pack_available and self.duration > 480:
                #まず残り時間を計算
                remaining_duration = self.duration - 480
                temp_fee = night_8hr_fee
                night_8hr_fee_count = 0
                while remaining_duration > 0:
                    # 10分ごとに10分料金を追加
                    temp_fee += every_10min_fee
                    remaining_duration -= 10
                    night_8hr_fee_count += 1
                #前回のパック料金に10分料金を加算した方が安い場合、前回のパック料金に10分料金を加算
                if temp_fee < fee:
                    #　今ままでの料金明細を削除
                    self.detail = {}
                    self.detail["ナイト8時間パック"] = night_8hr_fee
                    self.detail[f"10分料金({every_10min_fee}円)×{night_8hr_fee_count}"] = night_8hr_fee_count * every_10min_fee
                    fee = temp_fee
            
            # 夜間パックが利用可能で12時間以内の場合、夜間パック料金も考慮
            if night12hr_pack_available and self.duration <= 720:
                # fee = min(fee, night_12hr_fee)
                if night_12hr_fee < fee:
                    fee = night_12hr_fee
                    #　今ままでの料金明細を削除
                    self.detail = {}
                    self.detail["ナイト12時間パック"] = night_12hr_fee
            #もしかしたら、12時間パックに10分料金を加算した方が安い場合があるかもしれない
            if night12hr_pack_available and self.duration > 720:
                #まず残り時間を計算
                remaining_duration = self.duration - 720
                temp_fee = night_12hr_fee
                night_12hr_fee_count = 0
                while remaining_duration > 0:
                    # 10分ごとに10分料金を追加
                    temp_fee += every_10min_fee
                    remaining_duration -= 10
                    night_12hr_fee_count += 1
                #前回のパック料金に10分料金を加算した方が安い場合、前回のパック料金に10分料金を加算
                if temp_fee < fee:
                    fee = temp_fee
                    #　今ままでの料金明細を削除
                    self.detail = {}
                    self.detail["ナイト12時間パック"] = night_12hr_fee
                    self.detail[f"10分料金({every_10min_fee}円)×{night_12hr_fee_count}"] = night_12hr_fee_count * every_10min_fee
                    
            
            # 学割またはシニア割を適用
            if self.student_discount:
                # 学割を20%割引
                self.detail["学割20%割引"] = int(f"-{int(fee * 0.2)}")
                fee = int(fee * 0.8)

            elif self.age >= 60:
                # シニア割を10%割引
                self.detail["65歳以上10%割引"] = int(f"-{int(fee * 0.1)}")
                fee = int(fee * 0.9)

        # カスタム料金を追加
        fee += self.custom_fee
        if self.custom_fee != 0:
            self.detail["カスタム料金（食事など）"] = self.custom_fee
        #durationを元に戻す
        if temp_duration != None:
            self.duration = temp
        #デバッグ用 変数をすべて表示
        # print(f"パック料金:{pack_fees}円")
        # print(f"料金:{fee}円")
        self.detail["合計"] = fee
        # 料金明細のすべの値を1000円以上はカンマ区切りにする
        for key in self.detail.keys():
            if self.detail[key] >= 1000 or self.detail[key] <= -1000:
                self.detail[key] = f"{self.detail[key]:,}"
        
        return int(fee)
    # 0から24時間までの料金を計算する関数
    def calculate_fee_by_time(self,time_show=True) -> dict:
        fee_list = {}
        for i in range(145):
            i *= 10
            # iを時間に変換
            h_, m_ = divmod(i, 60)
            #　チェックイン時間からの経過時間を計算
            checkin_time_mm = int(self.checkin_time.split(':')[0]) * 60 + int(self.checkin_time.split(':')[1])
            # 経過時間を加算
            checkin_time_mm += i
            # 24時間を超えた場合、24時間を引く
            if checkin_time_mm >= 1440:
                checkin_time_mm -= 1440
            # 経過時間を時間と分に変換
            h, m = divmod(checkin_time_mm, 60)
            # keyを作成
            if time_show == False:
                key = f"{str(h_).zfill(2)}:{str(m_).zfill(2)}"
                valule=self.calculate(temp_duration=i)
                fee_list[key]=valule
            else:
                key = f"{str(h_).zfill(2)}:{str(m_).zfill(2)}"
                key = f"{key}({str(h).zfill(2)}:{str(m).zfill(2)})"
                valule=self.calculate(temp_duration=i)
                fee_list[key]=valule
            # print(f"{key}:{valule}円")
        return fee_list
    
    #現在の料金を計算する関数
    def calculate_now(self) -> int:
        #現在時刻を取得
        now = datetime.datetime.now(pytz.timezone('Asia/Tokyo'))
        # print(now)
        checkin_time_mm = int(self.checkin_time.split(':')[0]) * 60 + int(self.checkin_time.split(':')[1])
        #現在時刻を分に変換
        now = now.hour * 60 + now.minute
        #入店時刻から現在時刻までの経過時間を計算
        duration = now - checkin_time_mm
        #もし経過時間が負の数なら日付が昨日なのでそれを考慮
        if duration < 0:
            duration = (1440 - checkin_time_mm) + now
        r =self.calculate(temp_duration=duration)
        # print(f"現在の料金:{r}円")
        return r
    