var tblProducts;
var vents = {
  items: {
      // cabecera
      cli:'',
      date_joined:'',
      subtotal: 0.00,
      iva: 0.00,
      total: 0.00,

  //    Detalle
      products: []
      },


    calculate_invoice: function ()
    {

        var subtot = 0.00;
        var iva = $('input[name="iva"]').val();
        $.each(this.items.products, function (pos, dict){
            dict.pos = pos;
            dict.subtotal = dict.cant* parseFloat(dict.precio)
            subtot += dict.subtotal;
        });
        this.items.subtotal = subtot;
        //calculo de iva
        this.items.iva = this.items.subtotal*iva;
        this.items.total = this.items.subtotal + this.items.iva;

        $('input[name="subtotal"]').val(this.items.subtotal.toFixed(2));
        $('input[name="ivacalc"]').val(this.items.iva.toFixed(2));
        $('input[name="total"]').val(this.items.total.toFixed(2));
    },
    // agregar datos a tabla
    add: function (item){

       this.items.products.push(item);
       this.list();
    },

    // listar tabla
      list: function (){
            this.calculate_invoice();
          tblProducts=$('#tblProducts').DataTable({
            responsive: true,
            autoWidth: false,
            destroy: true,
              // mando coleccion de diccionarios
            data: this.items.products,
            columns: [
                {"data": "id"},
                {"data": "name"},
                {"data": "categoria.nombre_categoria"},
                {"data": "precio"},
                {"data": "cant"},
                {"data": "subtotal"},
            ],
            columnDefs: [
                {
                    // icono borrar
                    targets: [0],
                    class: 'text-center',
                    orderable: false,
                    render: function (data, type, row) {
                        return '<a rel="remove" class="btn btn-danger btn-xs btn-flat"><i class="fas fa-trash-alt" style="color: white"></i></a>';
                    }
                },

                // precio venta
                {
                    targets: [-3],
                    class: 'text-center',
                    orderable: false,
                    render: function (data, type, row) {
                        //convertir a float
                        return 'Q' + parseFloat(data).toFixed(2);
                    }
                },
                {
                    //cantidad
                    targets: [-2],
                    class: 'text-center',
                    orderable: false,
                    render: function (data, type, row) {
                        //cantidad
                        return '<input type="text" name="cant" class="form-control form-control-sm input-sm" autocomplete="off" value="'+row.cant+'">';
                    }
                },
                {
                    targets: [-1],
                    class: 'text-center',
                    orderable: false,
                    render: function (data, type, row) {
                        //convertir a float
                        return 'Q' + parseFloat(data).toFixed(2);
                    }
                },
            ],
              //touchpin para cantidades
            rowCallback(row, data, displayNum, displayIndex, dataIndex){
                 $(row).find('input[name="cant"]').TouchSpin({
                    min: 1,
                    max: 1000000000,
                    step: 1,

                });
            },
            initComplete: function (settings, json) {

            }
        });
    },
};

// formato para visualizar imagenes
function formatRepo(repo) {
    if (repo.loading) {
        return repo.text;
    }

    var option = $(
        '<div class="wrapper container">'+
        '<div class="row">' +
        '<div class="col-lg-1">' +
        '<img src="' + repo.image + '" class="img-fluid img-thumbnail d-block mx-auto rounded">' +
        '</div>' +
        '<div class="col-lg-11 text-left shadow-sm">' +
        //'<br>' +
        '<p style="margin-bottom: 0;">' +
        '<b>Nombre:</b> ' + repo.name + '<br>' +
        '<b>Categoría:</b> ' + repo.categoria.nombre_categoria + '<br>' +
        '<b>Precio:</b> <span class="badge badge-warning">Q'+repo.precio+'</span>'+
        '</p>' +
        '</div>' +
        '</div>' +
        '</div>');

    return option;
}


//fin formato para visaualizar
$(function () {
    // selector de pprodcutos
    $('.select2').select2({
        theme: "bootstrap4",
        language: 'es'
    });
    // para selector de fechas
     $('#date_joined').datetimepicker({
         format: 'YYYY-MM-DD',
         date: moment().format("YYYY-MM-DD"),
         locale: 'es',
         // minDate: moment().format("YYYY-MM-DD"),

     });

     // para precios
    $("input[name='iva']").TouchSpin({
                min: 0,
                max: 100,
                step: 0.01,
                decimals: 2,
                boostat: 5,
                maxboostedstep: 10,
                postfix: '%'
            }).on('change', function (){
    //            al hacer clic
            vents.calculate_invoice();

    }).val(0.12);

    // busqueda de productos el nombre search viene del nombre del imput del producto

     /*$('input[name="search"]').autocomplete({
        source: function (request, response) {
            $.ajax({
                url: window.location.pathname,
                type: 'POST',
                data: {
                    'action': 'search_products',
                    'term': request.term
                },
                dataType: 'json',
            }).done(function (data) {
                response(data);
            }).fail(function (jqXHR, textStatus, errorThrown) {
                //alert(textStatus + ': ' + errorThrown);
            }).always(function (data) {

            });
        },
        delay: 500,
        minLength: 1,
        select: function (event, ui) {
            event.preventDefault();
            console.clear();
            ui.item.cant = 1;
            ui.item.subtotal = 0.00;
            console.log(vents.items);
            vents.add(ui.item);

            // vents.items.products.push(ui.item);
            // vents.list();

            $(this).val('');
        }
    });*/


     //eliminar todos los productos
    $('.btnRemoveAll').on('click', function (){

        if(vents.items.products.length == 0) return false;
        alert_action('Notificacion','¿Quires eliminar todos los productos ingresados?', function (){
                    vents.items.products = [];
                    vents.list();
        },function (){
                // opcion cancelar en pregunga emergente
            } );

    });

     //cambio de cantidad y precio y eliminar
    $('#tblProducts tbody')
        .on('click', 'a[rel="remove"]', function (){
            var tr = tblProducts.cell($(this).closest('td, li')).index(); //obtener posicion
            //preguntar para eliminar un producto
            alert_action('Notificacion','¿Quires eliminar este producto?', function (){
                    vents.items.products.splice(tr.row,1);
                    vents.list();
            },function (){
                // opcion cancelar en pregunga emergente
            } );


        })
        .on('change', 'input[name="cant"]',function (){
        var cant = parseInt($(this).val()); //cantidad nueva
        var tr = tblProducts.cell($(this).closest('td, li')).index(); //obtener posicion

        // var data = tblProducts.row(tr.row).data();
        // var data = tblProducts.row(tr.row).node();


        vents.items.products[tr.row].cant = cant;

        vents.calculate_invoice();
        $('td:eq(5)',tblProducts.row(tr.row).node()).html( 'Q'+vents.items.products[tr.row].subtotal.toFixed(2));
    });

    //boton limpiar caja de buscador
    $('.btnClearSerch').on('click', function(){
        $('input[name="search"]').val('').focus();
    });


    //envio de los datos
       $('form').on('submit', function (e) {
            e.preventDefault();

            //validar que hayan productos en la tabala
            if(vents.items.products.length === 0) {
                message_error('No hay productos para facturar');
                return false;
            }
            vents.items.date_joined =  $('input[name="fecha"]').val();
            vents.items.cli =  $('select[name="cliente"]').val();



            var parameters = new FormData();
            parameters.append('action', $('input[name="action"]').val());
            parameters.append('vents', JSON.stringify(vents.items));

            submit_with_ajax(window.location.pathname, 'Notificación', '¿Estas seguro de realizar la siguiente acción?', parameters, function (response) {
                //si se agrega correctamente la factura
                alert_action('Impresion', '¿Dese imprimir la factura registrada?', function (){
                    // location.href = '/erp/sale/invoice/pdf/'+ response.id +'/'; //Esto abre una ventana emergente para imprimir o ver la impresion , pero no regresa
                    window.open('/erp/pedido/invoice/pdf/'+ response.id +'/','_blank');
                    location.href = '/erp/pedido/list/';
                },function (){
                // opcion cancelar en pregunga emergente
                    location.href = '/erp/producto/list/';
            } );

            });
        });

       // select2 para buscador de productos
    $('select[name="search"]').select2({
        theme: "bootstrap4",
        language: 'es',
        allowClear: true,
        ajax: {
            delay: 250,
            type: 'POST',
            url: window.location.pathname,
            data: function (params) {
                var queryParameters = {
                    term: params.term,
                    action: 'search_products'
                }
                return queryParameters;
            },
            processResults: function (data) {
                return {
                    results: data
                };
            },
        },
        placeholder: 'Ingrese una descripción',
        minimumInputLength: 1,
        templateResult: formatRepo,
    })
        .on('select2:select', function (e) {
        // recuperar datos
        var data = e.params.data;
        data.cant = 1;
        data.subtotal = 0.00;
        vents.add(data);
        // limpiar
        $(this).val('').trigger('change.select2');
    });


       vents.list();
});