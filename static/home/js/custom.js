

$('#myModal').on('shown.bs.modal', function (obj) {
    debugger;
    $('#myInput').trigger('focus')
  })


  function UpdateModal(Upjson,PageUrl){
    Upjson = Upjson.split(",");
    let UpSearch = "";
    $(Upjson).each((UjIndex,UjObj)=>{
        let UpUrlSp = UjObj.split(":")
        Upjson.length - 1 == UjIndex ? UpSearch += `${UpUrlSp[0]}=${UpUrlSp[1]}` : UpSearch += `${UpUrlSp[0]}=${UpUrlSp[1]}&`
    })
    let Ifrem = $('#UpdateModal .modal-body #Update_Ifrem')[0];
        Ifrem.src = `${PageUrl}?${UpSearch}`
    $('#UpdateModal').modal({
        backdrop: 'static',
        keyboard : false
    })
    $("#UpdateSaveBtn").click((UpBtnObj)=>{
        $($($(UpBtnObj.currentTarget).closest(".modal-content").find("iframe"))[0].contentDocument).find("form").submit()
        $('#UpdateModal').modal("hide")
        window.location.reload();
    })
    $("#UpdateCloseBtn").click((ClBtnObj)=>{
        debugger;
        $($(ClBtnObj.currentTarget).closest(".modal-content").find("iframe")).removeAttr("src")
    })
  }
  function DeleteModal(){
    $('#DeleteModal').modal({
        backdrop: 'static',
        keyboard : false
    })
  }