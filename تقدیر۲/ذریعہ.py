import pandas as pd


class ذریعہ(object):
    ستون = ['بارش', 'شمسی_تابکاری', 'درجہ_حرارت_زیادہ', 'درجہ_حرارت_کم', 'درجہ_حرارت_اوسط']

    def کوائف_پانا(خود, سے, تک, چوڑائی, طول, بلندی, خاکے='۸۔۵ََ'):
        raise NotImplementedError

    def _پاندس_بنانا(خود, سے, تک):
        اعداد_پاندس = pd.DataFrame(columns=list(خود.ستون), index=pd.period_range(سے, تک), dtype=float)
        return اعداد_پاندس


class ذریعہ_نکتہ(ذریعہ):

    def __init__(خود, چوڑائی, طول, بلندی, خاکے=None, تبدل_ستون=None):
        خود.چوڑائی = چوڑائی
        خود.طول = طول
        خود.بلندی = بلندی
        خود.خاکے = خاکے
        خود.تبدل_ستون = تبدل_ستون or {}

    def کوائف_پانا(خود, سے, تک, چوڑائی, طول, بلندی, خاکے='۸۔۵ََ'):
        if خود.چوڑائی != چوڑائی or خود.طول != طول or (بلندی is not None and بلندی != خود.بلندی):
            return
        if خود.خاکے is not None and خاکے is not None and خود.خاکے != خاکے:
            return

        اعداد_پاندس = خود._پاندس_بنانا(سے, تک)

        خود._کوائف_بھرنا(اعداد_پاندس, خود._کوائف_بنانا())

        return اعداد_پاندس

    def _کوائف_بھرنا(khud, adad, naye):
        if naye.index.freq == 'D':
            adad.fillna(naye, inplace=True)
        elif naye.index.freq == 'M':
            raise NotImplementedError
        elif naye.index.freq == 'Y':
            raise NotImplementedError
        else:
            raise ValueError(naye.index)

    def _نام_ستون(خود, ستون):
        try:
            return خود.تبدل_ستون[ستون]
        except KeyError:
            return ستون

    def _کوائف_بنانا(خود):
        raise NotImplementedError
