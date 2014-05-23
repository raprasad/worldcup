
function format_mail_links(){

        $('a.mlink').each(function(){
			e = this.rel.replace('/','@');
			//alert(e);
			this.href = 'mai' + '' +'lto:' + e;
			$(this).text(e);
		});

  // in: <a href="person/place.com">something or nothing</a>
        // out: <a href="mailto:person@place.com">Email</a>
		$('a.mlink2').each(function(){
			e = this.rel.replace('/','@');
			this.href = 'mai' + '' +'lto:' + e;
			$(this).text('Email');
		});


        // in: <a href="person/place.com">some text</a>
        // out: <a href="mailto:person@place.com">some text</a>
		$('a.mlink3').each(function(){
			e = this.rel.replace('/','@');
			this.href = 'mai' + '' +'lto:' + e;
		});
}		

