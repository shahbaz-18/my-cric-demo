//[Data Table Javascript]

//Project:	Aries Admin - Responsive Admin Template
//Version:  1.1
//Last change:  15/11/2017
//Primary use:   Used only for the Data Table

$(function () {
    "use strict";

    $('#example1').DataTable();
    $('#example2').DataTable({
      'paging'      : true,
      'lengthChange': false,
      'searching'   : false,
      'ordering'    : true,
      'info'        : true,
      'autoWidth'   : false
    });
	
	
	$('#example').DataTable( {
		dom: 'Bfrtip',
		buttons: [
			'copy', 'csv', 'excel', 'pdf', 'print'
		]
	} );
	
	$('#tickets').DataTable({
	  'paging'      : true,
	  'lengthChange': false,
	  'searching'   : false,
	  'ordering'    : true,
	  'info'        : true,
	  'autoWidth'   : false,
	});
	
	$('#employeelist').DataTable({
	  'paging'      : true,
	  'lengthChange': false,
	  'searching'   : true,
	  'ordering'    : true,
	  'info'        : true,
	  'autoWidth'   : false,
	});
	
  }); // End of use strict