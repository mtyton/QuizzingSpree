$(document).ready(function() {
    var active = window.location.pathname;
    $('a[href="' + active + '"]').addClass('active'); 
  });

$( '.nav .nav-link' ).on( 'click', function () {
    $( '.nav' ).find( 'a.active' ).removeClass( 'active' );
});