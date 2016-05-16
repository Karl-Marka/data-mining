element = document.getElementById("submit")
var DNA = ""
var slength = ""
var aslength = ""

var aine = {
            'F': 'TTT',
            'L': 'CTG',
            'S': 'AGC',
            'Y': 'TAT',
            'W': 'UGG',
            'P': 'CCG',
			'H': 'CAT',
			'Q': 'CAG',
			'R': 'CGC',
			'I': 'ATT',
			'M': 'ATG',
			'T': 'ACC',
			'N': 'AAC',
			'K': 'AAA',
			'V': 'GTG',
			'A': 'GCG',
			'D': 'GAT',
			'E': 'GAA',
			'G': 'GGC'
			};
			
var compl = {
	'A': 'T',
	'T': 'A',
	'G': 'C',
	'C': 'G'
}
			

function backTranslate(){
				var str = document.getElementById("input").value;
				str = str.toUpperCase();
                var new_str = '';
                for (var i=0; i < str.length; i++) {
                    new_str += aine[str[i]];
                }
				DNA = new_str
            }
			

			
function splitPrimer(){
	backTranslate();
	slength = document.getElementById("sense").value;
	aslength = document.getElementById("antisense").value;
	var revComplAsense = '';
	var asense = DNA.slice(0, aslength);
	var sense = DNA.slice(aslength, sense);
	var asenseArray = asense.split("");
	var revAsense = asenseArray.reverse();
	revAsense = revAsense.join("");	
	for (var i=0; i<revAsense.length; i++){
		revComplAsense += compl[revAsense[i]];
	};
	document.getElementById("output").value = "Antisense: " + revComplAsense + " " + "Sense: " + sense
		
}

		
element.addEventListener("click", function(){ splitPrimer(); });
