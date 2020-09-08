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
 
function mainLoadSlide(paper, slide) {
   var filename = 'slides' + '/' + paper + '/' + slide + '/' + 'slide.js?time='+ new Date().getTime();;
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
     zdeskInit(document.getElementById( 'webgl' ),'images/textures/', param);
	 slideMake('slides'+'/'+paper+'/'+slide+'/');
     mainOnAnimationFrame()
   	 zdeskSetRenderMode('mono-mode');  				
	  }
  };
 xmlhttp.send(null); 
}

function mainLoadSlideInfo(paper, slide) {
   var filename = 'slides' + '/' + paper + '/' + slide + '/' + 'slide_info.json?time='+ new Date().getTime();
   var slideName = '';
   var xmlhttp = new XMLHttpRequest();
   xmlhttp.open('GET', filename, true);
   xmlhttp.onreadystatechange = function() {
     if (xmlhttp.readyState == 4) {
       if (xmlhttp.status == 200) {
	       var slideInfo = JSON.parse(xmlhttp.responseText);
		   var slideName = '<font color=gray>Точка сборки - 3D</font>&nbsp;&nbsp;&nbsp;&nbsp;' + slideInfo.slideName;
		   mainSetHtmlByClass('slide-name', slideName)
	    }
	 }
  };
 xmlhttp.send(null); 
}

function mainAboutHTML() {
 s= 
`
<h2>Поддержка 3D-телевизоров и 3D-проекторов и Перекрестного взгляда</h2>
<p>
Созданные иллюстрации можно демонстрировать на 3D-телевизорах и 3D проекторов в стереорежиме без каких либо дополнительных драйверов и настроек.
Перейдите в стерео-режим с помощью кнопки 3D в области иллюстрации. Одно нажатие - режим <b>перекресного взгляда</b>. Второе нажатие - <b>режим 3D-TV SideBySide</b>. 
Для получения нормального результата нужно также перейти в <b>полноэкранный режим</b> (крайняя правая кнопка)
</p>
<h2>О проекте "Точка сборки"</h2>
<p>
Проект "Точка сборки" позволяет делать объемные иллюстрации для различных областей научного знания:
<ul>
<li>3D-моделирование
<li>Черчение, начертательная геометрия
<li>Математика, геометрия, стереометрия, физика
<li>Молекулярная химия и биоинженерия
<li> 3D-графики, визуализация данных, BI-презентации
<li>Разработка в области VR и AR
</ul>
</p>
<p>
Проект может использоваться как демонстрациолнный материал в традиционных и дистанционных обучающих курсах, при
начальном обучении программированию, при создании демо-зон в средних и высших учебных заведениях, на кафедрах графики, математики, физики, химии.
</p>
<h2>Контакты</h2>
<p>
Сайт проекта "Точка сборки" со всеми презентациями 
<a href="https://headfire.github.io/crpoint/">https://headfire.github.io/crpoint/</a>.
</p>
<p>
По всем предложениям пишите <a href="mailto:headfire@yandex.ru">headfire@yandex.ru</a>.
</p>
`;
	return s;
}

function mainLoadPopup(name) {
  var filename = 'slides' + '/' + paper + '/' + slide + '/' + 'slide_about.html?time='+ new Date().getTime();
  var html = mainAboutHTML();
  var xmlhttp = new XMLHttpRequest();
  xmlhttp.open('GET', filename, true);
  xmlhttp.onreadystatechange = function() {
  if (xmlhttp.readyState == 4) {
     if(xmlhttp.status == 200) {
		 html = xmlhttp.responseText + html
		 }
     document.getElementById('popupContent').innerHTML = html;
  	 document.getElementById('popupArea').style.display = 'block';
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































