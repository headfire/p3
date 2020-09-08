function loadedSlideGetParam() { 
	 var param = Object(); 
	 param.isDesk = true; 
	 param.isAxis = true; 
	 param.scaleA = 1; 
	 param.scaleB = 5; 
	 param.deskDX = 0; 
	 param.deskDY = 0; 
	 param.deskDZ = -60; 
	 return param;
}

function loadedSlideMake(slidePath) { 
	zdeskXCurve(slidePath+'exp_001_edge.json', 0xcccccc, 1);
	zdeskXCurve(slidePath+'exp_002_wire.json', 0x1919e5, 4);
	zdeskXPoint(3.25342e-15, 3, 0, 0xe51919, 6);
	zdeskXLabel(3.25342e-15, 3, 0, 'd_0', 0xe51919);
	zdeskXPoint(-17, 20, 0, 0xe51919, 6);
	zdeskXLabel(-17, 20, 0, 'd_1', 0xe51919);
	zdeskXPoint(-1.17773e-14, 37, 0, 0xe51919, 6);
	zdeskXLabel(-1.17773e-14, 37, 0, 'd_2', 0xe51919);
	zdeskXPoint(20.199, -31, 0, 0xe51919, 6);
	zdeskXLabel(20.199, -31, 0, 'd_3', 0xe51919);
	zdeskXCurve(slidePath+'exp_003_wire.json', 0xcccccc, 1);
}
