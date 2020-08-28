function myGraph(fname, func, 
                 amin, amax, fmin, fmax 
                  ,num) {
  var y = -400 + num*100;
  var steps = 100;
  var step = (amax - amin)/steps;
  var i, a1,z1, a2, z2;
  var k = 400/(fmax - fmin);
  Label(Decart(-600,y,100),fname);
  for (i=0;i<100;i++)  {
     a1 = amin + step * i;
     z1 = (func(a1) - fmin) * k + 10;
     a2 = amin + step * (i + 1);
     z2 = (func(a2) - fmin) * k  + 10;
     Line(Decart(-500+i*5, y, z1),
          Decart(-500+(i+1)*5,y, z2)
          );
  }
}

Label(Decart(0,500,200), 'E = ' + E);

var num = 0;
myGraph( 'Sqr(x)',
    function(x) { return Sqr(x); }, 
    0,3,0,8,num++);
myGraph( 'Sqrt(x)',
    function(x) { return Sqrt(x); }, 
    0,4,0,2,num++);
myGraph( 'Exp(x)',
    function(x) { return Exp(x); }, 
    0,2.5,1,10,num++);
myGraph( 'Log(x)',
    function(x) { return Log(x); }, 
    1,20,0,2,num++);
myGraph( 'Power(x,y)',
    function(x) { return Power(x,1.5); }, 
    1,10,0,20,num++);
