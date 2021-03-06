let THREE = require("three");
let OrbitControls = require("three-orbitcontrols");
//let https=require('https');

(function () {
  let scene, camera, renderer, controls;
  let geometry, material, mesh, axes, particles;
  //let result = []; // 最終的な二次元配列を入れるための配列
  let id = 11; // 点群id

  init();
  animate();

  //CSVファイルを読み込む関数getCSV()の定義
  // function getCSV() {
  //   return new Promise((resolve, reject) => {
  //     let req = new XMLHttpRequest(); // HTTPでファイルを読み込むためのXMLHttpRrequestオブジェクトを生成
  //     req.open("get", "../data/measure_glass.csv", true); // アクセスするファイルを指定
  //     req.send(null); // HTTPリクエストの発行

  //     // レスポンスが返ってきたらconvertCSVtoArray()を呼ぶ
  //     req.onload = function () {
  //       resolve(convertCSVtoArray(req.responseText)); // 渡されるのは読み込んだCSVデータ
  //     };
  //   });
  // }

  // 読み込んだCSVデータを二次元配列に変換する関数convertCSVtoArray()の定義
  // function convertCSVtoArray(str) {
  //   // 読み込んだCSVデータが文字列として渡される
  //   let result = []; // 最終的な二次元配列を入れるための配列
  //   let tmp = str.split("\n"); // 改行を区切り文字として行を要素とした配列を生成

  //   // 各行ごとにカンマで区切った文字列を要素とした二次元配列を生成
  //   for (let i = 0; i < tmp.length; ++i) {
  //     result[i] = tmp[i].split(",");
  //   }

  //   return result;
  // }

  function getData() {
    const result = [];
    return fetch(`http://127.0.0.1:8000/pointcloud/${encodeURIComponent(id)}`)
      .then((response) => {
        console.log(response.status); // => 200
        return response.json();
      })
      .then((data) => {
        // JSONパースされたオブジェクトが渡される
        result[0] = data.x.split(",");
        result[1] = data.y.split(",");
        result[2] = data.z.split(",");

        return result;
      });
  }

  async function init() {
    const SCALE = 30; //縮尺
    const POINT = 9600; //点群の数

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
    geometry = new THREE.Geometry();

    //let data=await getCSV(); //CSVデータの読み込み
    let data = await getData();
    //for (let i = 0; i < data.length; i++){
    for (let i = 0; i < POINT; i++) {
      //geometry.vertices.push(new THREE.Vector3(data[i][0]/SCALE, data[i][2]/SCALE, data[i][1]/SCALE));　//csvデータ
      geometry.vertices.push(
        new THREE.Vector3(
          data[0][i] / SCALE,
          data[2][i] / SCALE,
          data[1][i] / SCALE
        )
      ); //x, z, y
    }

    /**
     * 材質オブジェクトの生成
     * @type {Object}
     */
    material = new THREE.ParticleBasicMaterial({
      color: 0xff0000,
      size: 0.5,
    });
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
    document.body.appendChild(renderer.domElement);

    // id指定で点群の検索処理
    document.getElementById("form-button").onclick = function () {
      console.log(document.getElementById("number").value);
      id = parseInt(document.getElementById("number").value);
      init();
      animate();
    };
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
