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
	zdeskXPoint(0, 0, 0, 0xe51919, 3);
	zdeskXLabel(0, 0, 0, 'b0', 0xe51919);
	zdeskXPoint(-14.1421, 5.85786, 0, 0xe51919, 3);
	zdeskXLabel(-14.1421, 5.85786, 0, 'b1', 0xe51919);
	zdeskXPoint(-20, 20, 0, 0xe51919, 3);
	zdeskXLabel(-20, 20, 0, 'b2', 0xe51919);
	zdeskXPoint(-14.1421, 34.1421, 0, 0xe51919, 3);
	zdeskXLabel(-14.1421, 34.1421, 0, 'b3', 0xe51919);
	zdeskXPoint(0, 40, 0, 0xe51919, 3);
	zdeskXLabel(0, 40, 0, 'b4', 0xe51919);
	zdeskXPoint(40, 0, 0, 0xe51919, 3);
	zdeskXLabel(40, 0, 0, 'b5', 0xe51919);
	zdeskXPoint(0, -40, 0, 0xe51919, 3);
	zdeskXLabel(0, -40, 0, 'b6', 0xe51919);
	zdeskXPoint(20, -20, 0, 0xe51919, 3);
	zdeskXLabel(20, -20, 0, 'b7', 0xe51919);
	zdeskXCurve('exp_002_wire', 0x1919e5, 4);
}
