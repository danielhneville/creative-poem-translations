$(document).ready(function(){

	$('span').on('click', function(){
		var object = { 'word': $(this).attr('word') };
		$.post('/api_call', object, function(res){
			console.log(res);
			if (res['entryContent']){
				var htmlstr = res['entryContent'];
				$('.translate').html(function(){
					return htmlstr;
				});
			} else {
				$('.translate').html('<p>Search term has no results</p>');
			}
		}, 'json');
	});

});
