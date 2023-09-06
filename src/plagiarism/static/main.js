var _command_ = {
    command: "",
    message: {}
};
var _src_Array = new Array();
var _target_Array = new Array();


$(document).ready(function(){

    function initialize_ui() {
        return;
    };

    initialize_ui();
    $("#downlink").hide();

    // communication between server and front
    function communicate(data) {
        $.ajax({
            url: "/get_demo",
            type: "POST",
            contentType:"application/json; charset=utf-8",
            data: JSON.stringify(data),
            dataType: "json",
            success: function (response) {
                if (response["status"] == "success") {
                    if (data["command"] == "plagiarism_check") {
                        $("#loading").hide();
                        result_check = response["message"][0];
                        if (result_check["stats"]) {
                            $("#downlink").show();

                            document.getElementById("msg_txt").value = JSON.stringify(result_check["data"], null, 4);
                        };
                        alert(result_check["descript"]);

                        $("#file_src").val('');
                        $("#file_target").val('');
                        $("#limit").val('');

                    }
                }
                else {
                    alert(response["message"][0]);
                }
            },
            error: function (request, response) {
                alert("Server Error. Try again later.");
                return ;
            },
            complete: function(response) {
            }
        });
    };



   // Source Upload
    function sendBlob_src(blob) {
        var reader = new FileReader();
        reader.onloadend = function() {
            _base64 = reader.result;
            _src_Array.push(_base64);
        }
        reader.readAsDataURL(blob);
    };

    var src_file_element = document.getElementById("file_src");
    var src_File_Selected = null;
    src_file_element.onclick = function(e) {
        src_File_Selected = this.value;
        this.value = null;
    };

    src_file_element.value = null;
    src_file_element.onchange = function(e) {
        var src_file = e.target.files[0];
        if(!src_file) return;
        _src_Array.length = 0;

        var reader = new FileReader();

        reader.onload = function(event) {
            var wav_buffer = event.target.result;
            var view = new DataView(wav_buffer);
            var blob = new Blob([view], {type: 'text/plain'});
            sendBlob_src(blob);
        };
        reader.readAsArrayBuffer(src_file);
    };

   // Target Upload
    function sendBlob_target(blob) {
        var reader = new FileReader();
        reader.onloadend = function() {
            _base64 = reader.result;
            _target_Array.push(_base64);
        }
        reader.readAsDataURL(blob);
    };

    var target_file_element = document.getElementById("file_target");
    var target_File_Selected = null;
    target_file_element.onclick = function(e) {
        target_File_Selected = this.value;
        this.value = null;
    };

    target_file_element.value = null;
    target_file_element.onchange = function(e) {
        var target_file = e.target.files[0];
        if(!target_file) return;
        _target_Array.length = 0;

        var reader = new FileReader();

        reader.onload = function(event) {
            var wav_buffer = event.target.result;
            var view = new DataView(wav_buffer);
            var blob = new Blob([view], {type: 'text/plain'});
            sendBlob_target(blob);
        };
        reader.readAsArrayBuffer(target_file);
    };

    // Click of button of "File Submit"
    $("#btn_file_submit").click(function() {

        

        if (_src_Array.length == 0) {
            alert("Please select source file.");
            return;
        };
        if (_target_Array.length == 0) {
            alert("Please select target file.");
            return;
        };
        var file_src_name = $("#file_src")[0].files[0].name;
        if (file_src_name.toLowerCase().substr(-4) != '.pdf') {
            alert("Please select pdf file.");
            return;
        };
        var file_target_name = $("#file_target")[0].files[0].name;
        if (file_target_name.toLowerCase().substr(-4) != '.pdf') {
            alert("Please select pdf file.");
            return;
        }
        thresh = $("#limit").val();
        if (thresh == "") {
            alert("Please input threshold value.");
            return;
        }

        src_data = _src_Array.pop();
        target_data = _target_Array.pop();
        const data = {
            first_file_data: src_data,
            first_file_name: file_src_name,
            second_file_data: target_data,
            second_file_name: file_target_name,
            limit: thresh
        };
        _command_["command"] = "plagiarism_check";
        _command_["message"] = data;

        $("#loading").show();
        $("#downlink").hide();
        communicate(_command_);
    });
});