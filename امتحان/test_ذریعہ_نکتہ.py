import os
import unittest

import pandas as pd
import pandas.testing as pdt
from تقدیر.ذرائع import جسان, سی_اس_وی, دیسات, دیسات_ماھانہ
from எண்ணிக்கை import உரைக்கு

راستہ = os.path.split(__file__)[0]

مسل_جسان_سالانہ = os.path.join(راستہ, 'وسائل/سالانہ.json')
مسل_سی_اس_وی_سالانہ = os.path.join(راستہ, 'وسائل/سالانہ.csv')


class امتحان_ذریعہ_نکتہ(unittest.TestCase):
    @classmethod
    def setUpClass(قسم):

        قسم.سے, قسم.تک = '۲۰۱۳۰۱۰۱', '۲۰۱۳۰۱۰۹'
        پای_جسان = {
            "تاریخ": ["۲۰۱۳۰۱" + دن for دن in ["۰۱", "۰۲", "۰۳", "۰۴", "۰۵", "۰۶", "۰۷", "۰۸", "۰۹"]],
            "شمسی_تابکاری": [12.2, 12.9, 8.3, 4.9, 13.5, 13.5, 10.3, 13.1, 9.1],
            "درجہ_حرارت_زیادہ": [7.8, 2.2, 3.3, 2.8, -1.1, 6.1, 10.0, 9.4, 12.8],
            "درجہ_حرارت_کم": [-14.4, -13.3, -13.3, -10.6, -8.9, -10.6, -10.6, -8.3, -3.9],
            "بارش": [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
        }
        قسم.اعداد = pd.DataFrame(
            پای_جسان, columns=[س for س in پای_جسان if س != 'تاریخ'],
            index=pd.PeriodIndex([உரைக்கு(تا, 'latin') for تا in پای_جسان['تاریخ']], freq='D')
        )
        قسم.اعداد['درجہ_حرارت_اوسط'] = (قسم.اعداد["درجہ_حرارت_زیادہ"] + قسم.اعداد["درجہ_حرارت_کم"]) / 2

        مسل_دیسات = os.path.join(راستہ, 'وسائل/ACNM1301.WTH')
        مسل_جسان = os.path.join(راستہ, 'وسائل/روزانہ.json')
        مسل_سی_اس_وی = os.path.join(راستہ, 'وسائل/روزانہ.csv')

        قسم.جگہ = (34.583, -103.200, 1348)
        تبدل = {'شمسی_تابکاری': 'شمسی تابکاری'}
        قسم.ذرائع = {
            'جسان': جسان(مسل_جسان, *قسم.جگہ, تبدل_ستون=تبدل),
            'پای_جسان': جسان(پای_جسان, *قسم.جگہ),
            'سی_اس_وی': سی_اس_وی(مسل_سی_اس_وی, *قسم.جگہ, تبدل_ستون=تبدل),
            'دیسات': دیسات(مسل_دیسات)
        }

        قسم.خاکے = '۲۔۶'
        قسم.ذرائع_خاکے = {
            'جسان': جسان(مسل_جسان, *قسم.جگہ, خاکے=قسم.خاکے, تبدل_ستون=تبدل),
            'پای_جسان': جسان(پای_جسان, *قسم.جگہ, خاکے=قسم.خاکے),
            'سی_اس_وی': سی_اس_وی(مسل_سی_اس_وی, *قسم.جگہ, خاکے=قسم.خاکے, تبدل_ستون=تبدل),
            'دیسات': دیسات(مسل_دیسات, خاکے=قسم.خاکے)
        }

    def test_کوائف_پانا(خود):
        for نام, ذریعہ in خود.ذرائع.items():
            with خود.subTest(نام):
                pdt.assert_frame_equal(ذریعہ.کوائف_پانا(خود.سے, خود.تک, *خود.جگہ).اعداد, خود.اعداد, check_like=True)

    def test_بلندی_سحی_نہیں(خود):
        for نام, ذریعہ in خود.ذرائع.items():
            with خود.subTest(نام):
                خود.assertIsNone(ذریعہ.کوائف_پانا(خود.سے, خود.تک, *خود.جگہ[:-1], بلندی=-10))

    def test_خاکے_سہی_نہیں(خود):
        for نام, ذریعہ in خود.ذرائع_خاکے.items():
            with خود.subTest(نام):
                خود.assertIsNone(ذریعہ.کوائف_پانا(خود.سے, خود.تک, *خود.جگہ, خاکے='۸۔۰'))

    def testسہی_خاکے_(خود):
        for نام, ذریعہ in خود.ذرائع_خاکے.items():
            with خود.subTest(نام):
                pdt.assert_frame_equal(
                    ذریعہ.کوائف_پانا(خود.سے, خود.تک, *خود.جگہ, خاکے='۲۔۶').اعداد, خود.اعداد, check_like=True
                )


class امتحان_ماہانہ(unittest.TestCase):
    @classmethod
    def setUpClass(قسم):
        مسل_دیسات = os.path.join(راستہ, 'وسائل/ARPE.MTH')
        مسل_جسان = os.path.join(راستہ, 'وسائل/ماہانہ.json')
        مسل_سی_اس_وی = os.path.join(راستہ, 'وسائل/ماہانہ.csv')

        قسم.جگہ = (34.583, -103.200, 1348)
        قسم.ذرائے = {
            'جسان': جسان(مسل_جسان, *قسم.جگہ),
            'سی_اس_وی': سی_اس_وی(مسل_سی_اس_وی, *قسم.جگہ),
            'دیسات': دیسات_ماھانہ(مسل_دیسات, *قسم.جگہ)
        }
        قسم.اعداد = pd.DataFrame(
            {"شمسی_تابکاری": [25.44] * 31 + [23.43] * 28,
             "درجہ_حرارت_زیادہ": [30.47] * 31 + [29.51] * 28,
             "درجہ_حرارت_کم": [16.82] * 31 + [15.96] * 28,
             "بارش": [4.10] * 31 + [1.92] * 28},
            index=pd.period_range('۱۹۳۱۰۱۰۱', '۱۹۳۱۰۲۲۸', freq='D')
        )
        قسم.اعداد['درجہ_حرارت_اوسط'] = (قسم.اعداد["درجہ_حرارت_زیادہ"] + قسم.اعداد["درجہ_حرارت_کم"]) / 2

    def test_کوائف_پانا(خود):
        for نام, ذریعہ in خود.ذرائے.items():
            with خود.subTest(نام):
                pdt.assert_frame_equal(
                    ذریعہ.کوائف_پانا('۱۹۳۱۰۱۰۱', '۱۹۳۱۰۲۲۸', *خود.جگہ).اعداد, خود.اعداد, check_like=True
                )


class امتحان_سالانہ(unittest.TestCase):
    @classmethod
    def setUpClass(قسم):
        مسل_جسان = os.path.join(راستہ, 'وسائل/سالانہ.json')
        مسل_سی_اس_وی = os.path.join(راستہ, 'وسائل/سالانہ.csv')

        قسم.جگہ = (34.583, -103.200, 1348)
        قسم.ذرائے = {
            'جسان': جسان(مسل_جسان, *قسم.جگہ),
            'سی_اس_وی': سی_اس_وی(مسل_سی_اس_وی, *قسم.جگہ),
        }
        قسم.اعداد = pd.DataFrame(
            {"شمسی_تابکاری": [25.44] * 366 + [23.43] * 365,
             "درجہ_حرارت_زیادہ": [30.47] * 366 + [29.51] * 365,
             "درجہ_حرارت_کم": [16.82] * 366 + [15.96] * 365,
             "بارش": [4.10] * 366 + [1.92] * 365
             },
            index=pd.period_range('۲۰۱۲۰۱۰۱', '۲۰۱۳۱۲۳۱', freq='D')
        )
        قسم.اعداد['درجہ_حرارت_اوسط'] = (قسم.اعداد["درجہ_حرارت_زیادہ"] + قسم.اعداد["درجہ_حرارت_کم"]) / 2

    def test_کوائف_پانا(خود):
        for نام, ذریعہ in خود.ذرائے.items():
            with خود.subTest(نام):
                pdt.assert_frame_equal(
                    ذریعہ.کوائف_پانا('۲۰۱۲۰۱۰۱', '۲۰۱۳۱۲۳۱', *خود.جگہ).اعداد, خود.اعداد, check_like=True
                )
