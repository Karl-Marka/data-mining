

$('#sense').on('input', function() {
	input = $('#input').val();
	inputLength = input.length;
	if (inputLength != 0){
    document.getElementById("antisense").value = parseInt(inputLength * 3) - parseInt(document.getElementById("sense").value)
	};
});

$('#antisense').on('input', function() {
	input = $('#input').val();
	inputLength = input.length;
	if (inputLength != 0){
    document.getElementById("sense").value = parseInt(inputLength * 3) - parseInt(document.getElementById("antisense").value)
	};
});


$('#submit').click(function (){
	var peptide = $('#input').val();
	var asense = $('#antisense').val();
	var mintemp = 0
	var maxtemp = 100
	console.log(peptide + " " + asense);
		if ( asense % 3 != 0){
			alert('Antisense primer length must be divisible by 3 to avoid codon mix-up!')
		}
		
	
	$.get('./cgi-bin/main.py?peptide=' + peptide + '&asense=' + asense + '&mintemp=' + mintemp + '&maxtemp=' + maxtemp).done(function (response) {
		$('#output').html(response);
	}).fail(function () {
		alert('Some kind of error occured!');
	});
});
