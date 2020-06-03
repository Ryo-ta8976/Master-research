var THREE = require('three');
var OrbitControls = require("three-orbitcontrols");

(function(){
  var scene, camera, renderer, controls;
  var geometry, material, mesh, axes, particles;
  //var result = []; // 最終的な二次元配列を入れるための配列

  init();
  animate();

  //CSVファイルを読み込む関数getCSV()の定義
  function getCSV() {
    return new Promise((resolve, reject) => {
      var req = new XMLHttpRequest(); // HTTPでファイルを読み込むためのXMLHttpRrequestオブジェクトを生成
      req.open("get", "../data/measure.csv", true); // アクセスするファイルを指定
      req.send(null); // HTTPリクエストの発行

      // レスポンスが返ってきたらconvertCSVtoArray()を呼ぶ	
      req.onload = function () {
        resolve(convertCSVtoArray(req.responseText)); // 渡されるのは読み込んだCSVデータ
      }
    });
  }

  // 読み込んだCSVデータを二次元配列に変換する関数convertCSVtoArray()の定義
  function convertCSVtoArray(str){ // 読み込んだCSVデータが文字列として渡される
    var result = []; // 最終的な二次元配列を入れるための配列
    var tmp = str.split("\n"); // 改行を区切り文字として行を要素とした配列を生成

    // 各行ごとにカンマで区切った文字列を要素とした二次元配列を生成
    for(var i=0;i<tmp.length;++i){
        result[i] = tmp[i].split(',');
    }

    return result;
  }

  async function init() {

    /**
    * 表示箇所を生成するためのシーンオブジェクト
    * @type {Object} 
    */
    scene = new THREE.Scene();
     
     /**
     * モデルの視点を決めるためのカメラオブジェクト
     * @type {Object} 
     */
    camera = new THREE.PerspectiveCamera(45, 1.5, 0.1, 1000);
    camera.position.set(30, 45, 30);
    camera.fov = 90; 
    camera.lookAt(scene.position);

    //controls = new OrbitControls(camera);
    //controls = new OrbitControls(camera, renderer.domElement);
    //controls.update();
    //controls.autoRotate = true;
    
     /**
     * 座標軸を表示させる
     * @type {Object} 
     */
    axes = new THREE.AxisHelper(100);
    scene.add(axes);

    /**
      * 形状オブジェクトの生成
      * @type {Object} 
      */
     var geometry = new THREE.Geometry();

    var data=await getCSV(); //CSVデータの読み込み
    for (var i = 0; i < data.length; i++){
      geometry.vertices.push(new THREE.Vector3(data[i][0]/25, data[i][2]/25, data[i][1]/25));
    }
   
     

     /**
     * 材質オブジェクトの生成
     * @type {Object} 
     */
     var material = new THREE.ParticleBasicMaterial({ color: 0xFF0000, size: 0.5 });
     /**
     * 点オブジェクトの生成
     * @type {Object} 
     */
     particles = new THREE.ParticleSystem(geometry, material);
     scene.add(particles);
    

     /**
     * モデルをレンダリングするためのレンダラーオブジェクト
     * @type {Object} 
     */
    renderer = new THREE.WebGLRenderer();
    renderer.setSize(600, 600);
    document.body.appendChild( renderer.domElement );

  }

  function animate() {

    //controls.update();
    requestAnimationFrame(animate);

    particles.rotation.x += 0.005;
    //particles.rotation.y += 0.002;
    particles.rotation.z += 0.002;

    //controls.update();

    renderer.render(scene, camera);
  }
})();