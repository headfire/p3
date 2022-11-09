function loadedSlideGetParam() { 
	 var param = Object(); 
	 param.isDesk = true; 
	 param.isAxis = true; 
	 param.scaleA = 5; 
	 param.scaleB = 1; 
	 param.deskDX = 0; 
	 param.deskDY = 0; 
	 param.deskDZ = -60; 
	 return param;
}

function loadedSlideMake() { 
	zdeskXCurve('exp_001_edge', 0x4c4c4c, 2);
	zdeskXCurve('exp_002_wire', 0x1919e5, 4);
	zdeskXPoint(3.25342e-15, 3, 0, 0xe51919, 3);
	zdeskXLabel(3.25342e-15, 3, 0, 'd0', 0xe51919);
	zdeskXPoint(-17, 20, 0, 0xe51919, 3);
	zdeskXLabel(-17, 20, 0, 'd1', 0xe51919);
	zdeskXPoint(-1.17773e-14, 37, 0, 0xe51919, 3);
	zdeskXLabel(-1.17773e-14, 37, 0, 'd2', 0xe51919);
	zdeskXPoint(20.199, -31, 0, 0xe51919, 3);
	zdeskXLabel(20.199, -31, 0, 'd3', 0xe51919);
	zdeskXCurve('exp_003_wire', 0x4c4c4c, 2);
}
