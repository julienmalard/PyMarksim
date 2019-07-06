import numpy as np
import pandas as pd
from pykrige.uk import UniversalKriging as krigUniversal
from scipy import stats as estad

from تقدیر.ذریعہ import ذریعہ
from تقدیر.متغیرات import متغیرات


class جمع(ذریعہ):
    def __init__(خود, ذرائع):
        خود.ذرائع = ذرائع

    def _کوائف_بنانا(خود, سے, تک, عرض, طول, بلندی, خاکے):
        ذریعہ_سحی = next((ذ for ذ in خود.ذرائع if (ذ.عرض == عرض and ذ.طول == طول and ذ.بلندی == بلندی)), None)
        if not ذریعہ_سحی:
            return کریج(سے, تک, عرض, طول, بلندی, خاکے, دوسرے_ذرائع=خود.ذرائع)
        کو = ذریعہ_سحی.کوائف_پانا(سے, تک, عرض, طول, بلندی, خاکے=خاکے)

        # اگر ساری تاریخ پھلے سے ھی دستیاب ہیں تو کچھ اور کرنے کی ضرورت نہیں ہیے
        if not کو.لاپتہ().size:
            return کو.روزانہ()

        اعداد_پانڈاس = کو.روزانہ()
        پانڈاس_دوسرے = [
            ذ.کوائف_پانا(سے, تک, ذ.عرض, ذ.طول, ذ.بلندی, خاکے=خاکے).روزانہ() for ذ in خود.ذرائع if ذ is not ذریعہ_سحی
        ]
        for م in اعداد_پانڈاس:
            ش = اعداد_پانڈاس[م]
            ش_دوسرے = [پا[م] for پا in پانڈاس_دوسرے]

            ف = فعل_منتخاب(ش)

            اعداد_پانڈاس[م] = ف().تخمینہ_کرنا(ش, ش_دوسرے)

        _حدود_نافذ_کریں(اعداد_پانڈاس)

        return اعداد_پانڈاس


def کریج(سے, تک, عرض, طول, بلندی, خاکے, دوسرے_ذرائع):
    عرض_دوسرے = np.array([ج.عرض for ج in دوسرے_ذرائع])
    طول_دوسرے = np.array([ج.طول for ج in دوسرے_ذرائع])
    بلندی_دوسرے = np.array([ج.بلندی for ج in دوسرے_ذرائع])

    اعداد_پانڈاس = pd.DataFrame(
        np.nan, index=pd.PeriodIndex(pd.date_range(سے, تک)), columns=list(متغیرات)
    )
    قیمتیں = [ذ.کوائف_پانا(سے, تک, ذ.عرض, ذ.طول, ذ.بلندی, خاکے=خاکے).روزانہ() for ذ in دوسرے_ذرائع]
    for م in متغیرات:
        for تا in pd.date_range(سے, تک):
            قیمت = np.array([ق.loc[تا][م] for ق in قیمتیں])
            نہ_لاپتہ = ~np.isnan(قیمت)

            if np.unique(بلندی_دوسرے[نہ_لاپتہ]).size > 1:
                drift_ku = dict(drift_terms=['specified'], specified_drift=[بلندی_دوسرے[نہ_لاپتہ]])
                drift_exe = dict(specified_drift_arrays=[np.array([بلندی])])
            else:
                drift_ku = drift_exe = {}

            if np.unique(قیمت[نہ_لاپتہ]).size > 1:
                اعداد_پانڈاس.loc[تا][م] = krigUniversal(
                    عرض_دوسرے[نہ_لاپتہ], طول_دوسرے[نہ_لاپتہ], قیمت[نہ_لاپتہ], variogram_model='linear', **drift_ku
                ).execute('points', float(عرض), float(طول), **drift_exe)[0][0]
            elif np.unique(قیمت[نہ_لاپتہ]).size == 1:
                اعداد_پانڈاس.loc[تا][م] = قیمت[نہ_لاپتہ][0]

    _حدود_نافذ_کریں(اعداد_پانڈاس)

    return اعداد_پانڈاس


def فعل_منتخاب(شمار):
    اوسط = شمار.mean()
    انحراف = شمار.std()
    ینتہائی = np.any(np.logical_or(شمار < اوسط - 3 * انحراف, شمار > اوسط + 3 * انحراف))
    لاپتہ_نکتے = not np.any(شمار.rolling(10).count() == 0)

    if لاپتہ_نکتے:
        ف = کتمخ if ینتہائی else خط
    else:
        ف = کتمخ۲ if ینتہائی else موو۱

    return ف


class فعل_توسیع(object):

    def تخمینہ_کرنا(خود, ق, دوسرے):
        اچھے = خود._اچھے_ڈھونڈھنا(ق, دوسرے)
        for ج in اچھے:
            ق = ق.fillna(ج['ا'] + ج['ب'] * ج['ج'])
            if not ق.isnull().values.any():
                break
        return ق

    def _اچھے_ڈھونڈھنا(خود, ق, دوسرے):
        نہ_لاپتہ = ~ق.isnull()
        شامل = np.where(نہ_لاپتہ)[:10][0]
        اچھے = []
        if شامل.size:
            for ج in دوسرے:
                ا, ب = خود._خط_بنانا(ق[شامل], ج[شامل])
                پیشن = ا + ب * ج[~شامل]
                تشخیص = np.sqrt(np.mean((پیشن - ق[~شامل]) ** 2))
                if not np.isnan(تشخیص):
                    اچھے.append({'ا': ا, 'ب': ب, 'ج': ج, 'ت': تشخیص})
        return sorted(اچھے, key=lambda س: س['ت'])

    def _خط_بنانا(خود, ب, ت):
        raise NotImplementedError


class موو۱(فعل_توسیع):
    def _خط_بنانا(خود, ب, ت):
        # Hirsch,R.M. (۱۹۸۲). A comparison of four streamflow record extension
        # techniques, Water Resources Research, ۱۸, ۱۰۸۱ – ۱۰۸۸, ۱۹۸۲.
        ب_موو = np.nanstd(ت) / np.nanstd(ب)
        if np.correlate(ت, ب) < 0:
            ب_موو *= -1
        ا_موو = np.nanmean(ت) - (ب_موو * np.nanmean(ب))
        return ا_موو, ب_موو


class کتمخ(فعل_توسیع):
    def _خط_بنانا(خود, ب, ت):
        # کتمخ = KTRL = Kendall-Theil Robust Line = کینڈال تھیل مضبوط خت
        ب = np.array(ب)
        ت = np.array(ت)

        و = ب.size
        ک = []
        for ش in range(و - 1, 1, -1):
            for س in range(0, ش - 2):
                ت_ک = ت[ش] - ت[س]
                ب_ک = ب[ش] - ب[س]
                ک.append(ت_ک / ب_ک)

        ک = np.array(ک)
        ب_کتمخ = np.nanmedian(ک)
        ا_کتمخ = np.nanmedian(ت) - (ب_کتمخ * (np.nanmedian(ب)))

        return ا_کتمخ, ب_کتمخ


class کتمخ۲(فعل_توسیع):
    def _خط_بنانا(خود, ب, ت):
        # KTRL2: Khalil et al (۲۰۱۲)

        # Khalil,B.,T.B.M.J.Ouarda,and A.St-Hilaire (۲۰۱۲). Comparison of
        # record-extension techniques water quality variables, Water Resources
        # Management, ۲۶(۱۴), ۴۲۵۹-۴۲۸۰.

        ب = np.array(ب)
        ت = np.array(ت)

        فی_ب = np.percentile(ب, np.arange(5, 100, 5))
        فی_ت = np.percentile(ت, np.arange(5, 100, 5))

        ک۲ = []
        for ش in range(18, 1, -1):
            for س in range(0, ش - 2):
                تک۲ = فی_ت[ش] - فی_ت[س]
                بک۲ = فی_ب[ش] - فی_ب[س]
                ک۲.append(تک۲ / بک۲)

        ک۲ = np.array(ک۲)
        ب_کتمخ۲ = np.nanmedian(ک۲)
        ا_کتمخ۲ = np.nanmedian(ت) - (ب_کتمخ۲ * (np.nanmedian(ب)))

        return ا_کتمخ۲, ب_کتمخ۲ 


class قامخ(فعل_توسیع):  # پراگما: مت دکھنا
    def _خط_بنانا(خود, ب, ت):
        # قدرتی ارتباط کا مضبوت خط = قامخ
        # Robust Line of Organic Correlation (RLOC), Khalil اور Adamowski (۲۰۱۲)

        # Khalil, B. and Adamowski, J. (۲۰۱۲). Record extension for short-gauged
        # water quality parameters using a newly proposed robust version of the line
        # of organic correlation technique, Hydrol. Earth Syst. Sci., ۱۶, ۲۲۵۳-۲۲۶۶.

        فی_ب = np.percentile(ب, np.arange(5, 100, 5))
        فی_ت = np.percentile(ت, np.arange(5, 100, 5))

        ب_قامخ = (فی_ت[14] - فی_ت[4]) / (فی_ب[14] - فی_ب[4])
        if np.correlate(ت, ب) < 0:
            ب_قامخ *= -1
        ا_قامخ = np.nanmedian(ت) - (ب_قامخ * (np.nanmedian(ب)))

        return ا_قامخ, ب_قامخ


class خط(فعل_توسیع):
    def _خط_بنانا(خود, ب, ت):
        شیب, چوراہا = estad.linregress(ب, ت)[0:2]
        return چوراہا, شیب


def _حدود_نافذ_کریں(اعداد_پانڈاس):
    for م in اعداد_پانڈاس.columns:
        اعداد_پانڈاس.loc[اعداد_پانڈاس[م] > متغیرات[م].زیادہ, م] = متغیرات[م].زیادہ
        اعداد_پانڈاس.loc[اعداد_پانڈاس[م] < متغیرات[م].کم, م] = متغیرات[م].کم
