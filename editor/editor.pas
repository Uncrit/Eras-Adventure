{$MODE OBJFPC}
uses vipgfx,tools,tiles,myTTF;
label theEnd,skip;
const
      startFileName = '';
      scrWidth=1280;
      scrHeight=1024;
      fullscreen=false;

      menuYoffset = 64;
      menuXspace = 8;
      menuYspace = 8;

      tileSize = 31;

var
    selected:integer;

var
   myFont:ttfFont;
   s:string;

   backspace:boolean;



procedure updateMap;
var x,y:integer;
    id:integer;
    s:string;
    x1,y1:integer;
begin

    for y:=0 to mapHeight-1 do begin
        s:='';
        for x:=0 to mapWidth-1 do begin

            id:=getTileSpriteID(theMap[x,y]);
            s:=s+theMap[x,y];


            if id<>-1 then putSpriteAlphaClip(vscreen,x*tileSize,y*tileSize,theTileSprites[id].sprite);

        end;
      
    end;

    
    

    x:=(mouseX div tileSize) mod 1280;
    y:=(mouseY div tileSize) mod 1024;


    putSpriteAlphaClip(vscreen,x*tileSize,y*tileSize,theTileSprites[selected].sprite);
    


    if mouseL then theMap[x,y]:=theTileSprites[selected].id[1];
    if mouseR then theMap[x,y]:='0';

    if keyboard[key_s] then begin

        drawBar(vscreen,480,400,800,550,$ffaaaaaa);
        
        ttfPrintStringXY(vscreen,myFont,500,430,RGBA(0,0,0,255),theMapFileName);
        ttfPrintStringXY(vscreen,myFont,500,480,RGBA(0,0,0,255),'saved');

        saveMap(theMapFileName);

        repeat
            updateGFXsystem;
        until keyboard[KEY_RETURN];
    end;


end;




procedure updateMenu;

procedure getXY(x1,y1:integer; var x,y:integer);
var i:integer;
    counter:integer;
begin

    
    counter:=0;
    for i:=0 to selected do begin
   
        if  counter >= 32 then begin
            inc(y1);
            x1:=0;
            counter:=0;
        end;

        x:=x1 * tileSize + menuXspace * x1;
        y:=y1 * tileSize + menuYoffset + y1*menuYspace;

        inc(x1);

        inc(counter);

    end;     

end;
var x,y:integer;
    i:integer;
begin



    i:=0;
    y:=0;
    x:=0;
    for i:=0 to length(theTileSprites)-1 do begin
        
       if i = (32*(y+1)) then begin
            x:=0;
            inc(y);
        end;

        if (mouseX > (x*tileSize+x*menuXspace)) and (mouseX < ((x+1)*tileSize+x*menuXspace)) and (mouseY > (y*32)+menuYoffset+y*menuYspace) and (mouseY < ((y+1)*32)+menuYoffset+y*menuYspace) then begin
            selected:=i;
        end;

        putSpriteAlphaClip(vscreen,x*(tileSize)+x*menuXspace,y*tileSize+menuYoffset+y*menuYspace,theTileSprites[i].sprite);
        inc(x);

        if i>=length(theTileSprites) then break;

    end;

   
    getXY(0,0,x,y);

    drawRectangleClip(vscreen,x,y,x+32,y+32,$ffff0000);


    ttfPrintStringXY(vscreen,myFont,16,1024-64,RGBA(255,255,255,255),theTileSprites[selected].id + ' -> ' + theTileSprites[selected].filename);
end;



begin
ttfCreateFont('arial.ttf',64,myFont);




if not loadTileSprites('def.txt') then begin
    makeMessage('unable to load Tiles');
    halt;
end;




selected:=0;


initGFXsystem(scrWidth,scrHeight,fullscreen);


if startFileName<>'' then begin
    s:=startFileName;
    goto skip;
end; 

backspace:=false;

repeat
    fastfill(vscreen.data,vscreen.width*vscreen.height,$ff000000);

    ttfPrintStringXY(vscreen,myFont,64,100,RGBA(255,255,255,255),'enter map file name:');

    if (keyboard[key_backspace]) and (not backspace) then begin
        backspace:=true;
        setlength(s,length(s)-1);
    end else
     s:=s+visReadKey;
    
    if not keyboard[key_backspace] then backspace:=false;

    
        ttfPrintStringXY(vscreen,myFont,64,200,RGBA(255,255,255,255),s);


    updateGFXsystem;
    if keyboard[KEY_ESCAPE] then goto theEnd;
until gfxDone or keyboard[KEY_RETURN];


skip:

if not exist(s) then begin
 newmap;
theMapFileName:=s;
end else

if not loadMap(s) then begin
    makeMessage('unable to load map');
    halt;
end;


repeat
    fastfill(vscreen.data,vscreen.width*vscreen.height,$ff000000);


    if not keyboard[KEY_SPACE] then updateMap else updateMenu;



    updateGFXsystem;
until gfxDone or keyboard[KEY_ESCAPE];


theEnd:


finishGFXsystem;
ReturnFPSstring;
ttfCloseFont(myFont);

freeTileSprites;


end.
