var PledgeManager = (function () {

	function PledgeManager(summaryEltSelector, registryContainerSelector) {
		this.$summary = $(summaryEltSelector);
		this.$container = $(registryContainerSelector);
	}

	PledgeManager.prototype.init = function() {
		this.attach_events();
	};

	PledgeManager.prototype.attach_events = function() {
		$('div.styled-select', this.$container).on('change', 'select', this.select_value_changed.bind(this));
		$('#itemlist button').on('click', function () {
			$('form').submit();
		})
	};

	PledgeManager.prototype.select_value_changed = function(e) {
		$.ajax({
			url: '/registry/update_ajax/',
			data: $('#pledge_form').serialize(),
			dataType: 'json',
			type: 'post'
		}).done(this.update_done).fail(this.update_fail).always(this.update_always);
	};

	PledgeManager.prototype.update_done = function(result) {
		$('#items').find('.badge').text(result['numitems']);
		$('#item_total').text(result['itemtotal'])
		$('#pledge_total').text(result['pledgetotal']);

		$('#items .entry').remove();

		for (var k in result) {
			if (result.hasOwnProperty(k) && k != 'itemtotal' && k != 'pledgetotal' && k != 'numitems') {
				$('#summary').after('<li class="entry">'+result[k][0]+'&times; '+k+' for $'+result[k][1]+'</li>');
			}
		}
	};

	PledgeManager.prototype.update_fail = function(xhr, textStatus, errorThrown) {
		alert('failed to update pledges: ' + textStatus + ' (' + errorThrown + ')');
	};

	PledgeManager.prototype.update_always = function(result) {};

	return PledgeManager;

}());

$(document).ready(function () {
	new PledgeManager('#items', '.registry').init();
});
