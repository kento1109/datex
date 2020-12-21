# datex

テキスト中の日付表現に関する文字列を抽出するツールです。  
抽出自体は正規表現によるルールベースの手法を採用しています。

## 使い方

```
from datex.extract_date import compile_rules, extract_date_mention

compile_rules('datex/keys')

mention = extract_date_mention("1週間前から頭が痛い")
print(mention)
# 1週間前から

mention = extract_date_mention("先週の金曜日から頭が痛い")
print(mention)
# 先週の金曜日から
```

抽出例：
```
python datex/test.py
text : 2020/12/20に頭を打った -> mention : 2020/12/20
text : 2020年の12月19日に頭を打った -> mention : 2020年の12月19日
text : 12月19日から頭が痛い -> mention : 12月19日から
text : １０日ほど前から頭が痛い -> mention : 10日ほど前から
text : 12月の1日くらいから頭が痛い -> mention : 12月の1日くらい
text : 2~3日くらい前から頭が痛い -> mention : 2~3日くらい前から
text : 一週間前から頭が痛い -> mention : 1週間前から
text : 1カ月から頭が痛い -> mention : 1カ月から
text : 先月から頭が痛い -> mention : 先月から
text : 先月の初めから -> mention : 先月の初めから
text : 先週の金曜から -> mention : 先週の金曜から
text : 前から頭が痛い -> mention :
text : 1日に3回薬を飲む -> mention :
```
