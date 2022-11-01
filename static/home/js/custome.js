$('#myModal').modal({
    backdrop: 'static',
    keyboard : false
})

$('#myModal').on('shown.bs.modal', function () {
    $('#myInput').trigger('focus')
  })