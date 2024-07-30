/*
 * Author : Ngoc Nguyen
 * Description : Builds breadcrumbs for UNAVCO's website
 * Date : 05/2019
 */

/*
 * Create breadcrumbs by looking at the URL
 */
(function create_bread_crumbs(){
	var home = '<a href="//www.unavco.org">home</a>',
		separator = ' <img src="/lib/images/arrow-bullet.png" border="0" alt="separator"> ',
		known_hosts = {
			'www.unavco.org': '<a href="' + location.origin + '">gage</a>',
			'www.earthscope.org': '<a href="' + location.origin + '">earthscope</a>',
			'pbo.unavco.org': '<a href="' + location.origin + '">pbo</a>',
			'proxy-test.unavco.org': '<a href="' + location.origin + '">proxy-server</a>',
			'www-prod.int.unavco.org': '<a href="' + location.origin + '">prod-server</a>',
			'www-staging.int.unavco.org': '<a href="' + location.origin + '">staging-server</a>',
			'beta-web-server.win.int.unavco.org': '<a href="' + location.origin + '">beta-server</a>'
		},
		paths = location.pathname.replace(/^\/|\/$/g, '').split( '/' ),
		bread_crumb_item_path = '',
		bread_crumb_item;

	/*
	 * Checks URL response for potential broken links
	 */
	function is_valid_url( url ){
	    var request = new XMLHttpRequest();
	    
	    if ( !request ){
	        return false;
	    }

	    try {
	    	request.open( 'GET', url, false ); // false = set to synchronous //NOTE: Used to use HEAD here, to just get metadata and not the entire document, but for some reason newer versions of IOS perform miserably with a HEAD request.
	    	request.send( null );
	    	return request.status == 200 ? true : false;
	    } catch( er ) {
	        return false;
	    }
	}

	/*
	 * Builds out the bread crumbs for each path item
	 */
	function clean_bread_crumbs_text( url_source, url_text, length ){
		var known_path_exceptions = {
				'status' : null,
				'documentation.html#!' : null,
				'documentation-internal.html#!' : null,
				'10.7283' : null,
				'hydro' : null,
				'gps-gnss' : 'gps/gnss',
				//'perm_sta.php' : 'permanent station search', # NOT WORKING
				'meetings-events' : 'meetings  \&amp\;  events',
				'tls' : 'Terrestrial Laser Scanning',
				'sciworkshop12' : '2012 science workshop',
				'realtime' : 'Real\&\#45\;time',
				'policies_forms' : 'Policies\, Forms \&amp\; Procedures',													
				'reports' : 'reports to sponsors',
				'meeting_events_pubs' : 'Meeting \&amp\; Event Publications'
			},
			cleaned_url_text,
			url_path = url_source + '/' + url_text + '.html';

		// When we encounter a null item in the exceptions list or if this is a station's page, we exit so as not to build that bread crumb
		if ( known_path_exceptions[ url_text ] === null ){
			return null;
		}

		if ( typeof( known_path_exceptions[ url_text ] ) === 'string' ) {
			// Replace the path's default text with a custom text i.e. sciworkshop12 to 2012 science workshop
			cleaned_url_text = known_path_exceptions[ url_text ].toLowerCase();
		} else {
			// Change text to lowercase and replace hypens and underscores with spaces
			cleaned_url_text = url_text.replace( /-/g, ' ' ).replace( /_/g, ' ' ).replace( '.html', '' ).toLowerCase();
		}


		// Create breadcrumb with hyperlinks
		if( count < length ){
			// Purposely change URL source for short-courses as an exception
			if( url_source === '/education/professional-development/short-courses/2019' ){
				url_path = '/education/professional-development/short-courses/short-courses.html';
			};

			// Station pages do not end in .html
			if( url_source.indexOf( 'instrumentation/networks/status' ) >= 0 ){
				url_path = url_source;
			}

			// If the link is broken, we exit so as not to build that bread crumb
			if( !is_valid_url( url_path ) ){
				/*if ( location.hostname === 'beta-web-server.win.int.unavco.org' ){
					return '<span style="text-decoration: line-through;">' + url_text + '</span>';
				} else {
					return null;
				}*/

				return null;
			}

			return '<a href="' + url_path + '"<a>' + cleaned_url_text + '</a>';
		} else {
			// The last element will not have a working hyperlink instead be just plain text
			return '<a class="disabled" href="' + url_path + '"<a>' + cleaned_url_text + '</a>';
		}
	}

	/*
	 * Remove last element from paths array, if it follows the logic of /topic/topic.html
	 */
	if( ( paths [ paths.length - 1 ].replace( '.html', '' ) === paths [ paths.length - 2 ] ) && ( paths [ paths.length - 1 ].indexOf( '.html' ) >= 0 ) ){
		paths.pop();
	}

	/*
	 * Iterates through the paths array to build the individual breadcrumb elements
	 */
	for( var count = 0; count < paths.length; count++ ){
		bread_crumb_item_path += '/' + paths[ count ];

		bread_crumb_item = clean_bread_crumbs_text( bread_crumb_item_path, paths[ count ], paths.length - 1 );

		if( bread_crumb_item !== null ){
			paths[ count ] = bread_crumb_item;
		} else {
			paths.splice( count, 1 );
			count = count - 1;
		}
	}

	/*
	 * Adds reference to other known hosts to the beginnign of the path array
	 */
	if( known_hosts[ location.hostname ] ){
		paths.unshift( known_hosts[ location.hostname ] );
	}

	/*
	 * Adds reference to the home page
	 */
	paths.unshift( home );

	document.write( '<div class="crumb">' + paths.join( separator ) + '</div>' );
})();

$( document ).ready(function() {
	/*
	 * Highlights side nav items based upon breadcrumbs
	 */
	(function set_side_nav_current(){
		var side_nav = $( '#side_nav' ),
			side_nav_item,
			bread_crumb_items = $( '.crumb a' ),
			bread_crumb_items_path,
			bread_crumb_length = bread_crumb_items.length - 1;

		/* 
		 * If side nav exists then iterate through the breadcrumbs and select the corresponding item 
		 * in the side nav to highlight
		 */
		if( side_nav.length ){
			bread_crumb_items.each( function( index, item ){
				bread_crumb_items_path = item.href.replace( location.origin , '');
				side_nav_item = $( '#side_nav a[href="' + bread_crumb_items_path + '"]' );

				// If side nav item exists then add '_current' to parent nav items and '_current_last' to last item
				if ( side_nav_item.length ){
					item_class = side_nav_item.attr( 'class' );
					nav_level = item_class.substring( 0, item_class.indexOf( '_level_nav' ) );

					if( index === bread_crumb_length ){
						side_nav_item.attr( 'class', nav_level + '_level_nav_current_last' ); 
					} else {
						side_nav_item.attr( 'class', nav_level + '_level_nav_current' ); 
					}
				}
			})
		}
	})();
});