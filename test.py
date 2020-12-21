from datex.extract_date import compile_rules, extract_date_mention


if __name__ == '__main__':

    compile_rules('datex/keys')

    test_texts = [
        '2020/12/20に頭を打った', '2020年の12月19日に頭を打った', '12月19日から頭が痛い', '１０日ほど前から頭が痛い',
        '12月の1日くらいから頭が痛い', '2~3日くらい前から頭が痛い', '一週間前から頭が痛い', '1カ月から頭が痛い',
        '先月から頭が痛い', '先月の初めから', '先週の金曜から', '前から頭が痛い', '1日に3回薬を飲む'
    ]

    for text in test_texts:
        mention = extract_date_mention(text)
        print(f'text : {text} -> mention : {mention}')