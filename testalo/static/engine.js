 $(document).ready(function(){
        $('#keytrue').prop('checked', false);
        $('#toysetcheck').prop('checked', false);
        $('#endpointcheck').prop('checked', false);
        $('#customRadio').prop('checked', true);
        })
        
        $(function() {
            $('#counter').text('0');
            var generallen = $("input[name=test]:checked").length;
            if(generallen>0){$("#counter").text(generallen);}else{$("#counter").text('0');}
        })
        var testcheckboxes = $("input[name=test]");
        testcheckboxes.change(function(){
                    if(testcheckboxes.is(':checked')) {
                        testcheckboxes.removeAttr('required');

                    } else {
                        testcheckboxes.attr('required', 'required');
                    }
                });
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
        function endpointcheckact(checkboxElem) {
            if (checkboxElem.checked == true) {
                      $("#endpointcheck-holder").html('<input type="text" class="form-control" id="endpoint" name="endpointurl" value="http://wit.istc.cnr.it/arco/virtuoso/sparql" required>')
            }
            else{
              $("#endpointcheck-holder").html("")
            }
            }


                var requiredCheckboxes = $('.parameter');
                requiredCheckboxes.change(function(){
                    if(requiredCheckboxes.is(':checked')) {
                        requiredCheckboxes.removeAttr('required');
                        requiredCheckboxes[0].setCustomValidity('');
                    } else {
                        requiredCheckboxes.attr('required', 'required');
                    }
                });

                $("#files").on('submit',function(event) {
                    $('#load').modal('show')
                })
        

        
    

        $('input[type=radio][name=input-path]').change(function() {
            switch ($(this).val()) {
                case 'url':
                        $("#holder").html("")
                        $("#holder").html('<input type="text" class="form-control" id="urlinput" name="url" value="https://github.com/ICCD-MiBACT/ArCo/tree/master/ArCo-release/test/CQ" required>')
                        $("#keywordlabelholder").html('<div class="custom-control custom-checkbox" style="margin-top:20px"> <input type="checkbox" class="custom-control-input" id="keytrue" name="keytrue" onchange="keycheck(this)"> <label class="custom-control-label" for="keytrue">CQ FILE KEYWORD</label> </div> <div id="keyword-holder"> </div> <small id="emailHelp" class="form-text text-muted">Retrieve all files having KEYWORD from this path</small>')
                        $("#step2").show()
                        $("#local-para").html("")
                    break
                case 'local':
                    $("#keywordlabelholder").html("")
                    $("#holder").html("")
                    $("#holder").html('<div class="custom-file" style="height:100% !important"> <input type="file" class="custom-file-input" id="customFile" name="localfile" accept=".owl" multiple required onchange="updateList()"> <label class="custom-file-label" for="customFile">Choose files</label> <div id="fileList"></div> </div>')
                    $("#step2").hide()
                    $("#local-para").html('<div class="custom-control custom-checkbox" style="margin-top:20px"> <input required oninvalid="this.setCustomValidity(&#39;Please select at least CQ TOYSET KEYWORD or CQ SPARQL ENDPOINT URL&#39;)" oninput="setCustomValidity(&#39;&#39;)" type="checkbox" class="parameter custom-control-input" id="toysetcheck" name="toysetcheck" onchange="toysetcheckact(this)"> <label class="custom-control-label" for="toysetcheck">CQ TOYSET KEYWORD</label> </div> <div id="toysetkeyword-holder"> </div> <small id="emailHelp" class="form-text text-muted">If some toy-dataset-files are used as InputTestData they will be traced trough TOYSET-KEYWORD</small> <div class="custom-control custom-checkbox" style="margin-top:20px"> <input required type="checkbox" class="parameter custom-control-input" id="endpointcheck" name="endpointcheck" onchange="endpointcheckact(this)"> <label class="custom-control-label" for="endpointcheck">CQ SPARQL ENDPOINT URL</label> </div> <div id="endpointcheck-holder"> </div> <small id="emailHelp" class="form-text text-muted">CQ will be executed on selected SPARQL ENDPOINT</small>')

                    var requiredCheckboxes = $('.parameter');
                    requiredCheckboxes.change(function(){
                        if(requiredCheckboxes.is(':checked')) {
                            requiredCheckboxes.removeAttr('required');
                            requiredCheckboxes[0].setCustomValidity('');
                        } else {
                            requiredCheckboxes.attr('required', 'required');
                        }
                    });
    

                break
        }
    });

    updateList = function() {
        var input = document.getElementById('customFile');
        var output = document.getElementById('fileList');
      
        output.innerHTML = '<ul>';

        var lenghtfiles = input.files.length
        for (var i = 0; i < lenghtfiles; ++i) {
          output.innerHTML += '<li>' + input.files.item(i).name + '</li>';
        }
        output.innerHTML += '</ul>';
        
        var snippet = ""
        if (lenghtfiles > 1) {
            snippet = "s "
        } else {
            snippet = " "
        }
        $('.custom-file-label').html(input.files.length + " file" + snippet + "selected");
      }
