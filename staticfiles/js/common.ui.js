$(function(){

	var _href,
		flag;

	// 초기화
	$('.skip_nav').each(function (i, item) {
		flag = false;
		$(item).find('li').each(function (i) {
			var $this = $(this);
			if ($this.hasClass('current')) {
				skipContentsShow($this);
				flag = true;
			}
		})
		if (flag == false) {
			var $this = $(item).find('li').eq(0);
			skipContentsShow($this);
		}
	})

	// 스킵링크 클릭시 작동
	$('.skip_nav li a').on('click', function () {
		var $this = $(this);
		skipContentsShow($this.parent('li'));
	})

	function skipContentsShow(item) {
		_href = item.find('a').attr('href');
		item.addClass('current').siblings().removeClass('current');
		$(_href).addClass('active').siblings().removeClass('active');
	}

})

