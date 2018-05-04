### Parktsai 學習紀錄


```
20180424
今天開始接觸人生第一次的apk逆向工程,最主要流程如下
1.了解APK建立流程
2.實作Reverse apk

依據下圖來看,主要可以分成3個流程
建立APK---> 申請金鑰（RSA）--->簽章

感覺上簽章在這裡的目的是拿來證明開發者身份,但是在今天的實作中會進行重新簽章的動作,是否是一種規避版權的方法？



想學習者可以學習我大大KunYuChen 這篇
https://github.com/18z/apk-re-forfun/blob/master/02/apktool.md
```

![apktool-repackage](https://github.com/parkmftsai/Reverse-apk-research/blob/master/Image/build.png)
<br >


```
20180425
Frida 研究 
1.PC上Frida環境建立
可參考這篇https://www.codemetrix.net/hacking-android-apps-with-frida-1/

2.android模擬器環境（genymotion）
  這有點麻煩,搞了有點久,尤其是裝完android之後透過frida下以下指令時
  會出現
  List of devices attached
  adb server is out of date.  killing...
  cannot bind 'tcp:5037': Address already in use
  ADB server didn't ACK
  會讓人有點生氣╰（‵□′）╯
  一開始以為是有某個process佔了port 5037,殺了一堆process之後還是給你繼續連
  後來看到底下這篇
  
  
  https://blog.csdn.net/hai29785/article/details/52370106
  原來genymotion與pc不是用同一個sdk中的adb,所以某個adb剛好佔住port 5037
  所以只要把genymotion的adb路徑改成跟PC一樣就行囉^_^
  
  在此附上frida-server網址
  https://github.com/frida/frida/releases
  須注意pc上的frida版本與frida-server版本須一致
  yed:
     frida hook實作一遍
```
```
20180426
1.Frida hook 研究 
Frida hook的對象主要以process,原理在於將javascript code inject to any process
相關範例在20180426research資料夾內
Question: 
 如果要植入code,為何植入的是javascript code,python 不能？

可參考https://www.frida.re/docs/javascript-api/
  yed:
     frida hook to android emulator process 實作一遍
  




```
```
20180427~20180501

這陣子在看frida javascript api的使用
官方的介紹有點含糊,看起來與操作起來還是似懂非懂

官方網頁:https://www.frida.re/docs/javascript-api/
,但是這個新發現網頁給的範例似乎有一個脈落可尋,或許可以幫助我更了解frida的作用
http://ahageek.com/blog/wooyun_articles/Frida-%E8%B7%A8%E5%B9%B3%E5%8F%B0%E6%B3%A8%E5%85%A5%E5%B7%A5%E5%85%B7%E5%9F%BA%E7%A1%80%E7%AF%87.html


yed:
     參考並實做一遍上述網頁範例

```
```
20180502 and 20180504
5/2我突然想到一個問題，hook的操作是透過記憶體位址控制的，有沒有一種情況，在使用hook的時候，只要改動一個數值
被hook的process對應的變數，裡頭的數值也會改變？
於是我愉快的玩了一個測試
測試檔案在20180504research
在hook.py 裡頭有這段
var f = new NativeFunction(ptr(0x400566), 'int', ['int','pointer']);
其中0x400566為 目標function的 address
整句的意思是，我按照目標function的格式，也建立了一個function要hook用的
接著我們在hello.py裡頭有個條件式
if(n==10000) 
  ....以下省略
  
結果一測試下去，very nice ，數值不會改變，由此可以證明一點process的變數歸process, hook的還是hook的

5/4
今天我同事大大KunYuChen提出一個問題，在open底下
"""
根据packages.xml中指定的codePath，创建一个目录，apk会被命名成base.apk并拷贝到此，其中lib目录用来存放native库。
這個 base.apk 有無可能跟原本 apk 有差異呢？

"""
這感覺有點像5/2結論的延伸，在此提出一個假設
除非hook會把當前hook的記憶體狀態，把裡頭的hook function也寫進去，才可能
yed:
     驗證這個假設

```
