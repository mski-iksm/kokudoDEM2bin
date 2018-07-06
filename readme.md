# kokudoDEM2bin

##  [日本語/Japanese]

### 1. 概要

国土地理院配布の基盤地図情報（数値標高モデル）をバイナリデータに変換するためのコードです。

###2. 使用方法

OSはUbuntu/Linuxを想定。

#### 2.1. 事前準備

1. python3のインストール
2. 必要ライブラリをインストール

```bash
sudo pip3 install numpy matplotlib
```

3. gdalのインストール

```bash
sudo add-apt-repository ppa:ubuntugis/ppa
sudo apt-get update
sudo apt-get install gdal-bin
sudo apt-get -y install python-gdal
```



#### 2.2. 実行方法

``` bash
python3 kokudoDEM2bin.py <-l lonmin latmin lonmax latmax> [-nd] [-nc] [-ncon] [-nf] [-ms MAXSIZE] [-h]
```

* 必須引数
  * `-l lonmin lonmax latmin, latmax` ：経度・緯度の最小・最大値を10進数表記で入力する。
* オプショナル引数
  * `-nd, --nodownload`：jsonファイルのダウンロードをスキップする場合に使用。`json`フォルダに必要なjsonファイルが既にダウンロード済みの場合のみ使用可能。
  * `-nc, --noconvert`：jsonファイルをバイナリデータに変換する作業をスキップする場合に使用。`bin`フォルダに必要なバイナリデータがある場合のみ使用可能。
  * `-ncon, --noconnect`：1タイルごとのバイナリデータを大きなサイズに結合する作業をスキップする場合に使用。`connected_bin`に必要な結合済みバイナリデータがある場合のみ使用可能。
  * `-nf, --nofig`：画像を出力しない場合にのみ使用可能。
  * `-ms MAXSIZE, --maxsize MAXSIZE`：１つの画像として結合するタイルの数（１辺のタイル数）を`int`で指定する。指定しない場合は`10`（10x10=100タイルを結合する）。
  * `-h`：ヘルプを表示。

※緯度経度の10進法値は次のサイトで調べることができる [Googleマップで緯度・経度を求める](https://user.numazu-ct.ac.jp/~tsato/webmap/sphere/coordinates/advanced.html)



#### 2.3. 実行例

```bash
python3 kokudoDEM2bin.py -l 36.554892 137.638887 36.589236 137.698095 -ms 100 --vmin 1000
```





## [英語/English]

Codes for converting DEM data (Kiban Chizu Jyouhou Digital Elevation Map) of Japan into binary file.



### Usage

```bash
usage: kokudoDEM2bin.py [-h] -l LLUR LLUR LLUR LLUR [-nd] [-nc] [-ncon] [-nf]
                        [-ms MAXSIZE]

Download and convert Japanese DEM to binary files.

optional arguments:
  -h, --help            show this help message and exit
  -l LLUR LLUR LLUR LLUR, --llur LLUR LLUR LLUR LLUR
                        Input the Lower Left corner and Upper Right corner
                        cordinate. Order must be [LL(lat) LL(lon) UR(lat)
                        UR(lon)]
  -nd, --nodownload     Set for skip downloading.
  -nc, --noconvert      Set for skip converting each json file to binary.
  -ncon, --noconnect    Set for skip connecting binary files.
  -nf, --nofig          Set for skip illustrating figure.
  -ms MAXSIZE, --maxsize MAXSIZE
                        Max size of connected binary data in number of tiles.
                        The binary data will be separated into multiple files
                        when selected area exceeds this size. Default is 10
                        tiles (10x10 tile box is max).
```

