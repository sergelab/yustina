$(function() {
    $(".js-image-upload").on('change', function () {
        //Get count of selected files
        var countFiles = $(this)[0].files.length;
        var imgPath = $(this)[0].value;
        var extn = imgPath.substring(imgPath.lastIndexOf('.') + 1).toLowerCase();
        var image_holder = $(this).closest("div");
        var already = $('#' + $(this).attr('id') + '_already');

        $('button', image_holder).remove();
        $('img', image_holder).remove();
        already.remove();

        if (typeof(FileReader) !== undefined) {
            //loop for each file selected for uploaded.
            for (var i = 0; i < countFiles; i++) {
                var reader = new FileReader();
                reader.onload = function (e) {
                    $("<img />", {
                        "src": e.target.result,
                        "class": "thumb-image"
                    }).insertBefore($('input[type=file]', image_holder));
                };
                image_holder.show();
                reader.readAsDataURL($(this)[0].files[i]);
            }
        } else {
            alert("This browser does not support FileReader.");
        }
    });
});