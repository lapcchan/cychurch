;(function($){
/**
 * jqGrid Brazilian-Portuguese Translation
 * Junior Gobira juniousbr@gmail.com
 * http://jnsa.com.br
 * Dual licensed under the MIT and GPL licenses:
 * http://www.opensource.org/licenses/mit-license.php
 * http://www.gnu.org/licenses/gpl.html
**/
$.jgrid = {};

$.jgrid.defaults = {
	recordtext: "Registro(s)",
	loadtext: "Carregando...",
	pgtext : "/"
};
$.jgrid.search = {
    caption: "Procurar...",
    Find: "Procurar",
    Reset: "Resetar",
    odata : ['igual', 'diferente', 'menor', 'menor igual','maior','maior igual', 'come?ando com','terminando com','cont?m' ]
};
$.jgrid.edit = {
    addCaption: "Incluir",
    editCaption: "Alterar",
    bSubmit: "Enviar",
    bCancel: "Cancelar",
	bClose: "Fechar",
    processData: "Carregando...",
    msg: {
        required:"Campo ? requerido",
        number:"Por favor, informe um n?mero v?lido",
        minValue:"valor deve ser igual ou maior que ",
        maxValue:"valor deve ser menor ou igual a",
        email: "este e-mail n?o ? v?lido",
        integer: "Por favor, informe um valor inteiro",
		date: "Please, enter valid date value"
    }
};
$.jgrid.del = {
    caption: "Delete",
    msg: "Deletar registros selecionado(s)?",
    bSubmit: "Delete",
    bCancel: "Cancelar",
    processData: "Carregando..."
};
$.jgrid.nav = {
	edittext: " ",
    edittitle: "Alterar registro selecionado",
	addtext:" ",
    addtitle: "Incluir novo registro",
    deltext: " ",
    deltitle: "Deletar registro selecionado",
    searchtext: " ",
    searchtitle: "Procurar registros",
    refreshtext: "",
    refreshtitle: "Recarrgando Tabela",
    alertcap: "Aviso",
    alerttext: "Por favor, selecione um registro"
};
// setcolumns module
$.jgrid.col ={
    caption: "Mostrar/Esconder Colunas",
    bSubmit: "Enviar",
    bCancel: "Cancelar"
};
$.jgrid.errors = {
	errcap : "Erro",
	nourl : "Nenhuma URL defenida",
	norecords: "Sem registros para exibir",
    model : "Length of colNames <> colModel!"
};
$.jgrid.formatter = {
	integer : {thousandsSeparator: " ", defaulValue: 0},
	number : {decimalSeparator:".", thousandsSeparator: " ", decimalPlaces: 2, defaulValue: 0},
	currency : {decimalSeparator:".", thousandsSeparator: " ", decimalPlaces: 2, prefix: "", suffix:"", defaulValue: 0},
	date : {
		dayNames:   [
			"Sun", "Mon", "Tue", "Wed", "Thr", "Fri", "Sat",
			"Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"
		],
		monthNames: [
			"Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec",
			"January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"
		],
		AmPm : ["am","pm","AM","PM"],
		S: function (j) {return j < 11 || j > 13 ? ['st', 'nd', 'rd', 'th'][Math.min((j - 1) % 10, 3)] : 'th'},
		srcformat: 'Y-m-d',
		newformat: 'd/m/Y',
		masks : {
            ISO8601Long:"Y-m-d H:i:s",
            ISO8601Short:"Y-m-d",
            ShortDate: "n/j/Y",
            LongDate: "l, F d, Y",
            FullDateTime: "l, F d, Y g:i:s A",
            MonthDay: "F d",
            ShortTime: "g:i A",
            LongTime: "g:i:s A",
            SortableDateTime: "Y-m-d\\TH:i:s",
            UniversalSortableDateTime: "Y-m-d H:i:sO",
            YearMonth: "F, Y"
        },
        reformatAfterEdit : false
	},
	baseLinkUrl: '',
	showAction: 'show'
};
})(jQuery);
