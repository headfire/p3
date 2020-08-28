var mainFrameNumber = 1;
var mainFrameCount = 1;
var mainModeFlag = 'mono-mode';
var mainInfoFlag = 'info-on';
var mainPlayFlag = 'play-off'
var mainErrorLine = 0; 
var mainErrorMessage = ''; 
var mainEditorObject = null;

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

//получить строку в которой ошибка при выполнении скрипта
function mainGetErrorLine(e) {
//Mozilla, Chrome tested
       var line = 0;
	   var stackLines = e.stack.split('\n');
	   //console.log(stackLines);
	   var extracted = '';
	   
	   // first algoritm
	   for (i=0;i<stackLines.length; i++) {
	      if (stackLines[i].match(/(\d+\:\d+)/)) {
		     extracted = stackLines[i].match(/(\d+\:\d+)/g).pop();
			 line = extracted.split(':')[0];
			 return line;
		    }
		}	 
	   
	   // next algoritm
	   
	   return line;
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

if (flag == 'play-on') 
   return 'play-off'
if (flag == 'play-off') 
   return 'play-on'
}

function mainSetFlags() {
  document.getElementById('drawZone').className = mainModeFlag + ' ' + mainInfoFlag +  ' ' + mainPlayFlag;  
}

//EXAMPLES LIST
function mainLoadExamplesList(selectItem) {
var inner = '<option value="prompt" selected="selected">Выберите пример для загрузки...</option>';
  for(x in examplesList) {
    inner += '<option value="' + x + '">' + examplesList[x] + '</option>';
  }
  selectItem.innerHTML = inner;
}

function mainOnExample() {
  mainLoadExample(document.getElementById('examplesSelect').value);
}

function mainLoadExample(example) {
  var filename = 'exampl/' + example + '.js?time='+ new Date().getTime();;
  var xmlhttp = new XMLHttpRequest();
  xmlhttp.open('GET', filename, true);
  xmlhttp.onreadystatechange = function() {
  if (xmlhttp.readyState == 4) {
     if(xmlhttp.status == 200) {
       mainEditorObject.setValue(xmlhttp.responseText);
	   mainRunScript();
         }
    }
  };
  xmlhttp.send(null);
}

function mainLoadPopup(name) {
  var filename ='info/' + name + '.html?time='+ new Date().getTime();;
  var xmlhttp = new XMLHttpRequest();
  xmlhttp.open('GET', filename, true);
  xmlhttp.onreadystatechange = function() {
  if (xmlhttp.readyState == 4) {
     if(xmlhttp.status == 200) {
	    document.getElementById('popupContent').innerHTML = xmlhttp.responseText;;
		document.getElementById('popupArea').style.display = 'block';
		 }
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

function mainOnPlay() {
  mainPlayFlag = mainNextFlag(mainPlayFlag);
  mainSetFlags();
  if (mainPlayFlag == 'play-on')
    setTimeout(mainOnTimeoutPlay,1000);
}

function mainOnTimeoutPlay() {
  if (mainPlayFlag == 'play-on') {
     mainFrame(+1);
     setTimeout(mainOnTimeoutPlay, 1000);
	 }
}

function mainOnFrameNext() {
//выключаем проигрывание если включено
  if (mainPlayFlag=='play-on') 
      mainOnPlay();
	  
  mainFrame(+1);
 }

function mainOnFramePrev() {
  //выключаем проигрывание если включено
  if (mainPlayFlag=='play-on') 
      mainOnPlay(); 
	  
  mainFrame(-1);
 }

function mainFrame(step) {
  zdeskFrameChange(step);
  mainSetHtmlByClass('frame-counter', zdeskGetFrameInfo());
  mainSetInfo();
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

// EDITOR
function mainInitEditor(textArea) {
  var setting = {
    lineNumbers: true,
    matchBrackets: true,
    continueComments: "Enter",
    extraKeys: {"Ctrl-Q": "toggleComment"}
   }
   mainEditorObject = CodeMirror.fromTextArea(textArea, setting);
} 

function mainRunScript() {
  mainPlayFlag = 'play-off';
  mainSetFlags();
  zdeskClear();
  mainErrorMessage = '';
  if (mainErrorLine > 0) {
       mainEditorObject.removeLineClass(mainErrorLine - 1, 'background', 'line-error');
	   mainEditorErrorLine =  0;
	  } 
  try {
      eval(mainEditorObject.getValue());
   }
    catch (e) {
       mainErrorLine = mainGetErrorLine(e);	   
 	   mainEditorObject.addLineClass(mainErrorLine - 1, 'background', 'line-error');
	   mainErrorMessage = 'Ошибка в строке '+ mainErrorLine +':'+ ' '+ e.name + ' - '+ e.message +'</font>';
   } 
  mainFrameNumber = 1; 
  mainFrame(0);
}


function mainOnWindowResize() {
  zdeskHandleResize();
}

function mainOnAnimationFrame() {
  requestAnimationFrame( mainOnAnimationFrame );
  zdeskHandleControl();
}































