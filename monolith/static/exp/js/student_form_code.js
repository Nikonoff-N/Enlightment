console.log("i am loaded!")

let imgInputHelper = document.getElementById("add-single-img");
let imgInputHelperLabel = document.getElementById("add-img-label");
let imgContainer = document.querySelector(".custom__image-container");
let imgHolder = document.getElementById("img-holder");
let genderCheckbox = document.getElementById("gender-checkbox");
let genderLabel = document.getElementById("gender-label");
let imgFiles = [];

function init_form(){
  console.log("start form js")
  imgInputHelper = document.getElementById("add-single-img");
  imgInputHelperLabel = document.getElementById("add-img-label");
  imgContainer = document.querySelector(".custom__image-container");
  imgHolder = document.getElementById("img-holder");
  genderCheckbox = document.getElementById("gender-checkbox");
  genderLabel = document.getElementById("gender-label");
  imgFiles = [];

  let addImgHandler = () => {
      const file = imgInputHelper.files[0];
      if (!file) return;
      // Generate img preview
      const reader = new FileReader();
      reader.readAsDataURL(file);
      reader.onload = () => {
        
        //imgInputHelper.style.backgroundImage = reader.result;
        console.log('beep')
        // const newImg = document.createElement("img");
        // newImg.src = reader.result;
        imgHolder.src = reader.result;
        //imgContainer.insertBefore(newImg, imgInputHelperLabel);
      };
      // Store img file
      //imgFiles.push(file);
      // Reset image input
      //imgInputHelper.value = "";
      return;
    };
    imgInputHelper.addEventListener("change", addImgHandler);

    let customFormSubmitHandler = (ev) => {
      ev.preventDefault();
      let firstImgInput = document.getElementById("image-input");
      firstImgInput.files = getImgFileList(imgFiles);
      // submit form to server, etc
    };
    document
      .querySelector(".custom__form")
      .addEventListener("submit", customFormSubmitHandler);

  genderCheckbox.addEventListener('change', (event) => {
    if (event.currentTarget.checked) {
      genderLabel.innerHTML = 'Пол:Мужской'

    } else {
      genderLabel.innerHTML = 'Пол:Женский'

    }
  })
}