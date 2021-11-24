function jqGridInclude()
{
    var pathtojsfiles = "/cychurch/static/scripts/jqgrid/"; // need to be ajusted
    // set include to false if you do not want some modules to be included
    var minver = true;
    var modules = [
        { include: true, incfile:'grid.locale-en.js',minfile: 'js/min/grid.locale-en-min.js'}, // jqGrid translation
//        { include: true, incfile:'packall/grid.pack.js',minfile: ''}  // jqGrid all packecd
        { include: true, incfile:'grid.base.js',minfile: 'js/min/grid.base-min.js'}, // jqGrid base
        { include: true, incfile:'grid.common.js',minfile: 'js/min/grid.common-min.js' }, // jqGrid common for editing
        { include: true, incfile:'grid.formedit.js',minfile: 'js/min/grid.formedit-min.js' }, // jqGrid Form editing
        { include: true, incfile:'grid.inlinedit.js',minfile: 'js/min/grid.inlinedit-min.js' }, // jqGrid inline editing
        { include: true, incfile:'grid.celledit.js',minfile: 'js/min/grid.celledit-min.js' }, // jqGrid cell editing
        { include: true, incfile:'grid.subgrid.js',minfile: 'js/min/grid.subgrid-min.js'}, //jqGrid subgrid
        { include: true, incfile:'grid.treegrid.js',minfile: 'js/min/grid.treegrid-min.js'}, //jqGrid treegrid
        { include: true, incfile:'grid.custom.js',minfile: 'js/min/grid.custom-min.js'}, //jqGrid custom 
        { include: true, incfile:'grid.postext.js',minfile: 'js/min/grid.postext-min.js'}, //jqGrid postext
        { include: true, incfile:'grid.tbltogrid.js',minfile: 'js/min/grid.tbltogrid-min.js'}, //jqGrid table to grid 
        { include: true, incfile:'grid.setcolumns.js',minfile: 'js/min/grid.setcolumns-min.js'}, //jqGrid setcolumns
//        { include: true, incfile:'grid.import.js',minfile: 'js/min/grid.import-min.js'}, //jqGrid import
//        { include: true, incfile:'jquery.fmatter.js',minfile: 'js/min/jquery.fmatter-min.js'}, //jqGrid formater
//        { include: true, incfile:'json2.js',minfile: 'js/min/json2-min.js'}, //json utils
//        { include: true, incfile:'JsonXml.js',minfile: 'js/min/JsonXml-min.js'} //xmljson utils
 

    ];
    var filename;
    for(var i=0;i<modules.length; i++)
    {
        if(modules[i].include === true) {
        	
        	if (minver !== true) filename = pathtojsfiles+modules[i].incfile;
        	else filename = pathtojsfiles+modules[i].minfile;
        	if(jQuery.browser.safari || jQuery.browser.msie ) {
        		jQuery.ajax({url:filename,dataType:'script', async:false, cache: true});
        	} else {
        		IncludeJavaScript(filename);
        	}
        }
    }
    
    function IncludeJavaScript(jsFile)
    {
        var oHead = document.getElementsByTagName('head')[0];
        var oScript = document.createElement('script');
        oScript.type = 'text/javascript';
        oScript.src = jsFile;
        oHead.appendChild(oScript);        
    };
};
jqGridInclude();
