frame=document.getElementById("frame")

function clearImage() {
      document.getElementById('formFile').value = null;
      frame.src = "";
  }

  document.getElementById("formFile").addEventListener("onchange",preview)

  function preview() {
    console.log("executing")
      frame.src = URL.createObjectURL(event.target.files[0]);
  }
