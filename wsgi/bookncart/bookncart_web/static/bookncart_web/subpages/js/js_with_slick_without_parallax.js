var prevW = -1, prevH = -1;
var navBottom = 0 + $('#navbar_pc').height();
var $isFloatingButtonRotated = false;

$(document).ready(function(){
	prevW = $(window).width();
	prevH = $(window).height();
	getScrollLocationAndSetNavBarStyles(); // display transparent navbar on page load or opaque on refresh
	initProductSliderSlick();  // slick init for all books sliders
	setUpButtonClicks(); // add to cart,favourites and compare button click
	setModalWindowsChangeListener();
	prepareNavbarCategoryList();
	
});



$(window).resize(function() {
	if(this.resizeTO) clearTimeout(this.resizeTO);
	this.resizeTO = setTimeout(function() {
		$(this).trigger('resizeEnd');
	}, 500);
});

$(window).bind('resizeEnd', function() {
	var widthChanged = 0, heightChanged = 0;
	widthChanged = $(window).width() - prevW;
	heightChanged = $(window).height() - prevH;

	if(widthChanged != 0){
		// if window width is greater than 768px or if it is not a touch device
		// if( Modernizr.mq('only screen and (min-width: 768px)')  || (! Modernizr.touch) ){}
		if(widthChanged > 50 || widthChanged < -50){
			resizeSlick();
			setUpButtonClicks();
		}
	}

	prevW = $(window).width();
	prevH = $(window).height();
});

$(window).scroll(function(){
	if( $("#navbar_pc").length > 0 ){
		var stop = $(window).scrollTop();
		if (stop > navBottom) {
			navbarBackgroundTransparencyHide();
		} else {        
			navbarBackgroundTransparencyShow();
		}
	}
});

function getScrollLocationAndSetNavBarStyles(){
	var loc = $(window).scrollTop();
	if(loc > navBottom){
		navbarBackgroundTransparencyHide();
	} else{
		navbarBackgroundTransparencyShow();
	}
}

function initProductSliderSlick(){
	var width_for_slick = parseInt($(".show_products_as_slick").css("width"),10) ;
	var number_of_products = width_for_slick / 200;
	number_of_products = Math.floor(number_of_products);
	var autoplay_b = false;
	if(number_of_products < 2){
		autoplay_b = true;
	}
	$(".show_products_as_slick").each(function(idx, item){
		$(this).slick({
			infinite: false,
			slidesToShow: number_of_products,
			slidesToScroll: number_of_products,
			autoplay : autoplay_b,
			autoplaySpeed : 2500,
			appendArrows: $(this),			   
		});
	});
}

function resizeSlick(){			
	$(".show_products_as_slick").slick("unslick");
	var width_for_slick = parseInt($(".show_products_as_slick").css("width"),10) ;
	var number_of_products = width_for_slick / 200;
	number_of_products = Math.floor(number_of_products);
	var autoplay_b = false;
	if(number_of_products < 2){
		autoplay_b = true;
	}
	$(".show_products_as_slick").each(function(idx, item){
		$(this).slick({
			infinite: false,
			slidesToShow: number_of_products,
			slidesToScroll: number_of_products,
			autoplay : autoplay_b,
			autoplaySpeed : 2500,
			appendArrows: $(this),			   
		});
	});
}

function setUpButtonClicks(){
	$(".button_cart").click(function(){
		alert('add to cart');
	});

	$(".button_favourite").click(function(){
		var $this = $(this);
		if($this.find('span').hasClass("red_heart")){
			$this.find('span').removeClass("red_heart");
		}
		else{
			$this.find('span').addClass("red_heart");
		}
	});

	$(".button_compare").click(function(){
		alert('compare');
	});
}

function navbarBackgroundTransparencyHide(){
	$("#navbar_pc_logo").css("visibility","visible");
	$("#up_button_floating").slideDown({
		complete: function(){
			if( $isFloatingButtonRotated == true ){
				$isFloatingButtonRotated = false;
				$('#up_button_floating').animate({  borderSpacing: 0 }, {
					step: function(now,fx) {
						$(this).css('-webkit-transform','rotate('+now+'deg)'); 
						$(this).css('-moz-transform','rotate('+now+'deg)');
						$(this).css('transform','rotate('+now+'deg)');
					},
					duration:'fast'
				},'linear');
			}

		}
	});
}

function navbarBackgroundTransparencyShow(){
	$("#navbar_pc_logo").css("visibility","hidden");
	$("#up_button_floating").slideUp();
}

function setModalWindowsChangeListener(){
	$("#login_arrow_modal_11").css("visibility","visible");	
	$("#signup_arrow_modal_11").css("visibility","hidden");
	$(".visible_for_signup").css("display","none");
	$(".visible_for_login").css("display","block");

	$("#sign_up_text_modal_11").click(function(){
		$("#login_arrow_modal_11").css("visibility","hidden");	
		$("#signup_arrow_modal_11").css("visibility","visible");
		$(".visible_for_signup").css("display","block");
		$(".visible_for_login").css("display","none");
	});
	$("#login_text_modal_11").click(function(){
		$("#login_arrow_modal_11").css("visibility","visible");	
		$("#signup_arrow_modal_11").css("visibility","hidden");
		$(".visible_for_signup").css("display","none");
		$(".visible_for_login").css("display","block");
	});
}

function prepareNavbarCategoryList() {
    $('#expList').find('li:has(ul)').unbind('click').click(function(event) {
        if(this == event.target) {
            $(this).toggleClass('expanded');
            $(this).children('ul').toggle('medium');
        }
        return false;
    }).addClass('collapsed').removeClass('expanded').children('ul').hide();
 
    //Hack to add links inside the cv
    $('#expList a').unbind('click').click(function() {
        window.open($(this).attr('href'));
        return false;
    });
    
}


// set scroll to top button functioning
$("#up_button_floating").click(function(){
	$isFloatingButtonRotated = true;

	$('#up_button_floating').animate({  borderSpacing: -180 }, {
		step: function(now,fx) {
			$(this).css('-webkit-transform','rotate('+now+'deg)'); 
			$(this).css('-moz-transform','rotate('+now+'deg)');
			$(this).css('transform','rotate('+now+'deg)');
		},
		duration:'slow'
	},'linear');

	$('html, body').animate({ scrollTop: 0 }, 'slow', function () {
		
	});
});

function centerModal() {
	$(this).css('display', 'block');
	var $dialog = $(this).find(".modal-dialog");
	var offset = ($(window).height() - $dialog.height()) / 2;
    // Center modal vertically in window
    $dialog.css("margin-top", offset);
}

$('.modal').on('show.bs.modal', centerModal);
$(window).on("resize", function () {
	$('.modal:visible').each(centerModal);
});