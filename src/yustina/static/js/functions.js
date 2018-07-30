$(function(){
	$('.bio-link a').click(function(){
		$('#bio').slideDown(300);
		return false;
	});
	$('#bio').click(function(){
		$(this).slideUp(300);
	});

	$('.search-button').click(function(e){
		console.log('search');
		e.preventDefault();
		$('.header-search-form').slideToggle(300);
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
	var autoSlide = true;

	function nextSlide(){
		if(slideNow >= slideCount || slideNow <= 0){
			$('#viewport ul').css('transform', 'translate(0,0)');
			slideNow = 1;
		} else {
			translateWidth = -$('#viewport').width() * slideNow;
			$('#viewport ul').css('transform', 'translate(' + translateWidth + 'px, 0)');
			slideNow++;
		}
		$('#circles > div').removeClass('current');
		$('#circles > div:nth-child(' + slideNow + ')').addClass('current');
	}

	function toSlide(n){
		slideNow = n;
		nextSlide();
	}

	var timer = setInterval(nextSlide, 5000);
	$('#viewport').hover(function(){ clearInterval(timer); }, function(){ if(autoSlide) timer = setInterval(nextSlide, 5000); });

	$('#circles > div').click(function(){
		clearInterval(timer);
		autoSlide = false;
		toSlide(parseInt($(this).attr('data-slide')));
	});

	// $('.tabs > nav > ul > label').on('click', function(e){
	// 	$('.tabs > nav > ul > label').removeClass('active');
	// 	$(this).addClass('active');
	// });

	function ajaxLoad(){
		var ins = $('.ajax-insertion-point');
		if(ins.length == 0) return;
		var s = $(this).scrollTop();
		var y = ins.offset().top;
		var skip = ins.siblings().length;
		if(y <= s + $(window).height()){
			$('body').off('scroll touchmove');
			ins.addClass('active');
			$.ajax({
				url: ins.attr('data-url'),
				data: { skip: skip },
				method: 'GET',
				cache: false,
				success: function(data){
					if(data){
						ins.before(data);
						ins.removeClass('active');
						$('body').on('scroll touchmove', ajaxLoad);
					} else {
						ins.remove();
					}
				},
				error: function(){
					ins.remove();
				}
			});
		}
	}

	$('body').on('scroll touchmove', ajaxLoad);
	ajaxLoad();
});