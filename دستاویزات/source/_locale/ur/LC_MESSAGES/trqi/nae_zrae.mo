��          L               |   �  }   �   	  �   �     �  �   �  }  )  �  �  �   3  �        �  �   �   try:
    ذریعہ_ناسا = NASAPowerWeatherDataProvider(latitude=چوڑائی, longitude=طول, force_update=False)
except (requests.exceptions.ConnectionError, KeyError, JSONDecodeError):
    return

سے = max(ذریعہ_ناسا.first_date, سے)
تک = min(ذریعہ_ناسا.last_date, تک)

اعداد_پاندس = pd.DataFrame(columns=list(متاغیرات), index=pd.period_range(سے, تک), dtype=float)

ستون = {
    'بارش': 'RAIN',
    'شمسی_تابکاری': 'IRRAD',
    'درجہ_حرارت_زیادہ': 'TMAX',
    'درجہ_حرارت_کم': 'TMIN',
    'درجہ_حرارت_اوسط': 'TEMP'
}

for تاریخ in اعداد_پاندس.index:
    for س, س_ناسا in ستون.items():
        اعداد_پاندس.loc[تاریخ][س] = getattr(ذریعہ_ناسا(سے), س_ناسا)

اعداد_پاندس.شمسی_تابکاری *= 1e-6

return اعداد_پاندس اگر آپکہ کیسی وضع کے کوائف کا استعمال کرنا ہیے جو تقدیر میں اب تک دستیاب نہیں ہیے، آپ اسکے لئے ایک نئا ذریعہ کے قسم بنا سکتے ہیں۔ نئا قسم میں آپکو ایک ھی نئے فعل کو لیکھنا پڑھیگا، :meth:`~تقدیر.ذریعہ._کوائف_بنانا`. نئے ذرائع نمونے کے تور پر ناسا نام کا ذریعہ کا _کوائف_بنانا() نام کا فعل نیچے دیئا جاتا ہیے۔ Project-Id-Version: تقدیر 1
Report-Msgid-Bugs-To: 
POT-Creation-Date: 2019-01-10 22:20+0000
PO-Revision-Date: YEAR-MO-DA HO:MI+ZONE
Last-Translator: FULL NAME <EMAIL@ADDRESS>
Language: ur
Language-Team: ur <LL@li.org>
Plural-Forms: nplurals=2; plural=(n != 1)
MIME-Version: 1.0
Content-Type: text/plain; charset=utf-8
Content-Transfer-Encoding: 8bit
Generated-By: Babel 2.6.0
 try:
    ذریعہ_ناسا = NASAPowerWeatherDataProvider(latitude=چوڑائی, longitude=طول, force_update=False)
except (requests.exceptions.ConnectionError, KeyError, JSONDecodeError):
    return

سے = max(ذریعہ_ناسا.first_date, سے)
تک = min(ذریعہ_ناسا.last_date, تک)

اعداد_پاندس = pd.DataFrame(columns=list(متاغیرات), index=pd.period_range(سے, تک), dtype=float)

ستون = {
    'بارش': 'RAIN',
    'شمسی_تابکاری': 'IRRAD',
    'درجہ_حرارت_زیادہ': 'TMAX',
    'درجہ_حرارت_کم': 'TMIN',
    'درجہ_حرارت_اوسط': 'TEMP'
}

for تاریخ in اعداد_پاندس.index:
    for س, س_ناسا in ستون.items():
        اعداد_پاندس.loc[تاریخ][س] = getattr(ذریعہ_ناسا(سے), س_ناسا)

اعداد_پاندس.شمسی_تابکاری *= 1e-6

return اعداد_پاندس اگر آپکہ کیسی وضع کے کوائف کا استعمال کرنا ہیے جو تقدیر میں اب تک دستیاب نہیں ہیے، آپ اسکے لئے ایک نئا ذریعہ کے قسم بنا سکتے ہیں۔ نئا قسم میں آپکو ایک ھی نئے فعل کو لیکھنا پڑھیگا، :meth:`~تقدیر.ذریعہ._کوائف_بنانا`. نئے ذرائع نمونے کے تور پر ناسا نام کا ذریعہ کا _کوائف_بنانا() نام کا فعل نیچے دیئا جاتا ہیے۔ 