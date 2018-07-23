$(function(){
	$('video').click(function(){
		$(this).remove();
	});
	$('.bio-link a').click(function(){
		$('#bio').show(300);
		$('body').animate({ scrollTop: $('#bio').offset().top }, 300);
		return false;
	});

	var h = 0;
	var n = 0;
	$.each($('#person-card-slider ul li'), function(){
		h = Math.max(h, $(this).height());
		n++;
	});
	$('#person-card-slider ul').css('height', h);

	var slideNow = 1;
	var slideCount = $('#viewport ul').children().length;
	var translateWidth = 0;

	function nextSlide(){
		if(slideNow >= slideCount || slideNow <= 0){
			$('#viewport ul').css('transform', 'translate(0,0)');
			slideNow = 1;
		} else {
			translateWidth = -$('#viewport').width() * slideNow;
			$('#viewport ul').css('transform', 'translate(' + translateWidth + 'px, 0)');
			slideNow++;
		}
	}

	var timer = setInterval(nextSlide, 5000);
	$('#viewport').hover(function(){ clearInterval(timer); }, function(){ timer = setInterval(nextSlide, 5000); });


	$('.tabs > nav > ul > label').on('click', function(e){
		$('.tabs > nav > ul > label').removeClass('active');
		$(this).addClass('active');
	});

	$('#bio').click(function(){
		$(this).hide(300);
	});
});