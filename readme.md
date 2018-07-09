# kokudoDEM2bin

##  [日本語/Japanese]

### 1. 概要

国土地理院配布の[基盤地図情報（数値標高モデル・DEM）](https://fgd.gsi.go.jp/download/ref_dem.html)をバイナリデータに変換するためのコードです。

自動で標高データのダウンロードからバイナリファイルや画像ファイルにしてくれます。

データのソースは国土地理院の基盤地図情報（数値標高モデル）の5m/10m解像度のものです。

出力は5m解像度の標高データです。



### 2. 使用方法

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
python3 kokudoDEM2bin.py <-l lonmin latmin lonmax latmax> [-nd] [-nc] [-ncon] [-nf] [-ms MAXSIZE] [-h] [-min] [-max]
```

* 必須引数
  * `-l lonmin lonmax latmin, latmax` ：経度・緯度の最小・最大値を10進数表記で入力する。
* オプショナル引数
  * `-nd, --nodownload`：jsonファイルのダウンロードをスキップする場合に使用。`json`フォルダに必要なjsonファイルが既にダウンロード済みの場合のみ使用可能。
  * `-nc, --noconvert`：jsonファイルをバイナリデータに変換する作業をスキップする場合に使用。`bin`フォルダに必要なバイナリデータがある場合のみ使用可能。
  * `-ncon, --noconnect`：1タイルごとのバイナリデータを大きなサイズに結合する作業をスキップする場合に使用。`connected_bin`に必要な結合済みバイナリデータがある場合のみ使用可能。
  * `-nf, --nofig`：画像を出力しない場合にのみ使用可能。
  * `-ms MAXSIZE, --maxsize MAXSIZE`：１つの画像として結合するタイルの数（１辺のタイル数）を`int`で指定する。指定しない場合は`10`（10x10=100タイルを結合する）。なお、元データの１タイルは一辺150m程度。
  * `-min VMIN, --vmin VMIN`：DEMを図化する際の最小値。デフォルトは`None`なのでデータ中の最小値を図の最小値とする。
  * `-max VMAX, --vmax VMAX`：DEMを図化する際の最大値。デフォルトは`None`なのでデータ中の最大値を図の最大値とする。
  * `-h`：ヘルプを表示。

※緯度経度の10進法値は次のサイトで調べることができる [Googleマップで緯度・経度を求める](https://user.numazu-ct.ac.jp/~tsato/webmap/sphere/coordinates/advanced.html)



#### 2.3. 実行例

```bash
python3 kokudoDEM2bin.py -l 36.554892 137.638887 36.589236 137.698095 -ms 100 --vmin 1000
```



#### 2.4. 出力ファイル

__[メイン出力]__

* `connected_bin`フォルダ：DEMのバイナリファイル。
  * float32形式
  * リトルエンディアン
  * C言語オーダーのバイナリ配列（[m,n]はm行n列）
  * １ファイルの大きさは`-ms MAXSIZE, --maxsize MAXSIZE`で設定した大きさ通り（`-ms 5`ならば、元データにおいて5x5タイルを１枚のバイナリデータとして書き出す。）
  * ファイル名： `{x}_{y}.bin`
    * `x`：データの左上角のタイル番号(x座標)を示す。
    * `y`：データの左上角のタイル番号(y座標)を示す。



* `fig`フォルダ：`connected_bin`に出力したDEMを図化した画像ファイル。
  * png形式
  * １画像の大きさは`-ms MAXSIZE, --maxsize MAXSIZE`で設定した大きさ通り（`-ms 5`ならば、元データにおいて5x5タイルを１枚の画像として書き出す。）
  * ファイル名：`{x}_{y}.png`
    * `x`：データの左上角のタイル番号(x座標)を示す。
    * `y`：データの左上角のタイル番号(y座標)を示す。



__[中間ファイル]__

* `json`フォルダ：ダウンロードしたDEMのjsonファイルを保存するディレクトリ。データは１タイルごとにある。
* `bin`フォルダ：ダウンロードしたDEMデータをバイナリに変換したファイルを保存するディレクトリ。データは１タイルごとに存在している。`connected_bin`にはここにあるファイルを`-ms MAXSIZE, --maxsize MAXSIZE`で設定した数ずつ結合したバイナリファイルが保存される。



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
  -min VMIN, --vmin VMIN
                        vmin value of DEM illustration. Default is None.
  -max VMAX, --vmax VMAX
                        vmax value of DEM illustration. Default is None.
```

