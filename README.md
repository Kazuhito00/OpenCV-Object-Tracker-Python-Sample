# OpenCV-Object-Tracker-Sample
Python版OpenCVのTracking APIのサンプルです。<br>
<img src="https://user-images.githubusercontent.com/37477845/125820844-4956a881-0d6c-4519-93dd-8c47b80268ed.gif" loading="lazy" width="40%">　
<img src="https://user-images.githubusercontent.com/37477845/125820883-d1b08355-258f-4fcd-a59e-19dbd6fb4c2a.gif" loading="lazy" width="40%"> 

# Requirement 
* opencv-contrib-python 4.8.0.74 or later

# Algorithm
2023/07/25時点でOpenCVには以下10アルゴリズムが実装されています。
* DaSiamRPN
* NanoTrack
* MIL
* GOTURN
* CSRT
* KCF
* Boosting(Legacy API)
* MOSSE(Legacy API)
* MedianFlow(Legacy API)
* TLD(Legacy API)

# Usage
DaSiamRPNトラッカーのみのサンプルと、各アルゴリズムを比較するサンプルの2種類を用意しています。
#### DaSiamRPNトラッカーサンプル
以下コマンドでデモを起動してください。<br>
最初のフレーム表示時にROI選択を行い追跡対象を指定します。<br>
ESCキー押下でプログラム終了、スペースキー押下で追跡対象の再指定を行います。<br>
```
python DaSiamRPN_sample.py
```
* --device<br>
動画ファイル、もしくはカメラデバイス番号の指定<br>
デフォルト："sample_movie/bird.mp4"
* --width<br>
カメラキャプチャ時の横幅<br>
デフォルト：960
* --height<br>
カメラキャプチャ時の縦幅<br>
デフォルト：540


#### 各アルゴリズム比較サンプル
以下コマンドでデモを起動してください。<br>
最初のフレーム表示時にROI選択を行い追跡対象を指定します。<br>
ESCキー押下でプログラム終了、スペースキー押下で追跡対象の再指定を行います。<br>
--use_xxxxを指定することで使用アルゴリズムを追加できます。 ※何も指定していない場合はDaSiamRPNのみで動作<br>
```
python performance_comparison_sample.py
```
* --device<br>
動画ファイル、もしくはカメラデバイス番号の指定<br>
デフォルト："sample_movie/bird.mp4"
* --width<br>
カメラキャプチャ時の横幅<br>
デフォルト：960
* --height<br>
カメラキャプチャ時の縦幅<br>
デフォルト：540
* --use_mil<br>
MILトラッカーの使用有無<br>
デフォルト：指定なし
* --use_goturn<br>
GOTURNトラッカーの使用有無 ※model/GOTURN配下のzip要解凍<br>
デフォルト：指定なし
* --use_dasiamrpn<br>
DaSiamRPNトラッカーの使用有無<br>
デフォルト：指定なし
* --use_nano<br>
NanoTrackの使用有無<br>
デフォルト：指定なし
* --use_csrt<br>
CSRTトラッカーの使用有無<br>
デフォルト：指定なし
* --use_kcf<br>
KCFトラッカーの使用有無<br>
デフォルト：指定なし
* --use_boosting<br>
Boostingトラッカーの使用有無<br>
デフォルト：指定なし
* --use_mosse<br>
MOSSEトラッカーの使用有無<br>
デフォルト：指定なし
* --use_medianflow<br>
MedianFlowトラッカーの使用有無<br>
デフォルト：指定なし
* --use_tld<br>
TLDトラッカーの使用有無<br>
デフォルト：指定なし

# Author
高橋かずひと(https://twitter.com/KzhtTkhs)
 
# License 
OpenCV-Object-Tracker-Sample is under [Apache-2.0 License](LICENSE).

# License(Image)
サンプル動画は[NHKクリエイティブ・ライブラリー](https://www.nhk.or.jp/archives/creative/)の[ハクセキレイ　エサをついばみながら歩く](https://www2.nhk.or.jp/archives/creative/material/view.cgi?m=D0002161295_00000)を使用しています。
