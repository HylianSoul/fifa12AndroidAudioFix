# Audio fix for FIFA 12 (Android version)

**WARNING: the aim of this repository is not garantee the game works in current Android versions. The game is quite old and is always executed using a virtual machine (Virtual Master, VPhoneOS, for example) to working correctly. This patch only fixes its annoying sound in current devices.**

You have videos with the original behaviour below.

**Make sure the videos are not muted. The audio bug is clearly audible in these recordings.**


https://github.com/user-attachments/assets/0dc4e751-8ef0-496a-86e6-62779d9fc917

https://github.com/user-attachments/assets/3d414ccf-6081-498d-a54b-829dfb595f90


This can be solved enabling the *forcing 32 bits binary emulation* if you use [VPhoneOS](https://play.google.com/store/apps/details?id=com.yoyo.snake.rush). The problem is you loose performance (*FIFA 12* is not a problem in my phone, but it is a problem with other games) and I do not like to have dependency with one specific application.

I prefer to use [Virtual Master](https://play.google.com/store/apps/details?id=com.clone.android.dual.space) but I have this terrible bug using a different application (using a virtualization of a 32 bit Android system, too) in a phone with arm64-v8a (64 bit ARM architecture).

This patch is made to play this game in Virtual Master or other Android virtual machine. This patch is possible thanks to a *.so* patched version I found on the internet. Nevertheless, this version causes bugs when you change the visual settings, and the options are not correctly changed. Comparing the original and the patched version, **I used ChatGPT as my assistant**. The final patch was tested several times in my phone and works correctly. To more information, you can see the conversation (written in Spanish, sorry) in the *ai* folder.

## Execute the patch

1. You need...

    - An APK of the *FIFA 12* game.
    - Python 3 installed and set it in your PATH.

2. Open a terminal in the folder with the *.py* file and the APK and execute...

    ```sh
    python3 fifa12AndroidPatch.py name_of_the_app.apk
    ```

    You will have a new APK with the suffix *_patched*.

3. Install this new APK with the data of the game and enjoy!


## Little explanation

This patch only modifies a bit from zero to one in the *libFIFA12.so* file.

The code checks the SHA-256 of the *.so* file to ensure the patch can be applied. If you do not have the same checksum, it is not applied. You can delete or comment the following lines of the script to force the application of the patch, but I do not garantee the correct functionality of the new APK.

```python
if original_hash != EXPECTED_SHA256:
    print()
    print("ERROR: libFIFA12.so has not the expected SHA-256 checksum.")
    print("Any patch is applied.")
    sys.exit(1)
```

