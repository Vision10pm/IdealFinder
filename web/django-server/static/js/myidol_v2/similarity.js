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

const inputImage = document.querySelector("#input-image");
inputImage.addEventListener("change", (e) => {
  readImage(e.target);
});
