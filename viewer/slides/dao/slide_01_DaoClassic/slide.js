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
	zdeskXPoint(0, 0, 0, 0xe51919, 6);
	zdeskXLabel(0, 0, 0, 'b_0', 0xe51919);
	zdeskXPoint(-14.1421, 5.85786, 0, 0xe51919, 6);
	zdeskXLabel(-14.1421, 5.85786, 0, 'b_1', 0xe51919);
	zdeskXPoint(-20, 20, 0, 0xe51919, 6);
	zdeskXLabel(-20, 20, 0, 'b_2', 0xe51919);
	zdeskXPoint(-14.1421, 34.1421, 0, 0xe51919, 6);
	zdeskXLabel(-14.1421, 34.1421, 0, 'b_3', 0xe51919);
	zdeskXPoint(0, 40, 0, 0xe51919, 6);
	zdeskXLabel(0, 40, 0, 'b_4', 0xe51919);
	zdeskXPoint(40, 0, 0, 0xe51919, 6);
	zdeskXLabel(40, 0, 0, 'b_5', 0xe51919);
	zdeskXPoint(0, -40, 0, 0xe51919, 6);
	zdeskXLabel(0, -40, 0, 'b_6', 0xe51919);
	zdeskXPoint(20, -20, 0, 0xe51919, 6);
	zdeskXLabel(20, -20, 0, 'b_7', 0xe51919);
	zdeskXCurve(slidePath+'exp_002_wire.json', 0x1919e5, 4);
}
