function get_order() {
	axios.get('https://jsonplaceholder.typicode.com/todos/1').then(resp => {
		// axios.get('https://4dgxju5lue.execute-api.localhost.localstack.cloud:4566/api/pensionistas').then(resp => {
		var response = {
			"list_orders": [
			  [
				1,
				"APROVADO",
				"João",
				[
				  "misto",
				  "x-salada"
				]
			  ],
			  [
				2,
				"APROVADO",
				"Lúcia",
				[
				  "misto",
				  "hot-dog"
				]
			  ],
			  [
				3,
				"APROVADO",
				"Igor",
				[
				  "hot-dog",
				  "x-salada"
				]
			  ],
			  [
				4,
				"PROCESSANDO",
				"Lucas",
				[
				  "x-salada",
				  "misto"
				]
			  ]
			]
		  }

		// var response = resp.data;
		var table = document.getElementById('table_user').getElementsByTagName('tbody')[0];

		// LIMPAMOS O QUE TINHA ANTES e depois inserimos novos itens
		// isso impede que a tabela reexiba os dados seguidamente
		for (i = table.rows.length - 1; i >= 0; i--) {
			table.deleteRow(i);
		}

		for (var i = 0; i < response.list_orders.length; i++) {
			// criar uma nova linha de tabela e insere no começo
			var row = table.insertRow(i);

			// cria duas novas células (id, nome)
			//var cell1 = row.insertCell(0);
			//var cell2 = row.insertCell(1);

			for (var j = 0; j < response.list_orders[i].length; j++)
			{
				// cria uma nova células (id, nome, e etc...)
				var cell1 = row.insertCell(j);
				// altera o texto da célula (id, nome, e etc...)
				cell1.innerHTML = response.list_orders[i][j];
			}

			// segunda posição da linha i => nome
			//cell2.innerHTML = response.list[i][0]
			//cell2.innerHTML = response.list[i][1]

			// print
			console.log(response.list_orders[i]);
		}
	});
}


function post_order() {
	// var table = document.getElementById('table_user')
	var nome = document.getElementById('order_name').value;
	var itens = document.getElementById('order_items').value;

	console.log(nome); // "José"
	console.log(itens); // "1,2,3"

	var order = {
		"nome": nome,
		"items": itens.split(",")
	}

	console.log(order);

	// axios.get('https://jsonplaceholder.typicode.com/todos/1').then(resp => {
	//axios.get('https://4dgxju5lue.execute-api.localhost.localstack.cloud:4566/api/pensionistas').then(resp => {
}
