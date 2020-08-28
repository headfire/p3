// *******************************
// ***** ZDESK CORE FUNCTION *****
// *******************************

var zdeskCamera, zdeskControls, zdeskScene, zdeskDrawing;
var zdeskGeometryRenderer, zdeskLeftLabelRenderer, zdeskRightLabelRenderer ,zdeskStereoEffect;
var zdeskCurrentCoord;

var zdeskRenderMode = 'mono-mode';
var zdeskFrameNumber = 1;
var zdeskFrameCount = 1;

var zdeskPointColor;
var zdeskLineColor;
var zdeskObjectColor;
var zdeskTriangleColor;
var zdeskMarkColor;
var zdeskLabelColor;

var zdeskTransparent;

var zdeskVisibleStartFrame;
var zdeskVisibleEndFrame;
var zdeskObjects = Array();
var zdeskMessages = Array();

function zdeskGetFrameInfo() {
 return  zdeskFrameNumber + ' / ' + zdeskFrameCount;
}

function zdeskFrameChange(step) {
  zdeskSetFrame(zdeskFrameNumber + step);
}

function zdeskSetFrame(frameNumber) {
  zdeskFrameNumber = frameNumber;
  if (zdeskFrameNumber < 1) 
    zdeskFrameNumber = zdeskFrameCount;
  if (zdeskFrameNumber > zdeskFrameCount) 
    zdeskFrameNumber = 1;
  for (var i=0;  i < zdeskObjects.length ;i++) {
     zdeskObjects[i].object.visible = 
	    ((zdeskObjects[i].start <= zdeskFrameNumber) 
	    && (zdeskFrameNumber <= zdeskObjects[i].end))
	}	
   zdeskRender();
}

function zdeskGetPointMaterial() {
  return zdeskGetMaterial(zdeskPointColor, false);  
}

function zdeskGetLineMaterial() {
  return zdeskGetMaterial(zdeskLineColor, false);  
}

function zdeskGetObjectMaterial() {
  return zdeskGetMaterial(zdeskObjectColor, false);  
}

function zdeskGetTriangleMaterial() {
  return zdeskGetMaterial( zdeskTriangleColor, true);  
}

function zdeskGetMarkMaterial() {
  return zdeskGetMaterial( zdeskMarkColor, false);  
}

function zdeskGetMaterial(materialColor, isDoubleSide) {
 
  material = new THREE.MeshLambertMaterial( { color: materialColor} );
  
  if (isDoubleSide)
    material.side = THREE.DoubleSide 
	
  if (zdeskTransparent < 1) {
    material.opacity = zdeskTransparent;	
    material.transparent = true;
   }	
  
  return material;	
}

function zdeskForceColor(color) {

    var r = Math.floor( color / (256*256) ) % 256;
    var g = Math.floor( color / 256 ) % 256;
    var b = color % 256;
				
	// усиливаем цвета
	if ( r > 0x90)  r = 0xff; 
    if ( r < 0x60)  r = 0x00; 
	if ( g > 0x90)  g = 0xff; 
    if ( g < 0x60)  g = 0x00; 
	if ( b > 0x90)  b = 0xff; 
    if ( b < 0x60)  b = 0x00; 
				
    return r*256*256 + g*256 + b;
}

function zdeskGetMessages() {
  var str = ''
  for (var i = 0; i < zdeskMessages.length; i++ )  {
    if ((zdeskMessages[i].start <= zdeskFrameNumber) && (zdeskFrameNumber <= zdeskMessages[i].end))
    str += '<p>'+zdeskMessages[i].text+'</p>';
     }
  return str;	 
}

function zdeskSetRenderMode(mode) {
  zdeskRenderMode = mode;
   if (zdeskRenderMode ==  'mono-mode') {
      zdeskGeometryRenderer.autoClear = true;
	  zdeskRightLabelRenderer.domElement.style.display = 'none';
	  }   else {	  
      zdeskGeometryRenderer.autoClear = false;
      zdeskRightLabelRenderer.domElement.style.display = 'block';
   }
   zdeskHandleResize();
}

function zdeskHome() {
   zdeskControls.reset();
}

function zdeskClear() {

    zdeskFrameNumber = 1;
    zdeskFrameCount = 1;

	zdeskScene.remove(zdeskDrawing);

	// becose remove handler don't execute for object cildren
	zdeskLeftLabelRenderer.domElement.innerHTML=""; 
	zdeskRightLabelRenderer.domElement.innerHTML="";
	
	zdeskDrawing = new THREE.Group();
	zdeskScene.add( zdeskDrawing );
	zdeskCurrentCoord = new THREE.Group();
	zdeskDrawing.add( zdeskCurrentCoord );

	SetPointColor(YELLOW);
    SetLineColor(BLUE);
    SetObjectColor(CYAN);
    SetTriangleColor(MAGENTA);
    SetMarkColor(GRAY);
    SetLabelColor(RED);
	
	SetTransparent(NORMAL);
	
	SetVisible(1,1);
	
	zdeskObjects = Array();
	zdeskMessages = Array();
}


function zdeskAdd( object ) {
   zdeskObjects.push( {start:zdeskVisibleStartFrame, end:zdeskVisibleEndFrame, object:object});
   zdeskCurrentCoord.add( object );
}


function zdeskInit(container, texturePath) {
			
 			    if ( ! Detector.webgl ) Detector.addGetWebGLMessage();

		        drawArea = container;

				zdeskCamera = new THREE.PerspectiveCamera( 45, window.innerWidth / window.innerHeight, 1, 3000 );
				zdeskCamera.position.set(0,-1000,1000);
                zdeskCamera.lookAt(new THREE.Vector3( 0, 0, 0 ));

				zdeskControls = new THREE.TrackballControls( zdeskCamera, drawArea );
				zdeskControls.rotateSpeed = 1.0;
				zdeskControls.zoomSpeed = 1.2;
				zdeskControls.panSpeed = 0.8;
				zdeskControls.noZoom = false;
				zdeskControls.noPan = false;
				zdeskControls.staticMoving = true;
				zdeskControls.dynamicDampingFactor = 0.3;
				zdeskControls.keys = [ 65, 83, 68 ];
				zdeskControls.addEventListener( 'change', zdeskRender );

				zdeskScene = new THREE.Scene();

                THREE.ImageUtils.crossOrigin = '';
				
			    var deskGeometry = new THREE.BoxGeometry( 1500, 1000, 40 );
		        var deskTexture = THREE.ImageUtils.loadTexture( texturePath + 'wood.jpg', undefined, zdeskRender);
				deskTexture.minFilter = THREE.LinearFilter;
                var deskMaterial = new THREE.MeshBasicMaterial( {  map: deskTexture } );
                deskMesh = new THREE.Mesh( deskGeometry, deskMaterial );
				deskMesh.position.z = -22;
				zdeskScene.add( deskMesh );
				
				var paperGeometry = new THREE.BoxGeometry( 1189, 841, 2);
		        paperTexture = THREE.ImageUtils.loadTexture(texturePath + 'paper.jpg', undefined, zdeskRender);
				paperTexture.minFilter = THREE.LinearFilter;
				paperTexture.wrapS = THREE.RepeatWrapping;
                paperTexture.wrapT = THREE.RepeatWrapping;
                paperTexture.repeat.set( 4, 4 );
                var paperMaterial = new THREE.MeshBasicMaterial( {  map: paperTexture } );
                paperMesh = new THREE.Mesh( paperGeometry, paperMaterial );
				paperMesh.position.z = -1.9; // not 2 for flat surfaces visible
				zdeskScene.add( paperMesh );
		
				var cnopGeometry = new THREE.CylinderGeometry( 10, 10, 6, 12, 1 );
				var cnopMaterial =  new THREE.MeshLambertMaterial( { color:0x707070 } ); // shading: THREE.FlatShading

                cnopMesh = new THREE.Mesh( cnopGeometry, cnopMaterial );
				cnopMesh.position.set(564,390,0);
				cnopMesh.rotation.x = Math.PI/2;
				zdeskScene.add( cnopMesh );
				
                cnopMesh = new THREE.Mesh( cnopGeometry, cnopMaterial );
				cnopMesh.position.set(-564,390,0);
				cnopMesh.rotation.x = Math.PI/2;
				zdeskScene.add( cnopMesh );

                cnopMesh = new THREE.Mesh( cnopGeometry, cnopMaterial );
				cnopMesh.position.set(564,-390,0);
				cnopMesh.rotation.x = Math.PI/2;
				zdeskScene.add( cnopMesh );

                cnopMesh = new THREE.Mesh( cnopGeometry, cnopMaterial );
				cnopMesh.position.set(-564,-390,0);
				cnopMesh.rotation.x = Math.PI/2;
				zdeskScene.add( cnopMesh );
				
				zdeskDrawing = new THREE.Group();
				zdeskScene.add( zdeskDrawing );
		
				// lights

				light = new THREE.DirectionalLight( 0xffffff );
				light.position.set( -300, -200, 1000 );
				zdeskScene.add( light );

				light = new THREE.AmbientLight( 0x999999 );
				zdeskScene.add( light );

				// renderer
				
                zdeskGeometryRenderer = new THREE.WebGLRenderer( { antialias: true } );
				zdeskGeometryRenderer.setClearColor(  0x999999 );
				zdeskGeometryRenderer.setPixelRatio( window.devicePixelRatio );
				zdeskGeometryRenderer.setSize( drawArea.clientWidth, drawArea.clientHeight );
				zdeskGeometryRenderer.domElement.style.position = 'absolute';
				zdeskGeometryRenderer.domElement.style.top = '0px';
				drawArea.appendChild( zdeskGeometryRenderer.domElement );
		
				zdeskLeftLabelRenderer = new THREE.CSS2DRenderer('left');
				zdeskLeftLabelRenderer.setSize( drawArea.clientWidth/2, drawArea.clientHeight );
				zdeskLeftLabelRenderer.domElement.style.position = 'absolute';
				zdeskLeftLabelRenderer.domElement.style.top = '0px';
				zdeskLeftLabelRenderer.domElement.style.left = '0px';
				zdeskLeftLabelRenderer.domElement.style.pointerEvents = 'none';
				
				zdeskRightLabelRenderer = new THREE.CSS2DRenderer('right');
				zdeskRightLabelRenderer.setSize( drawArea.clientWidth/2, drawArea.clientHeight );
				zdeskRightLabelRenderer.domElement.style.position = 'absolute';
				zdeskRightLabelRenderer.domElement.style.top = '0px';
				zdeskRightLabelRenderer.domElement.style.left = ''+drawArea.clientWidth/2+'px';
				zdeskRightLabelRenderer.domElement.style.pointerEvents = 'none';
				
				drawArea.appendChild( zdeskLeftLabelRenderer.domElement );
				drawArea.appendChild( zdeskRightLabelRenderer.domElement );
				
				zdeskStereoEffect = new THREE.zdeskStereoEffect( zdeskGeometryRenderer, zdeskLeftLabelRenderer, zdeskRightLabelRenderer, 1200 );
				
                zdeskSetRenderMode('mono-mode');  				
}


function zdeskHandleResize() {
    if (zdeskRenderMode == 'mono-mode') {
	   zdeskCamera.aspect = (drawArea.clientWidth/ drawArea.clientHeight);
       zdeskCamera.updateProjectionMatrix();
       zdeskRightLabelRenderer.domElement.style.left = ''+drawArea.clientWidth/2+'px';
       zdeskRightLabelRenderer.setSize( drawArea.clientWidth/2, drawArea.clientHeight );
	   zdeskGeometryRenderer.setSize( drawArea.clientWidth, drawArea.clientHeight );
	   zdeskLeftLabelRenderer.domElement.style.left = '0px';
	   zdeskLeftLabelRenderer.setSize( drawArea.clientWidth, drawArea.clientHeight );
	  }	
	else if (zdeskRenderMode == 'cross-eye-mode') {
	   zdeskCamera.aspect = (drawArea.clientWidth/ drawArea.clientHeight);
       zdeskCamera.updateProjectionMatrix();
       zdeskRightLabelRenderer.domElement.style.left = ''+drawArea.clientWidth/2+'px';
       zdeskRightLabelRenderer.setSize( drawArea.clientWidth/2, drawArea.clientHeight );
	   zdeskLeftLabelRenderer.domElement.style.left = '0px';
	   zdeskLeftLabelRenderer.setSize( drawArea.clientWidth/2, drawArea.clientHeight );
	   zdeskStereoEffect.setSize( drawArea.clientWidth, drawArea.clientHeight );
	  }	
	else if (zdeskRenderMode == 'stereo-tv-mode') {
	   zdeskCamera.aspect = (drawArea.clientWidth/ drawArea.clientHeight) *2;
       zdeskCamera.updateProjectionMatrix();
       zdeskRightLabelRenderer.domElement.style.left = ''+drawArea.clientWidth/2+'px';
       zdeskRightLabelRenderer.setSize( drawArea.clientWidth/2, drawArea.clientHeight );
	   zdeskLeftLabelRenderer.domElement.style.left = '0px';
	   zdeskLeftLabelRenderer.setSize( drawArea.clientWidth/2, drawArea.clientHeight );
	   zdeskStereoEffect.setSize( drawArea.clientWidth, drawArea.clientHeight );
  } 
    zdeskControls.handleResize();
	zdeskRender();
}

function zdeskHandleControl() {
   zdeskControls.update();
}

function zdeskRender() {
    if (zdeskRenderMode == 'mono-mode') {
	   zdeskGeometryRenderer.render( zdeskScene, zdeskCamera );
	   zdeskLeftLabelRenderer.render( zdeskScene, zdeskCamera );
	  }
	else if (zdeskRenderMode == 'cross-eye-mode') {
	   zdeskStereoEffect.render( zdeskScene, zdeskCamera, true);
	  } 
	else if (zdeskRenderMode == 'stereo-tv-mode') {
	   zdeskStereoEffect.render( zdeskScene, zdeskCamera, false);
	  } 
}

// *******************************
// ZDESK CORE INTERFACE FUNCTION
// *******************************

// util 

function zdeskPointOnLine(start, end, k) {
  var dx = end.x - start.x; 
  var dy = end.y - start.y; 
  var dz = end.z - start.z;
  return zdeskDecart(start.x + dx*k, start.y + dy*k, start.z + dz*k);
}

function zdeskDistance(start, end) {
  var dx = end.x - start.x; 
  var dy = end.y - start.y; 
  var dz = end.z - start.z;
  return Math.sqrt(dx*dx+dy*dy+dz*dz);   
}

function zdeskCreateCapPoint(place) {
  var geometry = new THREE.IcosahedronGeometry( 5, 2 );
  var object = new THREE.Mesh( geometry, zdeskGetLineMaterial() );
    object.position.copy(place);
  return object;
}

function zdeskArrow(place, lenght, lookAt) {
  var geometry = new THREE.CylinderGeometry( 0, lenght/3, lenght, 8 );
  var object = new THREE.Mesh( geometry, zdeskGetLineMaterial()  );
    object.position.copy(place);
    if (!(lookAt === undefined))
	   object.lookAt( lookAt );
    object.rotateOnAxis(new THREE.Vector3(1,0,0),Math.PI/2);
  zdeskAdd( object );
}

// position function

function zdeskDecart( x, y, z) {
   z = z || 0;
   return new THREE.Vector3(x, y, z);
}
		    
function zdeskPolar( radius, angle, z) {
   z = z || 0;
   return new THREE.Vector3(radius*Math.cos(angle), radius*Math.sin(angle), z);
}

// lines and vectors

function zdeskPoint(place) {
	var sphereGeometry = new THREE.IcosahedronGeometry( 10, 2 );
    var material = zdeskGetPointMaterial();
	var object = new THREE.Mesh( sphereGeometry, material );
      object.position.copy(place);
    zdeskAdd( object );
}

function zdeskLine(startPlace, endPlace) {
    var geometry = new THREE.CylinderGeometry( 1, 1, 1 );
    var object = new THREE.Mesh( geometry, zdeskGetLineMaterial() );
	object.position.copy(startPlace);
	object.position.lerp( endPlace, 0.5 );
	object.scale.set( 5, startPlace.distanceTo( endPlace ), 5 );
	object.lookAt( endPlace );
	object.rotateOnAxis(new THREE.Vector3(1,0,0),Math.PI/2);
	zdeskAdd( object );
}

function zdeskVect(start, end) {
  var arrowLen = 30; 
  var endLine = zdeskPointOnLine(start, end, 1 - ((arrowLen/2)  / zdeskDistance(start, end)));
  var conePlace = zdeskPointOnLine(endLine, end, 1/2);
  zdeskLine(start, endLine);
  zdeskArrow(endLine, arrowLen, end);
}

function zdeskArc(place, radius, startAngle, angle, lookAt) {

  var geometry = new THREE.TorusGeometry( radius, 5, 8, 40, angle);
  var object = new THREE.Mesh( geometry, zdeskGetLineMaterial()  );
  object.position.copy(place);
	if (!(lookAt === undefined))
	   object.lookAt( lookAt );
	
	// наконечники дуги
   if (angle < 360)	{
       var cap1 = zdeskCreateCapPoint(zdeskPolar(radius, 0));
       var cap2 = zdeskCreateCapPoint(zdeskPolar(radius, angle));
       object.add(cap1);               
       object.add(cap2);               
   }
   
    object.rotateOnAxis(new THREE.Vector3(0,0,1),startAngle);
	zdeskAdd( object );
}

// flat figures

function zdeskTriangle(placeA, placeB, placeC) {
   var geometry = new THREE.Geometry();
     geometry.vertices.push( placeA, placeB, placeC )
     geometry.faces.push( new THREE.Face3( 0, 1, 2 ) );
   var object = new THREE.Mesh( geometry, zdeskGetTriangleMaterial());
   zdeskAdd( object );
}

// solid

function zdeskBox(place, sizeX, sizeY, sizeZ, lookAt, zAngle) {

    var geometry = new THREE.BoxGeometry(sizeX, sizeY, sizeZ );
    var object = new THREE.Mesh( geometry, zdeskGetObjectMaterial() );
	object.position.copy(place);
	if (!(lookAt === undefined))
	   object.lookAt( lookAt );
	if (!(zAngle === undefined))
	   object.rotateOnAxis(new THREE.Vector3(0,0,1), zAngle);
	zdeskAdd( object );
}

function zdeskSphere(place, radius) {

    var geometry = new THREE.SphereGeometry(radius, 40, 40 );
    var object = new THREE.Mesh( geometry, zdeskGetObjectMaterial() );
	object.position.copy(place);
	zdeskAdd( object );
}

function zdeskCylinder(place, topRadius, bottomRadius, height, lookAt) {

    var geometry = new THREE.CylinderGeometry(topRadius, bottomRadius, height, 40, 1 );
    var object = new THREE.Mesh( geometry, zdeskGetObjectMaterial() );
	object.position.copy(place);
	if (!(lookAt === undefined))
	   object.lookAt( lookAt );
	object.rotateOnAxis(new THREE.Vector3(1,0,0), Math.PI/2);
	zdeskAdd( object );
}

function zdeskTorus(place, mainRadius, tubeRadius, lookAt) {

    var geometry = new THREE.TorusGeometry(mainRadius, tubeRadius,  50, 30 );
    var object = new THREE.Mesh( geometry, zdeskGetObjectMaterial() );
	object.position.copy(place);
	if (!(lookAt === undefined))
	   object.lookAt( lookAt );
	zdeskAdd( object );
}

// marks and comments

function zdeskMarkLine(placeA, placeB, markCount) {

  var markLen = 4; 
  var markR = 8; 
  var markSpace = 10; 
  var place = zdeskPointOnLine(placeA, placeB, 1/2);
  var shift = markSpace*(markCount-1)/2;
  
  var group = new THREE.Group;
    group.position.copy(place);
    group.lookAt( placeB );
	
  for (var i=0 ; i<markCount;i++) {
  place = zdeskDecart(0,0,i*markSpace - shift);	
  var geometry = new THREE.CylinderGeometry( markR, markR, markLen, 12 );
  var object = new THREE.Mesh( geometry, zdeskGetMarkMaterial()  );
    object.position.copy(place);
    object.rotateOnAxis(new THREE.Vector3(1,0,0),Math.PI/2);
  group.add(object);	
  }
 
  zdeskAdd( group );
}

function zdeskMarkAngle(aPlace, basePlace, bPlace, markCount) {
  
  // точность при сравнении с нулем
  const delta = 0.001 
  
  // находим вектора при вершине угла
  var a = zdeskDecart(aPlace.x - basePlace.x, aPlace.y - basePlace.y, aPlace.z - basePlace.z);
  var b = zdeskDecart(bPlace.x - basePlace.x, bPlace.y - basePlace.y, bPlace.z - basePlace.z);
  
  //назодим векторное произведение (оно - же перпендикуляр к обоим векторам)
  var cross = zdeskDecart(0,0,0);
  cross.crossVectors(a,b);
 
  // проверяем векторное произведение на близость к нулю
  // это значит, что угол либо нулевой, либо 180 - метки не чертим
  if ( cross.length() < delta ) 
    return;
    
  var markR = 3; 
  var centerR = 40; 
  var spaceR = 10; 
  var shift = spaceR*(markCount-1)/2; 
  
  var group = new THREE.Group;
  
  // вращаем группу в направлении перпендикуляра с сторонам угла
  group.lookAt( cross );

  // вычисляем координаты единичного вектора с учетом поворота 
  group.updateMatrix();
  var ex = zdeskDecart(100,0,0);
  ex.applyMatrix4(group.matrix);
  
  // вычисляем углы
  var angle = b.angleTo(a);
  var aAngle = ex.angleTo(a);
  var bAngle = ex.angleTo(b);
  
  // определяем стартовый угол и корректруем в зависимости от схемы векторов
  var startAngle = aAngle;
  if (Math.abs((bAngle - aAngle) - angle) > delta)
     var startAngle = Math.PI*2-aAngle;
 
  // сдвигаем группу в вершину угла	  
  group.position.copy(basePlace);
	
  for (var i=0 ;i<markCount; i++) {
    var geometry = new THREE.TorusGeometry( centerR - shift + i*spaceR, markR, 8, 40, angle);
    var object = new THREE.Mesh( geometry, zdeskGetMarkMaterial()  );
    object.rotateOnAxis(new THREE.Vector3(0,0,1), startAngle);
    group.add(object);	
  }
 
   zdeskAdd( group );
}

function zdeskLabel(place, text) {

    var r = Math.floor( zdeskLabelColor / (256*256) ) % 256;
    var g = Math.floor( zdeskLabelColor / 256 ) % 256;
    var b = zdeskLabelColor % 256;

	var div = document.createElement( 'div' );
	div.className = 'label';
	div.style.color = 'rgb(' + r + ',' + g + ',' + b + ')';
	div.style.opacity = zdeskTransparent;
	div.textContent = text;
	var label = new THREE.CSS2DObject( div , 'left');
	label.position.copy(place);
	zdeskAdd( label );

	var div = document.createElement( 'div' );
	div.className = 'label';
	div.style.color = 'rgb(' + r + ',' + g + ',' + b + ')';
	div.style.opacity = ''+zdeskTransparent;
	div.textContent = text;
	var label = new THREE.CSS2DObject( div , 'right');
	label.position.copy(place);
	zdeskAdd( label );
}
			
function zdeskMessage(text) {
  zdeskMessages.push( {start:zdeskVisibleStartFrame, end:zdeskVisibleEndFrame, text:text});
}

// coord system

function zdeskSetCoord(place, lookAt, zAngle) {
	zdeskCurrentCoord = new THREE.Group();
	zdeskCurrentCoord.position.copy(place);
	if (!(lookAt === undefined))
	   zdeskCurrentCoord.lookAt(lookAt);
	if (!(zAngle === undefined))
	   zdeskCurrentCoord.rotateOnAxis(new THREE.Vector3(0,0,1), zAngle);
	zdeskDrawing.add( zdeskCurrentCoord );
}

function zdeskCoord() {
  var o = zdeskDecart(0,0,0);
  var len = 300;
  var plen = 100;
  var x = zdeskDecart(len,0,0);
  var y = zdeskDecart(0,len,0);
  var z = zdeskDecart(0,0,len);
  zdeskPoint(o); zdeskLabel(o,'O');
  zdeskVect(o,x); zdeskLabel(x,'x');
  zdeskVect(o,y); zdeskLabel(y,'y');
  zdeskVect(o,z); zdeskLabel(z,'z');
  
  zdeskPoint(zdeskDecart(plen,0,0));
  zdeskPoint(zdeskDecart(0,plen,0));
  zdeskPoint(zdeskDecart(0,0,plen));

  zdeskPoint(zdeskDecart(plen*2,0,0));
  zdeskPoint(zdeskDecart(0,plen*2,0));
  zdeskPoint(zdeskDecart(0,0,plen*2));
}

// color and transparent

function zdeskSetPointColor(color) { zdeskPointColor = color; } 
function zdeskSetLineColor(color) { zdeskLineColor = color; } 
function zdeskSetObjectColor(color) { zdeskObjectColor = color; } 
function zdeskSetMarkColor(color) { zdeskMarkColor = color; } 
function zdeskSetTriangleColor(color) { zdeskTriangleColor = zdeskForceColor(color); } 
function zdeskSetLabelColor(color) { zdeskLabelColor = zdeskForceColor(color); } 
function zdeskSetTransparent(transparent) { zdeskTransparent = transparent; } 

// frames control

function zdeskSetVisible(startFrame, endFrame) {
  zdeskVisibleStartFrame = startFrame;
  zdeskVisibleEndFrame = endFrame;
  if (zdeskFrameCount<endFrame) {
      zdeskFrameCount = endFrame;
  }  
}





























