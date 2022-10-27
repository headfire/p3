// ****************
// настройки камеры
// ****************

//global scale
gs=1;

echo($vpr);
echo($vpt);
echo($vpd);
$vpr =  [50.8, 0, 128.8]; $vpt =  [5941.28, 4141.46, 797.559]; $vpd =  45225.7;

// ********************
// анимационные функции
// ********************

sigma = 0.001;

function isOdd(x) = (x % 2) == 1;

function spline(x,x1,x2,y1,y2) = y1+((1+sin(-90+180*(x-x1)/(x2-x1)))/2)*(y2-y1);   

function fkey(time,keyframes)= 
  [ if (time<keyframes[0][0])
       keyframes[0][1]
    else if (time>=keyframes[len(keyframes)-1][0])
       keyframes[len(keyframes)-1][1]
    else
      for (i=[0:len(keyframes)-2])  
         if ((time>=keyframes[i][0])
             &&(time<=keyframes[i+1][0])) 
                spline(time, keyframes[i][0],keyframes[i+1][0],keyframes[i][1],keyframes[i+1][1])
  ][0];
  
function bkey(time,keyframes)= 
  [ if (time<keyframes[0]+sigma)
       false
    else if (time>=keyframes[len(keyframes)-1]+sigma)
       isOdd(len(keyframes))
    else 
      for (i=[0:len(keyframes)-2])  
         if ((time>=keyframes[i]+sigma)
             &&(time<keyframes[i+1]+sigma)) 
              isOdd(i+1)
  ][0];
  
 function lineLimit(x,y,x1,y1,x2,y2) = 
            (y1-y2)*x + (x2-x1)*y > x2*y1-x1*y2;    


// ****************
// сценарий
// ****************
// Офисный центр Алгоритм представляет
// новогоднюю историю
// Офис Мечты

// Здраствуйте, вы обещали показать мне офис мечты
// Уже Новый Год скоро, а офиса все нет!
// ->Появляется серый куб
scCube = 0;

// Какой-то странный офис... 
// Вы ничего не перепутали?
// Как в нем работать?
// Где будет начальник, то есть я?
// ->Выдавливается дальнее помещение
scRoom1 = 1;

// Отдел продаж?
// ->Выдавливается среднее помещение
scRoom2 = 2;

//startTime = stRoom3Start;
// Бухгалтерия?
// ->Выдавливается ближнее помещение
scRoom3 = 3;

// А чай попить, на диване посидеть?
// ->Выдавливается коридор
scHall = 4;

// Может, двери сделайте? 
// Мне на работу через чердак лазить?
// ->Появляются дверные проемы
scDoorHoles = 5;

// Вы что дверей не видели?
// Сделайте по нормальному
// ->Появляются косяки и приоткрытые двери
scDoors = 6;

// На полу должен быть ламинат
// ->Пол становится коричневым
scLaminat=7;

// Где окна со стеклопакетами?
// ->Появляются оконные проемы
scWindows=8;

// Отоплкение, кондиционеры?
// ->Сверху прилетают батареи
// ->Сверху прилетают кондиционеры
scCond=9;

// Элетричество, Интернет, Телефон
// ->Сверху прилетают кабель-каналы
scEl = 10;

// А светильники у Вас светодиодные?
// ->Диагонально появляются светильники
scSvet = 11;

// Ну вот, похоже на дело - теперь можно работать
// Хотя, честно говоря, в офисах вы ничего не понимаете
// Я бы сделал все по другому
// -> Исчезают кабеля и светильники
scDesign = 12;

// Зачем нам эти угрюмые прямые углы?
// Сделаем повеселее
// -> Появляются перекосы.
scAngle=13;

// И вообще, я хотел для себя овальный кабинет, 
// как в белом доме
// -> Половина станвится овальной
scOval=14;

// Потолки нужно выше.
// -> Потолки выше
scRoofPlus=15;

// Нет, лучше ниже
// -> Потолки ниже
scRoofMinus=16;

// А давайте у меня выше, а у моих подчиненных ниже.
// -> Потолки синусоидой
scRoofSinus=17;

// Вот как-то так. В общем учитесь, ребята, как
// нужно офисы проектировать, 
// а то сдаете приличным людям
// непонятно чего.
// Ах да, еще стены потолще сделайте, 
// чтобы всякие гады работать не мешали.
scWallPlus=18;

// Совсем другое дело!
// -> Появляются светильники
scSvetSin=19;

// ->Через некоторое время все исчезает
scClear=20;

// Офисный центр Алгоритм предлагает 
// готовые офисы и офисы по индивидуальным проектам
// Звоните 8-905-637-99-91
// Желаем Вам встретить Новый год в новом офисе!

// ****************
// настройка времени
// ****************
startScene = scCube;
finishScene = scClear;

frames = -1;
frame = 0;
half = 0.5;
full = 1;
percent = (frames>1)
          ? (frame-1)/(frames-1)
          : $t;
time = startScene+percent*(finishScene+full-startScene);

// ****************
// настройки материалов
// разделение экспорта по материалам
// ****************
mat=0;

matOffice = (mat==0) || (mat==1);
matDoors = (mat==0) || (mat==2);
matWin = (mat==0) || (mat==3);
matWinGlass = (mat==0) || (mat==4);
matLaminat = (mat==0) || (mat==5);
matEl = (mat==0) || (mat==6);
matCond = (mat==0) || (mat==7);
matRad = (mat==0) || (mat==8);
matSvet = (mat==0) || (mat==9);

// ****************
// флаги
// ****************

isOffice = bkey(time,[scCube+half,scClear+half]);
//isRoom1 = bkey(time,[scRoom1+half,scClear+half]);
//isRoom2 = bkey(time,[scRoom2+half,scClear+half]);
//isRoom3 = bkey(time,[scRoom3+half,scClear+half]);
//isHall =  bkey(time,[scHall+half,scClear+half]);
isDoorHoles = bkey(time,[scDoorHoles+half,scClear+half]);
isDoors = bkey(time,[scDoors+half,scClear+half]);
isLaminat = bkey(time,[scLaminat,scClear+half]);
isWindows = bkey(time,[scWindows+half,scClear+half]);
isWindowHoles = bkey(time,[scWindows+half,scClear+half]);
isRad = bkey(time,[scCond,scClear+half]);
isCond = bkey(time,[scCond,scClear+half]);
isEl =  bkey(time,[scEl,scDesign+half]);
isSvet = bkey(time,[scSvet,scDesign+half,
                    scSvetSin, scClear+half]);

//*****************
// числовые параметры
//*****************
// размеры лезвий (гарантированно больше любых элементов)
catSize=20000*gs;

w = fkey(time,[[scWallPlus,150*gs],[scWallPlus+full,250*gs]]);

hBase = 3500*gs;
hDelta1 = fkey(time,[[scRoofPlus,0],
           [scRoofPlus+full,2000*gs],
           [scRoofMinus,2000*gs],
           [scRoofMinus+full,1000*gs],
           [scRoofSinus,1000*gs],
           [scRoofSinus+full,-100*gs],
           ]);

hDelta2 = fkey(time,[[scRoofPlus,0],
           [scRoofPlus+full,2000*gs],
           [scRoofMinus,2000*gs],
           [scRoofMinus+full,1000*gs],
           [scRoofSinus,1000*gs],
           [scRoofSinus+full,2200*gs]
           ]);

hRoom1 = fkey(time,[[scRoom1,hBase*1.2],
                    [scRoom1+full,0]]);

hRoom2 = fkey(time,[[scRoom2,hBase*1.2],
                    [scRoom2+full,0]]);

hRoom3 = fkey(time,[[scRoom3,hBase*1.2],
                    [scRoom3+full,0]]);

hHall = fkey(time,[[scHall,hBase*1.2],
                    [scHall+full,0]]);
                    

yRooms = 7000*gs;
yHall = 3000*gs;
xRoom1 = 4000*gs;
xRoom2 = 6000*gs;
xRoom3 = 4000*gs;

wWindow = 1400*gs;
hWindow = 1400*gs;
zWindow = 1700*gs;

wWinDecor = 150*gs;
dWinDecor = 10*gs;
wWinGlass = 10*gs;

wDoor = 800*gs;
hDoor = 2000*gs;
yDoor =  50*gs;
wDoorDecor = 150*gs;
dDoorDecor = 10*gs;


hRad = (zWindow-hWindow/2)/1.3;
wRad = wWindow/1.3;
dRad = 100*gs;
zRadFinal = (zWindow-hWindow/2)/2;
zRad = fkey(time, [[scCond,15000*gs],
                  [scCond+full,zRadFinal]]);

wCond = wWindow/1.2;
hCond = 400*gs;
dCond = 200*gs;
zCondFinal = (hBase + (zWindow+hWindow/2))/2;
zCond = fkey(time,[[scCond,15000*gs],
                   [scCond+full,zCondFinal]]);


hEl = 150*gs;
wEl = 80*gs;
dEl = yRooms;
zElFinal = 900*gs;
zEl = fkey(time,[[scEl,15000*gs],
                 [scEl+full,zElFinal]]);

dSvet=300*gs; 
hSvet=100*gs; 
deltaSvet=900*gs; 
hPlusSvet=400*gs;

y1SvetLimit = 0;
x1SvetLimit = fkey(time,[[scSvet,0],
                        [scSvet+full,xRoom1+xRoom2+xRoom3+yRooms],
                        [scSvetSin,0],
                        [scSvetSin+full,xRoom1+xRoom2+xRoom3+yRooms]]);
y2SvetLimit = yRooms;
x2SvetLimit = fkey(time,[[scSvet,-yRooms],
                        [scSvet+full,xRoom1+xRoom2+xRoom3],
                        [scSvetSin,-yRooms],
                        [scSvetSin+full,xRoom1+xRoom2+xRoom3]]);


// перекосы
alfa=fkey(time,[[scAngle,0],[scAngle+full,20]]);
beta=fkey(time,[[scAngle,0],[scAngle+full,5]]);
yRoomsDelta=fkey(time,[[scAngle,0],[scAngle+full,1400*gs]]);
gamma=atan((yRoomsDelta*2)/(xRoom1+xRoom2+xRoom3));

// положения дверей
xDoor1 = (xRoom1+sin(alfa)*yRooms)/2;
xDoor2 = xRoom1+sin(alfa)*yRooms+
  (xRoom2-sin(alfa)*yRooms-sin(beta)*yRooms)/2;
xDoor3 = xRoom1+xRoom2+xRoom3-
  (xRoom3+sin(beta)*yRooms)/2;

//овальная стена
xOval = 2500*gs;
deltaOval  = fkey(time,[[scOval,xOval],
                        [scOval+full,0]]);

//появление ламината
percentLaminat = fkey(time,[[scLaminat,0],
                            [scLaminat+full,1]]);


//*****************
// отрисовка
//*****************

function roof(x)=hBase+(hDelta2+hDelta1)/2+(hDelta1-hDelta2)/2*sin(-90+180*(x/(xRoom1+xRoom2+xRoom3)));

function isSvetVisible(x,y) = lineLimit(x,y,
                                        x1SvetLimit,y1SvetLimit,
                                        x2SvetLimit,y2SvetLimit);

module oval(ww,hh) {
    translate([deltaOval,(yRooms+yRoomsDelta)/2,0])
    linear_extrude(hh)
    union() {  
      offset(ww)
        scale([xOval*2/(yRooms+yRoomsDelta),1,1]) 
           circle((yRooms+yRoomsDelta)/2,$fn=100); 
    translate([xOval,0])
      square([xOval*2,(yRooms+yRoomsDelta)+ww*2],true);  
    }    
}

module outerOffice() {
    union() {
       translate([-w,-w,-w])  
         cube([xRoom1+xRoom2+xRoom3+w*2,yRooms+yHall+w*2, hBase*3+w]);
       translate([0,0,-w])  
         oval(w,hBase*2); 
    }    
}

module innerOffice() {
 union() {   
   translate([w,w,0])
     cube([xRoom1+xRoom2+xRoom3-w*2,yRooms+yHall-w*2,hBase*2],false);
 oval(-w,hBase*2);    
 }    
}


module roof() {
    xbegin = -xOval-w*2;
    xend = xRoom1+xRoom2+xRoom3+xOval+w*2;     
    xstep = 100;    
    coords = [[xbegin,catSize], 
               for (x=[xbegin:xstep:xend]) [x, roof(x)],
                [xend,catSize]];
    translate([0,yRooms+yHall+w*2,0])   
      rotate([90,0,0])
        linear_extrude(yRooms+yHall+w*4)     
           polygon(coords);
}

module hallRoomsCat() {
   translate([0,yRooms+yRoomsDelta,0])    
     rotate(180-gamma)
      translate([-catSize,-w,-hBase*0.2])    
       cube([catSize*2,catSize*2,hBase*3]);        
}

module roomsHallCat() {
   translate([0,yRooms+yRoomsDelta,0])    
     rotate(-gamma)
      translate([-catSize,-w,-hBase*0.2])    
       cube([catSize*2,catSize*2,hBase*3]);        
}

module room1Room2Cat() {
   translate([xRoom1,0,0])    
     rotate(-90-alfa)
      translate([-catSize,-w,-hBase*0.2])    
       cube([catSize*2,catSize*2,hBase*3]);        
}

module room2Room1Cat() {
   translate([xRoom1,0,0])    
     rotate(90-alfa)
      translate([-catSize,-w,-hBase*0.2])    
       cube([catSize*2,catSize*2,hBase*3]);        
}

module room2Room3Cat() {
   translate([xRoom1+xRoom2,0,0])    
     rotate(-90+beta)
      translate([-catSize,-w,-hBase*0.2])    
       cube([catSize*2,catSize*2,hBase*3]);        
}

module room3Room2Cat() {
   translate([xRoom1+xRoom2,0,0])    
     rotate(90+beta)
      translate([-catSize,-w,-hBase*0.2])    
       cube([catSize*2,catSize*2,hBase*3]);        
}
  
module hall() {
  difference() { 
    innerOffice();
    hallRoomsCat();      
  }    
}

module room1() {
  difference() { 
    innerOffice();
    roomsHallCat();      
    room1Room2Cat();  
  }    
}


module room2() {
  difference() { 
    innerOffice();
    roomsHallCat();      
    room2Room1Cat();  
    room2Room3Cat();  
  }    
}

module room3() {
  difference() { 
    innerOffice();
    roomsHallCat();      
    room3Room2Cat();  
  }    
}


module doorHole() {
   translate([0,0,hDoor/2])    
    cube([wDoor,w*2+2,hDoor],center=true);  
}

module doorHoles() {
       translate([xRoom1+xRoom2+xRoom3, yRooms-yRoomsDelta+(yHall+yRoomsDelta)/2,0])  
          rotate([0,0,90])
             doorHole();
        translate([0,yRooms+yRoomsDelta,0])  
          rotate([0,0,-gamma])
            translate([xDoor1,0,0])  
               doorHole();
        translate([0, yRooms+yRoomsDelta,0])  
         rotate([0,0,-gamma])
           translate([xDoor2, 0,0])  
                 doorHole();
        translate([0, yRooms+yRoomsDelta,0])  
          rotate([0,0,-gamma])
              translate([xDoor3,0,0])  
                doorHole();
    }

module windowHoles() {
        delta = (xRoom2-w*2-wWindow*2)/2/3+wWindow/2;
        translate([xRoom1/2,0,zWindow])  
           cube([wWindow,w*2+2,hWindow],true);  
        translate([xRoom1+xRoom2/2+delta,0,zWindow])  
           cube([wWindow,w*2+2,hWindow],true);  
        translate([xRoom1+xRoom2/2-delta,0,zWindow])  
           cube([wWindow,w*2+2,hWindow],true);  
        translate([xRoom1+xRoom2+xRoom3/2,0,zWindow])  
           cube([wWindow,w*2+2,hWindow],true);  
}    


if (matOffice)
if (isOffice)
  color("Wheat")
   difference() {
     outerOffice();        
     roof();
     translate([0,0,hRoom1])        
       room1();   
     translate([0,0,hRoom2])        
       room2(); 
     translate([0,0,hRoom3])        
       room3(); 
     translate([0,0,hHall])        
        hall();         
     if (isDoorHoles) {
        doorHoles(); 
     }
     if (isWindowHoles) {
        windowHoles(); 
     }
   }


module door() {
   translate([-wDoor/2,-w,0]) { 
   color("Brown") 
   rotate([0,0,-60])
   cube([wDoor,yDoor,hDoor]); 
   color("Brown") {
     translate([-wDoorDecor,-dDoorDecor,0])  
       cube([wDoorDecor+dDoorDecor, w*2+dDoorDecor*2, hDoor+dDoorDecor]);    
     translate([wDoor-dDoorDecor,-dDoorDecor,0])  
       cube([wDoorDecor+dDoorDecor, w*2+dDoorDecor*2, hDoor+dDoorDecor]);    
     translate([-wDoorDecor,-dDoorDecor,hDoor])  
       cube([wDoor+wDoorDecor*2, w*2+dDoorDecor*2, wDoorDecor+dDoorDecor]);    
   }    
  } 
}


if (matDoors)
if (isDoors) {
    translate([xRoom1+xRoom2+xRoom3, yRooms-yRoomsDelta+(yHall+yRoomsDelta)/2,0])  
      rotate([0,0,90])
         door();
    translate([0,yRooms+yRoomsDelta,0])  
      rotate([0,0,-gamma])
        translate([xDoor1,0,0])  
           door();  
    translate([0, yRooms+yRoomsDelta,0])  
      rotate([0,0,-gamma])
        translate([xDoor2, 0,0])  
          door();  
    translate([0, yRooms+yRoomsDelta,0])  
      rotate([0,0,-gamma])
        translate([xDoor3, 0,0])  
           door();  
}

if (matLaminat)
if (isLaminat) 
    color("Orange") 
     translate([0,0,-1])
      { 
       cube([(xRoom1+xRoom2+xRoom3)*percentLaminat,(yRooms+yHall)*percentLaminat,2]);
       if(percentLaminat>0.8)   
         oval(0,2); 
    }

module window() {
    
   if (matWin)  
   color("White") {
     rotate([90,0,0])
       linear_extrude(w*2+dWinDecor*2,center=true) 
         difference() { 
           square([wWindow+wWinDecor*2,hWindow+wWinDecor*2],center=true); 
           square([wWindow-dWinDecor,hWindow-dWinDecor],center=true); 
          };    
     cube([wWinDecor/2,wWinGlass+dWinDecor*2,hWindow], true);
      }
      
   if(matWinGlass)      
   color("DeepSkyBlue",0.2)
    cube([wWindow,wWinGlass,hWindow],true);
}

if (isWindows) {
        delta = (xRoom2-w*2-wWindow*2)/2/3+wWindow/2;
        translate([xRoom1/2,0,zWindow])  
           window();  
        translate([xRoom1+xRoom2/2+delta,0,zWindow])  
           window();  
        translate([xRoom1+xRoom2/2-delta,0,zWindow])  
           window();  
        translate([xRoom1+xRoom2+xRoom3/2,0,zWindow])  
          window();  
 }
     

// батареи
 
module rad(wRad,dRad,hRad) {
  segments=6;
  spaceRatio = 0.25;
  full=spaceRatio*(segments-1)+segments;    
  step=wRad/full*(1+spaceRatio);
  color("Gray")    
    translate([-wRad/2,0,-hRad/2])    
      for(i=[0:segments-1])
        translate([i*step,0,0])    
           cube([wRad/segments/(1+spaceRatio),dRad,hRad]);
}

 
if (matRad)
if (isRad) {
        delta = (xRoom2-w*2-wWindow*2)/2/3+wWindow/2;
        translate([xRoom1/2,w,zRad])  
           rad(wRad,dRad,hRad);  
        translate([xRoom1+xRoom2/2+delta,w,zRad])  
           rad(wRad,dRad,hRad);  
        translate([xRoom1+xRoom2/2-delta,w,zRad])  
           rad(wRad,dRad,hRad);  
        translate([xRoom1+xRoom2+xRoom3/2,w,zRad])  
           rad(wRad,dRad,hRad);  
 }
 
 
// кондиционеры
 
module cond(wCond,dCond,hCond) {
color("White")
 rotate([-90,0,0])   
  linear_extrude(dCond,scale=0.9)    
    square([wCond,hCond],true);    
}

if (matCond) 
if (isCond) { 
        translate([xRoom1/2,w,zCond])  
           cond(wCond,dCond,hCond);  
        translate([xRoom1+xRoom2/2,w,zCond])  
           cond(wCond,dCond,hCond);  
        translate([xRoom1+xRoom2+xRoom3/2,w,zCond])  
           cond(wCond,dCond,hCond);  
}

// электричество

module el(wEl,dEl,hEl) {
color("White")
   translate([-wEl/2,0,-hEl/2]) 
    cube([wEl,dEl,hEl]);
}

if (matEl)
if (isEl) {
        translate([w,0,zEl])  
           el(wEl,dEl,hEl);  
        translate([xRoom1-w,0,zEl])  
           el(wEl,dEl,hEl);  
        translate([xRoom1+w,0,zEl])  
           el(wEl,dEl,hEl);  
        translate([xRoom1+xRoom2-w,0,zEl])  
           el(wEl,dEl,hEl);  
        translate([xRoom1+xRoom2+w,0,zEl])  
           el(wEl,dEl,hEl);  
       translate([xRoom1+xRoom2+xRoom3-w,0,zEl])  
           el(wEl,dEl,hEl);  
}    

// свет

module svet(xCenter, yCenter, hCenter,
            xSvet,ySvet,hSvet,
            xCount,yCount, dx,dy) {
  xTotal = (xCount-1)*dx;
  yTotal = (yCount-1)*dy; 
  color("White",1)              
  for(xi=[0:xCount-1])   
    for(yi=[0:yCount-1])
      let(x=xCenter+xi*dx-xTotal/2, y=yCenter+yi*dy-yTotal/2)   
       if(isSvetVisible(x,y))  
         translate([x,y,roof(x)+hCenter]) 
           cube([xSvet,ySvet,hSvet],true);
}

if (matSvet)
if (isSvet) {
svet(xRoom1/2,yRooms/2, hPlusSvet,
        dSvet,dSvet,hSvet,
        3,5,deltaSvet,deltaSvet) ;

svet(xRoom1+xRoom2/2,yRooms/2, hPlusSvet,
        dSvet,dSvet,hSvet,
        4,5,deltaSvet,deltaSvet) ;

svet(xRoom1+xRoom2+xRoom3/2,yRooms/2, hPlusSvet,
        dSvet,dSvet,hSvet,
        3,5,deltaSvet,deltaSvet) ;

svet((xRoom1+xRoom2+xRoom3)/2,yRooms+yHall/2, hPlusSvet,
        dSvet,dSvet,hSvet,
        9,1,deltaSvet,deltaSvet);
}


