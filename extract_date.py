import re
import unicodedata

from rule import compile_rules
from rule import re_date_ptns_dict

ksuji_table = str.maketrans('一二三四五六七八九〇十', '12345678901')


def text_normalize(text: str) -> str:
    """
    NFKC正規化, 漢数字をアラビア数字に変換
    """
    text = unicodedata.normalize('NFKC', text)
    return text.translate(ksuji_table)


def extract_date_mention(text: str) -> str:
    """
    テキスト内の日付表現を抽出する
    定時間（絶対時間）表現（2020/12/20）及び不定（昨日）時間表現の両方を抽出する
    例）2020/12/20に頭を打った　-> 2020/12/20
    例）1週間前から頭が痛い　-> 1週間前から
    """
    mention_list = list()
    text = text_normalize(text)
    for re_date_ptns in re_date_ptns_dict['target_ptns_list']:
        mention = re_date_ptns.search(text)
        if mention is not None:
            mention_list.append(mention.group())
    mention_list = sorted(mention_list, key=lambda x: len(x), reverse=True)
    if len(mention_list) > 0:
        target_mention = mention_list[0]  # longest match
        ex_ptns = re_date_ptns_dict['exclusion_ptn_str'].search(target_mention)
        if ex_ptns is not None:
            return ''
        else:
            return target_mention
    else:
        return ''
