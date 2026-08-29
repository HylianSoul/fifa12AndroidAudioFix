# Audio fix for FIFA 12 (Android version)

**WARNING: the aim of this repository is not garantee the game works in current Android versions. The game is quite old and always is executed using a virtual machine (Virtual Master, VPhoneOS, for example) to working correctly. This patch only fixes its annoying sound in current devices.**

Here you have videos with the original behaviour.

**Make sure the videos are not muted. The audio bug is clearly audible in these recordings.**


https://github.com/user-attachments/assets/0dc4e751-8ef0-496a-86e6-62779d9fc917

https://github.com/user-attachments/assets/3d414ccf-6081-498d-a54b-829dfb595f90


This this can be solved enabling the *forcing 32 bits binary emulation* if you use [VPhoneOS](https://play.google.com/store/apps/details?id=com.yoyo.snake.rush). The problem is you loose performance (FIFA 12 is not a problem in my phone, but I could be with other games) and you have dependency with one application.

I prefer to use [Virtual Master](https://play.google.com/store/apps/details?id=com.clone.android.dual.space) but I have this terrible bug using a different application (using 32 bit Android system, too) in a phone with arm64-v8a (64 bit ARM architecture).

This patch is made to play this game in Virtual Master or other Android virtual machine. This patche is possible thanks to a *.so* patched version I found on the internet. Nevertheless, this version causes bugs when you change the visual settings, and the options are not correctly change. Comparing the original and the patched version, **I used ChatGPT as my assistant**. The final patch was tested several times in my phone and works correctly. To more information, you can see the conversation (written in Spanish, sorry) in the *ai* folder.




