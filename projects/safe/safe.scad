// mode settings

mode = 0; // [0:Flexed, 1:Half flexed, 2:Plane, 3:Animation, 4:Base proj, 5:Cap proj]


anim = ($t<0.5) ? $t*2:(1-$t)*2;
alphaModes = [1,0.5,0,anim,0,0];
alpha = alphaModes[mode];

isBaseProj = mode==4;
isCapProj = mode==5;
isProj = isBaseProj || isCapProj; 

// visible settings 

isBase = true;
isCap = true;
isCred = true; 

xCred=85; 
yCred=54; 
xCredPad=2; 
yCredPad=3;

wMet = 1;
angleSide = 7;

hFlexSide = 12;
hFlexCenter = 14;
coneFlex = 3;
hLimb = 6;

xBase = (xCred+xCredPad*2);

coneSide=5;
xSide = xBase/3.7;
ySideHalf = yCred/2+yCredPad;

xCenterHalf = xBase/2-xSide;
yCenterHalf = yCred/2+yCredPad+coneSide;

xStartHole = 7;          
xBodyHole = 7;
xEndHole = 10;          
yHole = 40;          

module stop_wizard() {}

eps=0.01; // for flex painting

xDown=gipo(hFlexSide, hFlexSide); // 45 deg
dHole = ySideHalf-yHole/2;          
wFlexSide=gipo(coneSide, xSide);

function gipo(x,y) = sqrt(x*x+y*y);  

module trapV(x,y,dx1,dx2) {
    linear_extrude(1) {
    polygon( [
         [0+eps,0+eps],
         [0+eps+dx1,y-eps],
         [x-dx2-eps,y-eps],
         [x-eps,0+eps]]
        );   
    } 
}

module trapG(x,y,dy1,dy2) {
    linear_extrude(1) {
    polygon( [
         [0+eps,0+eps],
         [0+eps,y-eps],
         [x-eps,y-dy1-eps],
         [x-eps,0+dy2+eps]
        ]);   
    } 
}

module quad(x,y) {
 translate([eps,eps,0])   
 cube([x-2*eps,y-2*eps,1]);   
  }


module base() {
    
   // Center Segment 
   quad(xCenterHalf,yCenterHalf);

   translate([0,yCenterHalf,0]) {
      rotate(90*alpha,[1,0,0]) {   
         trapV(xCenterHalf, hFlexCenter,0, coneFlex);
         translate([0,hFlexCenter,0]) {   
           rotate(90*alpha,[1,0,0]) {   
              trapV(xCenterHalf-coneFlex, hLimb,0,0);
           }    
         }
      }    
   }

   // Side Segment
   
   translate([xCenterHalf,0,0]) 
      rotate(-angleSide*alpha,[0,1,0]) {
      trapG(xSide,yCenterHalf, coneSide,0);
      translate([0,yCenterHalf,0])
           rotate(-atan(coneSide/xSide))
             rotate(90*alpha,[1,0,0]) {    
               trapV(wFlexSide, hFlexSide, 
                    coneFlex,-coneFlex);
               translate([coneFlex, hFlexSide,0])  
                 rotate(90*alpha,[1,0,0])     
                   quad(wFlexSide, hLimb);
             }  

 
   translate([xSide,0,0])
    rotate(-45*alpha,[0,1,0]) {     
      trapG(xDown,ySideHalf,0,0);
      translate([xDown,0])  
        rotate(45*alpha,[0,1,0]) {      
          quad(xStartHole,ySideHalf);
          translate([xStartHole,0,0])
            rotate(-45*alpha,[0,1,0]) {
              translate([0,ySideHalf-dHole,0])
                 quad(xBodyHole, dHole);
              translate([xBodyHole,0,0])
                 rotate(45*alpha,[0,1,0])
                    quad(xEndHole, ySideHalf);
            }  
     }      
   } 

}   
} 

module cap() {
    
   yCenterCapHalf = yCenterHalf-wMet; 
   // Center Segment 
   quad(xCenterHalf,yCenterCapHalf);
 
   // Side Segment
   translate([xCenterHalf,0,0])  
      rotate(-angleSide*alpha,[0,1,0]) { 
         trapG(xSide,yCenterCapHalf, coneSide,0);
         translate([xSide,0,0]) { 
           trapG(hFlexSide+xStartHole/2,
              yCenterCapHalf-coneSide,
             (yCenterCapHalf-coneSide) - (yHole/2-wMet),0);
           translate([hFlexSide+xStartHole/2,0,0])  
              quad(xStartHole,yHole/2-wMet);
         }    
      }    
   
}

module base2() {
 base();
 mirror([1,0,0]) base();
}

module base4() {
 base2();
 mirror([0,1,0]) base2();    
}

module cap2() {
 cap();
 mirror([1,0,0]) cap();
}

module cap4() {
 cap2();
 mirror([0,1,0]) cap2();    
}

if (isBase && !isProj) {
    color([0.7,0.7,0.7])
    base4();
}

if (isCred && !isProj) {
    color([0,0.5,0.5])
    translate([-xCred/2,-yCred/2, hFlexSide/3*2])
    trapV(xCred, yCred,0,0);
}    

if (isCap && !isProj) {
    color([0.85,0,0.85])
    translate([0,0, hFlexSide+wMet/3])
    cap4();
}

if (isBaseProj) {
  projection()  
    base4();
}

if (isCapProj) {
  projection()  
    cap4();
}

function getLen() = 
  4* (
  ySideHalf+
  xStartHole + xBodyHole + xEndHole +
  xDown + 
  hFlexSide*2+hLimb*2 + wFlexSide + 
  xCenterHalf + hFlexCenter + hLimb +
  yHole+xBodyHole
  );

echo(getLen());

