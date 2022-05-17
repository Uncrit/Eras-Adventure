@Echo off
del editor.exe
ppcrossx64 -B editor.pas -glh -Fu../../vip-code/vipgfx-code/src -Fu../../vip-code/vipgfx-code/TTF/myFT1
del *.o
del *.ppu
del *.s
del *.res
del ..\..\vip-code\vipgfx-code\TTF\myFT1\*.o
del ..\..\vip-code\vipgfx-code\TTF\myFT1\*.ppu
del ..\..\vip-code\vipgfx-code\src\*.o
del ..\..\vip-code\vipgfx-code\src\*.ppu
editor.exe
pause