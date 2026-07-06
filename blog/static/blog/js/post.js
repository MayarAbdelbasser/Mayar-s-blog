const imageInput = document.getElementById("id_image");
const imagePreview = document.getElementById("image-preview");
print(imageInput);
if (imageInput) {
  imageInput.addEventListener("change", function () {
    const file = this.files[0]; // بنجيب الملف اللي المستخدم اختاره

    if (file) {
      const reader = new FileReader(); // بنستخدم FileReader لقراءة الملف

      // أول ما الملف يخلص قراية، حطي النتيجة في مصدر الصورة واظهريها
      reader.onload = function (e) {
        imagePreview.src = e.target.result;
        imagePreview.style.display = "block"; // إظهار الصورة
      };

      reader.readAsDataURL(file); // قراءة الملف كـ Data URL
    } else {
      // لو المستخدم ألغى الاختيار، اخفي الصورة تاني
      imagePreview.src = "#";
      imagePreview.style.display = "none";
    }
  });
}
