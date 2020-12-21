import re
import os

y_keys = '年/.-'
m_keys = '月/.-'
d_keys = '日'
duration_keys = '-~,'
allow_keys = 'の'  # 「先週の金曜」のように間に許容する文字列を指定

re_date_ptns_dict = dict()


def duration_expansion(ptn: str, duration_keys: str) -> str:
    """
    正規表現のパターンを拡張する
    （2日前 -> 2~3日前）
    """
    digit_match = re.match('\\\d{1,2}', ptn)
    if digit_match is not None:
        digit_key = digit_match.group()
        remain_str = ptn[digit_match.end():]
        new_ptn = f'{digit_key}[{duration_keys}]{digit_key}{remain_str}'
        return new_ptn


def read_re_pattern_strings(file: str, duration_keys: str = None) -> str:
    """
    ファイルから正規表現用の文字列を読み込む
    """
    ptns = list()
    with open(file) as f:
        for row in f:
            ptn = row.strip()
            ptn = ptn.replace('\d', '\d{1,2}')
            ptns.append(ptn)
            if duration_keys is not None:
                new_ptns = duration_expansion(ptn, duration_keys)
                if new_ptns is not None:
                    ptns.append(new_ptns)
    ptns = sorted(ptns, key=lambda x: len(x), reverse=True)
    ptns = '|'.join(ptns)
    return f'({ptns})'


def compile_rules(target_dir: str) -> None:
    """
    正規表現のルールをコンパイルする
    """
    date_prefix_ptns = read_re_pattern_strings(
        os.path.join(target_dir, 'date_prefix.txt'))
    date_suffix_ptns = read_re_pattern_strings(
        os.path.join(target_dir, 'date_suffix.txt'))
    date_dayweek_ptns = read_re_pattern_strings(
        os.path.join(target_dir, 'date_dayweek.txt'))
    date_keywords_ptns = read_re_pattern_strings(
        os.path.join(target_dir, 'date_keywords.txt'), duration_keys)
    date_exclusion_ptns = read_re_pattern_strings(
        os.path.join(target_dir, 'date_exclusion.txt'))

    _re_date_ymd_ptns = f'{date_prefix_ptns}?\d{{4}}[{y_keys}][{allow_keys}]?\d{{1,2}}[{m_keys}][{allow_keys}]?\d{{1,2}}[{d_keys}]?{date_suffix_ptns}?'
    _re_date_ym_ptns = f'{date_prefix_ptns}?\d{{4}}[{y_keys}][{allow_keys}]?\d{{1,2}}[{m_keys}]?{date_suffix_ptns}?'
    _re_date_md_ptns = f'{date_prefix_ptns}?\d{{1,2}}[{m_keys}][{allow_keys}]?\d{{1,2}}[{d_keys}]?{date_suffix_ptns}?'
    _re_date_keywords_ptns = f'{date_keywords_ptns}[{allow_keys}]?{date_suffix_ptns}?{date_suffix_ptns}?{date_suffix_ptns}?'
    _re_date_dayweek_ptns = f'{date_prefix_ptns}?{date_keywords_ptns}?[{allow_keys}]?{date_dayweek_ptns}{date_suffix_ptns}?{date_suffix_ptns}?'
    _re_date_exclusion_ptns = f'^{date_exclusion_ptns}$'

    re_date_ymd_ptns = re.compile(_re_date_ymd_ptns)
    re_date_ym_ptns = re.compile(_re_date_ym_ptns)
    re_date_md_ptns = re.compile(_re_date_md_ptns)
    re_date_keywords_ptns = re.compile(_re_date_keywords_ptns)
    re_date_dayweek_ptns = re.compile(_re_date_dayweek_ptns)

    re_date_ptns_list = list()
    re_date_ptns_list.append(re_date_ymd_ptns)
    re_date_ptns_list.append(re_date_ym_ptns)
    re_date_ptns_list.append(re_date_md_ptns)
    re_date_ptns_list.append(re_date_keywords_ptns)
    re_date_ptns_list.append(re_date_dayweek_ptns)

    re_date_ptns_dict['target_ptns_list'] = re_date_ptns_list
    re_date_ptns_dict['exclusion_ptn_str'] = re.compile(_re_date_exclusion_ptns)
