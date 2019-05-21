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
                        $("#holder").html("")
                        $("#holder").html('<input type="text" class="form-control" id="urlinput" name="url" value="https://github.com/ICCD-MiBACT/ArCo/tree/master/ArCo-release/test/CQ" required>')
                        $("#keywordlabelholder").html('<div class="custom-control custom-checkbox" style="margin-top:20px"> <input type="checkbox" class="custom-control-input" id="keytrue" name="keytrue" onchange="keycheck(this)"> <label class="custom-control-label" for="keytrue">CQ FILE KEYWORD</label> </div> <div id="keyword-holder"> </div> <small id="emailHelp" class="form-text text-muted">Retrieve all files having KEYWORD from this path</small>')
                        
                    break
                case 'local':
                        $("#keywordlabelholder").html("")
                        $("#holder").html("")
                        $("#holder").html('<div class="custom-file"> <input type="file" class="custom-file-input" id="customFile" name="localfile" accept=".owl" multiple required> <label class="custom-file-label" for="customFile">Choose files</label> </div>')
                        $(".custom-file-input").on("change", function(e) {
                            var theFiles = e.target.files;
                            var relativePath = theFiles[0].webkitRelativePath;
                            var folder = relativePath.split("/");
                            $(this).siblings(".custom-file-label").addClass("selected").html(folder[0]);
                          });
                    break
            }
        });