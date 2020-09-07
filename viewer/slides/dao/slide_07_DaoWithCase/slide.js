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
	loader = new THREE.BufferGeometryLoader();
			exp_001_shape_phong_material = new THREE.MeshPhongMaterial({color:0xff593d,specular:0x333333,shininess:0.9,side: THREE.DoubleSide,});
			loader.load(slidePath+'exp_001_shape.json', function(geometry) {
				mesh = new THREE.Mesh(geometry, exp_001_shape_phong_material);
				mesh.castShadow = true;
				mesh.receiveShadow = true;
				zdeskScene.add(mesh);
				zdeskRender();
			});

			exp_002_shape_phong_material = new THREE.MeshPhongMaterial({color:0xf9ff1e,specular:0x333333,shininess:0.9,side: THREE.DoubleSide,});
			loader.load(slidePath+'exp_002_shape.json', function(geometry) {
				mesh = new THREE.Mesh(geometry, exp_002_shape_phong_material);
				mesh.castShadow = true;
				mesh.receiveShadow = true;
				zdeskScene.add(mesh);
				zdeskRender();
			});

			exp_003_shape_phong_material = new THREE.MeshPhongMaterial({color:0x8482ff,specular:0x333333,shininess:0.9,side: THREE.DoubleSide,});
			loader.load(slidePath+'exp_003_shape.json', function(geometry) {
				mesh = new THREE.Mesh(geometry, exp_003_shape_phong_material);
				mesh.castShadow = true;
				mesh.receiveShadow = true;
				zdeskScene.add(mesh);
				zdeskRender();
			});

}
