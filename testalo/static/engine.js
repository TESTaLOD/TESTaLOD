 $(document).ready(function(){
        $('#keytrue').prop('checked', false);
        $('#toysetcheck').prop('checked', false);
        $('#customRadio').prop('checked', true);
        })
        
        $(function() {
            $('#counter').text('0');
            var generallen = $("input[name=test]:checked").length;
            if(generallen>0){$("#counter").text(generallen);}else{$("#counter").text('0');}
        })
        $("input[name=test]").on("change", function() {
            var len = $("input[name=test]:checked").length;
            $("input[name=sel]").prop('checked', false);
            if(len>0){$("#counter").text(+len);}else{$("#counter").text('0');}
        });
        function ccchange(checkboxElem) {
        if (checkboxElem.checked == true) {
                  $("input[name=test]").each(function(){
                          var input = $(this);
                          input.prop('checked', true);
                          var len = $("input[name=test]:checked").length;
                          $("#counter").text(len)
                  });
        }
        else{
                  $("input[name=test]").each(function(){
                          var input = $(this);
                          input.prop('checked', false);
                          $("#counter").text('0')
                  });
        }
        }

        function keycheck(checkboxElem) {
        if (checkboxElem.checked == true) {
                  $("#keyword-holder").html('<input type="text" class="form-control" id="filename" name="filekeyword" value="testcase" required>')
        }
        else{
          $("#keyword-holder").html("")
        }
        }
        function toysetcheckact(checkboxElem) {
        if (checkboxElem.checked == true) {
                  $("#toysetkeyword-holder").html('<input type="text" class="form-control" id="toyset" name="toysetkeyword" value="Toyset" required>')
        }
        else{
          $("#toysetkeyword-holder").html("")
        }
        }
        

        
        $('#fire2').click(function() {
          document.html;
        });

        $('input[type=radio][name=input-path]').change(function() {
            switch ($(this).val()) {
                case 'url':
                        $("#holder").html('')
                        $("#holder").html('<input type="text" class="form-control" id="urlinput" name="url" value="https://github.com/ICCD-MiBACT/ArCo/tree/master/ArCo-release/test/CQ" required>')
                        $("#keywordlabelholder").html('<div class="custom-control custom-checkbox" style="margin-top:20px"> <input type="checkbox" class="custom-control-input" id="keytrue" name="keytrue" onchange="keycheck(this)"> <label class="custom-control-label" for="keytrue">CQ FILE KEYWORD</label> </div> <div id="keyword-holder"> </div> <small id="emailHelp" class="form-text text-muted">Retrieve all files having KEYWORD from this path</small>')
                        
                    break
                case 'local':
                        $("#keywordlabelholder").html("")
                        $("#holder").html('')
                        $("#holder").html('<div class="custom-file files" id="localfile"> <input type="file" class="custom-file-input" id="customFile" name="localfile" accept=".owl" multiple required> <label class="custom-file-label" for="customFile">Choose files</label> <br /> <ul class="fileList"></ul> </div>')
                        $.fn.fileUploader = function (filesToUpload, sectionIdentifier) {
                            var fileIdCounter = 0;
                        
                            this.closest(".files").change(function (evt) {
                                var output = [];
                        
                                for (var i = 0; i < evt.target.files.length; i++) {
                                    fileIdCounter++;
                                    var file = evt.target.files[i];
                                    var fileId = sectionIdentifier + fileIdCounter;
                        
                                    filesToUpload.push({
                                        id: fileId,
                                        file: file
                                    });
                        
                                    var removeLink = "<a class=\"removeFile\" href=\"#\" data-fileid=\"" + fileId + "\">Remove</a>";
                        
                                    output.push("<li><strong>", escape(file.name), "</strong> - ", file.size, " bytes. &nbsp; &nbsp; ", removeLink, "</li> ");
                                };
                        
                                $(this).children(".fileList")
                                    .append(output.join(""));
                        
                                //reset the input to null - nice little chrome bug!
                                evt.target.value = null;
                            });
                        
                            $(this).on("click", ".removeFile", function (e) {
                                e.preventDefault();
                        
                                var fileId = $(this).parent().children("a").data("fileid");
                        
                                // loop through the files array and check if the name of that file matches FileName
                                // and get the index of the match
                                for (var i = 0; i < filesToUpload.length; ++i) {
                                    if (filesToUpload[i].id === fileId)
                                        filesToUpload.splice(i, 1);
                                }
                        
                                $(this).parent().remove();
                            });
                        
                            this.clear = function () {
                                for (var i = 0; i < filesToUpload.length; ++i) {
                                    if (filesToUpload[i].id.indexOf(sectionIdentifier) >= 0)
                                        filesToUpload.splice(i, 1);
                                }
                        
                                $(this).children(".fileList").empty();
                            }
                        
                            return this;
                        };
                        
                        (function () {
                            var filesToUpload = [];   
                            var files1Uploader = $("#localfile").fileUploader(filesToUpload, "localfile");
                        })()
                        
                        
                        
                        //$("#holder").html('<div class="custom-file"> <input type="file" class="custom-file-input" id="customFile" name="localfile" accept=".owl" multiple required> <label class="custom-file-label" for="customFile">Choose files</label> </div>')
                        /*$(".custom-file-input").on("change", function(e) {
                            var fileName = $(this).val();
                            $(this).next('.custom-file-label').addClass("selected").html(fileName);
                          });*/
                    break
            }
        });