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
好吧,不多說先來實做

