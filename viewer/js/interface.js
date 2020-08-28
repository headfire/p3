// **********************************************
// ******** ZDESK SCRIPT INTERFACE **************
// **********************************************

// position system  

function Decart( x, y, z ) {  return zdeskDecart( x, y, z ); }
function Polar( radius, angle, z) { return zdeskPolar( radius, angle, z); }

// lines and vectors

function Point(place) { zdeskPoint(place); }
function Line(startPlace, endPlace) {zdeskLine(startPlace, endPlace);}
function Vect(start, end) {zdeskVect(start, end);}
function Arc(place, radius, startAngle, angle, lookAt) { zdeskArc(place, radius, startAngle, angle, lookAt); }
function Circle(place, radius, lookAt) { zdeskArc(place, radius, 0, Math.PI * 2, lookAt); }

// flat figures

function Triangle(placeA, placeB, placeC) { zdeskTriangle(placeA, placeB, placeC); }

// solid

function Box(place, sizeX, sizeY, sizeZ, lookAt, zAngle) {  zdeskBox(place, sizeX, sizeY, sizeZ, lookAt, zAngle); }
function Sphere(place, radius) { zdeskSphere(place, radius); }
function Cylinder(place, topRadius, bottomRadius, height, lookAt) { zdeskCylinder(place, topRadius, bottomRadius, height, lookAt); }
function Torus(place, mainRadius, tubeRadius, lookAt) { zdeskTorus(place, mainRadius, tubeRadius, lookAt); }

// marks and comments

function MarkLine(placeA, placeB, markCount) { zdeskMarkLine(placeA, placeB, markCount); }
function MarkAngle(aPlace, basePlace, bPlace, markCount) { zdeskMarkAngle(aPlace, basePlace, bPlace, markCount); }
function Label(place, text) { zdeskLabel(place, text); }
function Message(text) { zdeskMessage(text);}

// coord system

function SetCoord(place, lookAt, zAngle) { zdeskSetCoord(place, lookAt, zAngle); }
function Coord() { zdeskCoord(); }

// color and transparent

const GRAY = 0x808080;
const RED = 0xa02020;
const GREEN = 0x20a020;
const BLUE = 0x2020a0;
const MAGENTA = 0xa000a0;
const CYAN = 0x00a0a0;
const YELLOW = 0xa0a000;
const BROWN = 0x905000;

function SetPointColor(color) { zdeskSetPointColor(color); } 
function SetLineColor(color) { zdeskSetLineColor(color); } 
function SetObjectColor(color) { zdeskSetObjectColor(color); } 
function SetMarkColor(color) { zdeskSetMarkColor(color); } 
function SetTriangleColor(color) { zdeskSetTriangleColor(color); } 
function SetLabelColor(color) { zdeskSetLabelColor(color); } 

const NORMAL = 1;
const GLASS = 0.4;
const CHOST = 0.2;

function SetTransparent(transparent) { zdeskSetTransparent(transparent); } 

// frames control

function SetVisible(startFrame, endFrame) { zdeskSetVisible(startFrame, endFrame); }

// trigonometry math

const PI = Math.PI; 
function Rad(angleInDegrees) { return angleInDegrees/180*Math.PI }
function Deg(angleInRadians) { return angleInRadians/Math.PI*180; }

const Sin = Math.sin;
const Cos = Math.cos;
const Tan = Math.tan;

const ASin = Math.asin; 
const ACos = Math.acos; 
const ATan = Math.atan;

// power math

const E = Math.E;

function Sqr(x) { return x*x;}
const Sqrt = Math.sqrt; 
const Power = Math.pow;
const Exp = Math.exp;
const Log = Math.log

// custom math 

const Min = Math.min;
const Max = Math.max;

function Random(min, max) {
  return Math.random() * ( max - min ) + min;
}

// end of interface
