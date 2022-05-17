{$MODE OBJFPC}
{$H+}
unit tiles;
interface
uses vipgfx,tools;

const
	mapWidth = 40;
	mapHeight = 32;

type
	aTileSprite = record
		id : string;
		filename : string;
		sprite : gfxImage;
	end;


var
	theTileSprites : array of aTileSprite;
	theMap : array [0..mapWidth,0..mapHeight] of char;

	theMapFileName:string;



function loadTileSprites(defFileName:string):boolean;
procedure freeTileSprites;
	
procedure saveMap(filename:string);
function loadMap(mapFileName:string):boolean;
procedure newMap;

procedure printMap;

function getTileSpriteID(id:string):integer;



implementation

procedure splitTileEquString(s:string;var left,right:string);
var ch:char;
	i:dword;
begin
	left:='';
	right:='';
	i:=1;
	
	repeat
		ch:=s[i];
		inc(i);
	until ch='''';
	
	repeat
		ch:=s[i];
		if ch<>'''' then left:=left+ch;
		inc(i);
	until ch='''';

	repeat
		ch:=s[i];
		inc(i);
	until ch='=';

	repeat
		ch:=s[i];
		inc(i);
	until (ch=' ') or (ch='	');

	repeat
		ch:=s[i];
		right:=right+ch;
		inc(i);
	until (ch=' ') or (ch='	') or (i>length(s));

	
end;


function initTileSprite(left,right:string):boolean;
begin
	setlength(theTileSprites,length(theTileSprites)+1);
	theTileSprites[length(theTileSprites)-1].id:=left;

	if not exist(right) then begin
		makeMessage('Unable to load '+right);
		result:=false;
		exit;
	end;
	pngLoad(theTileSprites[length(theTileSprites)-1].sprite,right);
	theTileSprites[length(theTileSprites)-1].filename:=right;
	result:=true;
end;


function loadTileSprites(defFileName:string):boolean;
var
    f:text;
    s:string;
    left:string;
    right:string;
begin
	if not exist(defFileName) then begin
		makeMessage('File '+defFileName+' not found!');
		result:=false;
		exit;
	end;

	setlength(theTileSprites,0);

	assign(f,defFileName);
	reset(f);

	readln(f,s);
	if s<>'[Tiles]' then begin
		makeMessage('Section [Tiles] not found');
		result:=false;
		exit;
	end;





	repeat
		readln(f,s);
		splitTileEquString(s,left,right);
		if not initTileSprite(left,right) then begin
			result:=false;
			makeMessage('loading Tile '+right+' fail');
			exit;
		end;
	until eof(f);
	




	close(f);

	result:=true;
end;


procedure freeTileSprites;
var i:dword;
begin
	for i:=0 to length(theTileSprites)-1 do begin
		freeImage(theTileSprites[i].sprite);
	end;
	setlength(theTileSprites,0);
end;







procedure saveMap(filename:string);
var f:text;
	x,y:integer;
	s:string;
begin

	assign(f,filename);
	rewrite(f);

	for y:=0 to mapHeight-1 do begin
		s:='';
		for x:=0 to mapWidth-1 do begin

			s:=s+theMap[x,y];

		end;

		writeln(f,s);
	end;



	close(f);

end;




function loadMap(mapFileName:string):boolean;
var
    f:text;
    x,y:dword;
    ch:char;
    no:dword;
    s:string;
begin
	
	theMapFileName:=mapFileName;

	if not exist(mapFileName) then begin
		makeMessage('File '+mapFileName+' not found!');
		result:=false;
		exit;
	end;


	assign(f,mapFileName);
	reset(f);

		for y:=0 to mapHeight-1 do begin
			readln(f,s);
			for x:=0 to mapWidth-1 do begin
				ch:=s[x+1];
				theMap[x,y]:=ch;
			end;

			inc(no);
		end;
		

	close(f);

	result:=true;
end;

procedure printMap;
var
    x,y:dword;
    s:string;
begin
log('printMap');

		for y:=0 to mapHeight-1 do begin
			s:='';
			for x:=0 to mapWidth-1 do begin
				
				s:=s+theMap[x,y];
			end;


			logwrite(s);
		end;
		
end;


procedure newMap;
var x,y:integer;
begin

	for y:=0 to mapHeight-1 do
		for x:=0 to mapWidth-1 do

			theMap[x,y]:='0';



end;




function getTileSpriteID(id:string):integer;
var i:dword;
begin
	for i:=0 to length(theTileSprites)-1 do begin
		if theTileSprites[i].id = id then begin
			result:=i;
			exit;
		end;
	end;
	if id<>'0' then makeMessage('unknow tile '+id);
	result:=-1;
end;

begin
end.