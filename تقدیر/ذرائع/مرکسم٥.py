import calendar
import os
import re
from datetime import date as تاریخ
from subprocess import run as چلو

import numpy as نمپی
import pandas as پاندس
from pkg_resources import resource_filename as وسائل_کا_نام
from تقدیر import لغت_قابو
from تقدیر.ذرائع.ذریعہ import ذریعہ

مسل_مرکسم = لغت_قابو['مسل_مرکسم']  #
dir_marksim = os.path.join(os.path.split(مسل_مرکسم)[0])
راستہ_اعداد_اع_گر_نم = os.path.join(dir_marksim, 'gcm5data')  # علمی گردش کی نمونہ کا راستہ

#
راستہ_سانچے = وسائل_کا_نام('تقدیر', 'سانچے.CLI')


class مرکسم٥(ذریعہ):
    ممکنہ_تاریخیں = (تاریخ(1, 1, 1), تاریخ(2099, 1, 1))

    def _اعداد_پیدا_کرنا(خود, سے, تک, ر_ح_را, ش_ترکار, پہلہ_ہونےولے_اشتمال):
        """

        :param سے:
        :type سے: تاریخوقت | تاریخ
        :param تک:
        :type تک: تاریخوقت | تاریخ
        :param ر_ح_را: رشتہدار حراستی کے راسبہ
        :type ر_ح_را:
        :param ش_ترکار:
        :type ش_ترکار:
        :param پہلہ_ہونےولے_اشتمال:
        :type پہلہ_ہونےولے_اشتمال:
        :return:
        :rtype:
        """

        پہلا_سال = سے.year
        آخرا_سال = تک.year

        #
        if آخرا_سال < پہلا_سال:
            raise ValueError('پہلا سال اکر سال کے پہلہ ینا ہے.')

        if آخرا_سال > 2099:
            raise ValueError('سال ٢٠١٢ اور ٢٠٩٩ کے بچ میں ہونے پڑتے ہیں.')

        #
        راستہ_موجودہ = os.path.join(dir_marksim, 'CLI_TQDR')

        if not os.path.isdir(راستہ_موجودہ):
            os.makedirs(راستہ_موجودہ)

        with open(راستہ_سانچے) as م:
            سانچے = م.readlines()

        #
        for س, قطار in enumerate(سانچے):
            سانچے[س] = قطار.format(LAT=round(خود.چوڑائی, 1), LONG=round(خود.طول, 1), ELEV=round(خود.بلندی, 1))

        #
        with open(os.path.join(راستہ_موجودہ, 'TQDR.CLI'), 'w') as م:
            م.write(''.join(سانچے))

        متن_ر_ح_را = 'rcp' + str(ر_ح_را).replace('.', '')

        اعداد_دن = پاندس.DataFrame(index=پاندس.date_range(سے, تک), columns=خود.دن_ستون)

        # ہر سال کے لئے...
        for سال in range(پہلا_سال, آخرا_سال + 1):

            if سال < 2013:
                if calendar.isleap(سال):
                    سال_مارکسم = 2016
                else:
                    سال_مارکسم = 2013
            else:
                سال_مارکسم = سال
            #
            if سال < 2013:
                سانچے_نمونہ = '00000000000000000'
            else:
                سانچے_نمونہ = '11111111111111111'

            if ر_ح_را == 0:
                متن_ر_ح_را = 'rcp26'
                سانچے_نمونہ = '00000000000000000'

            مسل_پیداوار_مرکسم = 'TQDR0101.WTG'
            راستہ_پیداوار_مرکسم = os.path.join(راستہ_موجودہ, '_'.join(('TQDR', سانچے_نمونہ, متن_ر_ح_را, str(سال))))

            if پہلہ_ہونےولے_اشتمال and os.path.isdir(راستہ_پیداوار_مرکسم):
                پہلہ_سے_مسلیں = [x for x in os.listdir(راستہ_پیداوار_مرکسم)
                                 if re.match(r'[A-Z]{4}[0-9]{2}01\.WT[GH]$', x) is not None]
                if len(پہلہ_سے_مسلیں):
                    مسل_پیداوار_مرکسم = پہلہ_سے_مسلیں[نمپی.random.randint(len(پہلہ_سے_مسلیں))]
                else:
                    پہلہ_ہونےولے_اشتمال = False
            else:
                پہلہ_ہونےولے_اشتمال = False

            if not پہلہ_ہونےولے_اشتمال:
                #
                متاغیرات = dict(
                    مسل_مرکسم=مسل_مرکسم,
                    راستہ_١=راستہ_اعداد_اع_گر_نم,
                    راستہ_٢=راستہ_موجودہ,
                    سانچے=سانچے_نمونہ,
                    ار_سی_پی=متن_ر_ح_را,
                    سال=سال_مارکسم,
                    تکرار=10,
                    بھیج=1313
                )

                #
                فرمان = '{مسل_مرکسم} {راستہ_١} {راستہ_٢} {سانچے} {ار_سی_پی} {سال} {تکرار} {بھیج}'.format(**متاغیرات)

                #
                چلو(فرمان)

                if سال_مارکسم != سال:
                    os.rename(راستہ_پیداوار_مرکسم[:-4] + str(سال_مارکسم), راستہ_پیداوار_مرکسم)

            #
            with open(os.path.join(راستہ_پیداوار_مرکسم, مسل_پیداوار_مرکسم), 'r') as م:
                #
                عنوان = ''
                while '@DATE' not in عنوان:
                    عنوان = م.readline()

                ستون_کا_نام = عنوان.split()
                #
                پیداوار = م.readlines()

            #
            شمسی_تابکاری = نمپی.array([float(ب.split()[ستون_کا_نام.index('SRAD')]) for ب in پیداوار if ب != '\n'])
            درجہ_حرارت_زیادہ = نمپی.array([float(ب.split()[ستون_کا_نام.index('TMAX')]) for ب in پیداوار if ب != '\n'])
            درجہ_حرارت_کم = نمپی.array([float(ب.split()[ستون_کا_نام.index('TMIN')]) for ب in پیداوار if ب != '\n'])
            بارش = نمپی.array([float(ب.split()[ستون_کا_نام.index('RAIN')]) for ب in پیداوار if ب != '\n'])

            #
            درجہ_حرارت_اوسط = نمپی.add(درجہ_حرارت_زیادہ, درجہ_حرارت_کم) / 2

            تاریخ_شروع = تاریخ(سال, 1, 1)
            تاریخ_ختم = تاریخ(سال, 12, 31)
            if سال == پہلا_سال:
                دن_ش = سے.timetuple().tm_yday - 1
            else:
                دن_ش = 0
            if سال == آخرا_سال:
                دن_خ = تک.timetuple().tm_yday
            else:
                دن_خ = None

            اعداد = نمپی.array([بارش, شمسی_تابکاری, درجہ_حرارت_زیادہ, درجہ_حرارت_کم, درجہ_حرارت_اوسط]).T
            if calendar.isleap(سال):
                اعداد = نمپی.insert(اعداد, 58, اعداد[59], axis=0)
                if دن_خ is None:
                    دن_خ = 366
            else:
                اعداد = نمپی.array([بارش, شمسی_تابکاری, درجہ_حرارت_زیادہ, درجہ_حرارت_کم, درجہ_حرارت_اوسط]).T
                if دن_خ is None:
                    دن_خ = 365

            اعداد_دن[تاریخ_شروع:تاریخ_ختم] = اعداد[دن_ش:دن_خ, ]

        return اعداد_دن
