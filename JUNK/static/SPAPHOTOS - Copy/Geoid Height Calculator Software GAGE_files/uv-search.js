// JavaScript Document
// Refactored 2017-09-15- JR - To use new Custom Search Element Control API 2.0

(function() {
    var cx = '013932175650203472878:urnkt25qjyc';
    var gcse = document.createElement('script');
    gcse.type = 'text/javascript';
    gcse.async = true;
    gcse.src = 'https://cse.google.com/cse.js?cx=' + cx;
    var s = document.getElementsByTagName('script')[0];
    s.parentNode.insertBefore(gcse, s);
  })();

function inputFocus() {
	document.getElementById('query-input').style['background'] = '';
}

function inputBlur() {
	var queryInput = document.getElementById('query-input');
	if (!queryInput.value) {
		queryInput.style['background'] = ''
				/*'white url(http://www.google.com/coop/images/'
				+ 'google_custom_search_watermark.gif) no-repeat 0% 50%';*/
	}
}

function submitQuery() {
	window.location = 'https://www.unavco.org/search/search.html?q='
			+ encodeURIComponent(
					document.getElementById('query-input').value);
	return false;
}
