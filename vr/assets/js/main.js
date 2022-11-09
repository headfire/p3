var mainModeFlag = 'mono-mode';
var mainInfoFlag = 'info-on';
var mainErrorMessage = '';

//UTIL
function mainSetHtmlByClass(className, innerHTML) {
var x = document.getElementsByClassName(className);
var i;
  for (i = 0; i < x.length; i++) {
    x[i].innerHTML = innerHTML;
  }
}

function mainSetInfo() {
   var mode = '';
   if (mainModeFlag == 'cross-eye-mode') {
      mode = '3D Перекрестный взгляд';
      }
   if (mainModeFlag == 'stereo-tv-mode') {
      mode = '3D TV SideBySyde';
      }
   var info = '';
   if (mainErrorMessage !== '') {
     info += "<font color='red'>" + mainErrorMessage +"</font>";
	 } 
	else { 
      info += "<font color='blue'>"+mode+"</font> ";
	  info += "Мышь: Левая: ОСМОТР, Средняя: ПРИБЛИЖЕНИЕ, Правая: СМЕЩЕНИЕ " 
	  info += zdeskGetMessages(); 
   }
   mainSetHtmlByClass('info',info);
}

function mainCloneToolbar() {
   var toolbarCode = document.getElementById('mono-toolbar').innerHTML;
   document.getElementById('left-toolbar').innerHTML = toolbarCode;
   document.getElementById('right-toolbar').innerHTML = toolbarCode;
}

//Запустить отображение в полноэкранном режиме
function launchFullScreen(element) {
if(element.requestFullScreen) {
element.requestFullScreen();
} else if(element.mozRequestFullScreen) {
element.mozRequestFullScreen();
} else if(element.webkitRequestFullScreen) {
element.webkitRequestFullScreen();
}
}

// Выход из полноэкранного режима
function cancelFullscreen() {
if(document.cancelFullScreen) {
document.cancelFullScreen();
} else if(document.mozCancelFullScreen) {
document.mozCancelFullScreen();
} else if(document.webkitCancelFullScreen) {
document.webkitCancelFullScreen();
}
}

// FLAGS
function mainNextFlag(flag) {

if (flag == 'mono-mode') 
    return  'cross-eye-mode';
if (flag == 'cross-eye-mode') 
    return  'stereo-tv-mode';
if (flag == 'stereo-tv-mode') 
    return  'mono-mode';
	
if (flag == 'info-on') 
   return 'info-off'
if (flag == 'info-off') 
   return 'info-on'
}

function mainSetFlags() {
  document.getElementById('drawZone').className = mainModeFlag + ' ' + mainInfoFlag;  
}

function mainSlideGetParamDefault() {
   var param = Object();
   param.isDesk = true; 	 
   param.isAxis = true; 	 
   param.scaleA = 1; 	 
   param.scaleB = 1; 	 
   param.deskDX = 0; 	 
   param.deskDY = 0; 	 
   param.deskDZ = -50;
 return param;
 }  

function mainSlideMakeDefault() {
}
 
function mainLoadSlide(path) {
   var filename = path +'slide.js?time='+ new Date().getTime();;
   var slideGetParam = mainSlideGetParamDefault;
   var slideMake = mainSlideMakeDefault;
   var xmlhttp = new XMLHttpRequest();
   xmlhttp.open('GET', filename, true);
   xmlhttp.onreadystatechange = function() {
     if (xmlhttp.readyState == 4) {
       if (xmlhttp.status == 200) {
		 try {
           eval(xmlhttp.responseText);
	       slideGetParam = loadedSlideGetParam;
           slideMake = loadedSlideMake;
 		 } catch(e) { console.log(e); }
        }
     param = slideGetParam() 
     zdeskInit(document.getElementById( 'webgl' ),'assets/images/textures/', path, param);
	 slideMake();
     mainOnAnimationFrame()
   	 zdeskSetRenderMode('mono-mode');  				
	  }
  };
 xmlhttp.send(null); 
}

function mainOnHome() {
   zdeskHome();
}

function mainOnInfo() {
  mainInfoFlag = mainNextFlag(mainInfoFlag);
  mainSetFlags();
 }


function mainOnFullScreen() {
  launchFullScreen(document.getElementById( 'drawZone' ));
}

function mainOnMode() {
   mainModeFlag = mainNextFlag(mainModeFlag);
   mainSetFlags();
   mainSetInfo();
   zdeskSetRenderMode(mainModeFlag);
 }

function mainOnWindowResize() {
  zdeskHandleResize();
}

function mainOnAnimationFrame() {
  requestAnimationFrame( mainOnAnimationFrame );
  zdeskHandleControl();
}































