function myCustomProp(c1, c2, count, n) {
            return c1+(c2-c1)/count*n;
         }

  
function myCustomDiv(point1,point2, count, n) {
          return  Decart( myCustomProp(point1.x, point2.x, count, n),
                          myCustomProp(point1.y,point2.y, count, n),
                          myCustomProp(point1.z,point2.z, count, n)
                     );
           }

SetCoord(Decart(0,0,200));

var pointA = Decart(-300,-300,-100);
var pointB = Decart(-300,300,100);
var pointC = Decart(300,300,-100);
var pointD = Decart(300,-300,100);
var count=10;

Label(pointA,'A');
Label(pointB,'B');
Label(pointC,'C');
Label(pointD,'D');
Point(pointA);
Point(pointB);
Point(pointC);
Point(pointD);
Line(pointA, pointB);
Line(pointB, pointC);
Line(pointC, pointD);
Line(pointD, pointA);

for(var i=1; i<count; i++) 
Line(myCustomDiv(pointA, pointB, count, i), 
            myCustomDiv(pointD, pointC, count, i)
   );

for(var i=1; i<count; i++) 
 Line(myCustomDiv(pointB, pointC, count, i), 
            myCustomDiv(pointA, pointD, count, i)
   );
