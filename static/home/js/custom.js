

$('#myModal').on('shown.bs.modal', function (obj) {
    debugger;
    $('#myInput').trigger('focus')
  })


  function UpdateModal(Upjson,PageUrl){
    Upjson = Upjson.split(",");
    let UpSearch = "";
    $(Upjson).each((UjIndex,UjObj)=>{
        debugger;
        let UpUrlSp = UjObj.split(":")
        Upjson.length - 1 == UjIndex ? UpSearch += `${UpUrlSp[0]}=${UpUrlSp[1]}` : UpSearch += `${UpUrlSp[0]}=${UpUrlSp[1]}&`
    })
    let Ifrem = $('#UpdateModal .modal-body #Update_Ifrem')[0];
        Ifrem.src = `${PageUrl}?${UpSearch}`
    $('#UpdateModal').modal({
        backdrop: 'static',
        keyboard : false
    })
    $("#UpdateSaveBtn").click((btnObj)=>{
        debugger;
        
    })
  }
  function DeleteModal(){
    $('#DeleteModal').modal({
        backdrop: 'static',
        keyboard : false
    })
  }