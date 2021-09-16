function onLoadOpenCV() {
  document.querySelector("input#image").disabled=false;
}

var blob = new Blob();
const fr = new FileReader();
function readImage(input) {
  if (input.files && input.files[0]) {
    fr.onload = (e) => {
      console.log(e.target.result);
      console.log(new Array(e.target.result));
      //   const previewImage = document.querySelector("#preview-image");
      //   previewImage.src = e.target.result;
    };

    fr.readAsArrayBuffer(input.files[0]);
    fr.readAsBinaryString(input.files[0]);
    fr.readAsDataURL(input.files[0]);
    fr.readAsText(input.files[0]);
  }
}
let imgElement = document.querySelector("#upload_img");
let inputElement = document.querySelector("input#image");
inputElement.addEventListener(
  "change",
  (e) => {
    console.log("input changed");
    imgElement.src = URL.createObjectURL(e.target.files[0]);
  },
  false
);

function post(mat, height, width) {
  var data = {};
  data["user_img"] = mat;
  data["height"] = height;
  data["width"] = width;
  data = JSON.stringify(data).replace("\n", "");
  return fetch("", {
    body: data,
    headers: {
      "Content-Type": "application/json",
    },
    method: "post",
  })
    .then((res) => res.json())
    .then((res) => {
      // document.querySelector(".score-int").innerText = res.score;
      return res;
    });
}
function changeByJson(json) {
  var target = document.querySelectorAll(json.selector);
  for(let i=0; i < target.length; i++) {
    target[i][json.attr] = json.values[i]
  }
}
imgElement.onload = function () {
  let src = cv.imread(imgElement);
  let mat = new cv.Mat();
  cv.cvtColor(src, mat, cv.COLOR_RGBA2RGB);
  size = mat.size();
  post(
    new Uint8ClampedArray(mat.data, mat.cols, mat.rows).toString(),
    size.height,
    size.width
  ).then((res) => {
    changeByJson(res);
  });
  mat.delete();
  return;
};

