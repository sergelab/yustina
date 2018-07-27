$(function(){
	$('.bio-link a').click(function(){
		$('#bio').slideDown(300);
		return false;
	});
	$('#bio').click(function(){
		$(this).slideUp(300);
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
	var autoSlide = true;

	function nextSlide(n = false){
		if(n === false){
			if(slideNow >= slideCount || slideNow <= 0){
				$('#viewport ul').css('transform', 'translate(0,0)');
				slideNow = 1;
			} else {
				translateWidth = -$('#viewport').width() * slideNow;
				$('#viewport ul').css('transform', 'translate(' + translateWidth + 'px, 0)');
				slideNow++;
			}
		} else {
			slideNow = n;
			nextSlide();
		}
		$('#circles > div').removeClass('current');
		$('#circles > div:nth-child(' + slideNow + ')').addClass('current');
	}

	var timer = setInterval(nextSlide, 5000);
	$('#viewport').hover(function(){ clearInterval(timer); }, function(){ if(autoSlide) timer = setInterval(nextSlide, 5000); });

	$('#circles > div').click(function(){
		clearInterval(timer);
		autoSlide = false;
		nextSlide(parseInt($(this).attr('data-slide')));
	});

	$('.tabs > nav > ul > label').on('click', function(e){
		$('.tabs > nav > ul > label').removeClass('active');
		$(this).addClass('active');
	});
});